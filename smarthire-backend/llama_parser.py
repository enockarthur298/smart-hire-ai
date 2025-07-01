import os
import re
import requests

# ========== SECTION PARSERS ==========

def extract_name(text):
    # Try to find the first line that isn't empty and doesn't start with special patterns
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith(("**", "=", "Here are")) and not stripped.lower().startswith(("curriculum", "resume")):
            return stripped
    return "Candidate"

def extract_section(text, section_header):
    # Find the section and capture until next section or end
    pattern = rf"\*\*{section_header}\*\*\n+((?:.|\n)*?)(?=\n\*\*|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_skills(text):
    skills_section = extract_section(text, "Technical Skills")
    if not skills_section:
        return []

    skills = set()
    for line in skills_section.split("\n"):
        line = line.strip()
        if line.startswith("= "):
            content = line[2:]
            if ":" in content:
                _, values = content.split(":", 1)
                items = [s.strip() for s in values.split(",") if s.strip()]
                skills.update(items)
            else:
                # Handle single words like: = Postman
                skills.add(content.strip())

    return list(skills)

def extract_experience(text):
    experience_section = extract_section(text, "Total Experience")
    if not experience_section:
        return 0

    # Try to count real years
    match = re.search(r"(\d+)\s*(?:year|month)", experience_section, re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Fallback: count internships as 1 year
    if "intern" in experience_section.lower():
        return 1

    return 0


def extract_cgpa(text):
    # First check education section
    education = extract_section(text, "Education")
    if education:
        match = re.search(r"CGPA[:\s]*([0-9./]+)", education, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Then check entire text
    match = re.search(r"CGPA[:\s]*([0-9./]+)", text, re.IGNORECASE)
    return match.group(1) if match else "N/A"

def extract_education(text):
    education_section = extract_section(text, "Education")
    if not education_section:
        return "Not available"
    
    # Clean up each education line
    education_lines = []
    for line in education_section.split("\n"):
        line = line.strip()
        if line.startswith("= "):
            line = line[2:]  # Remove "= " prefix
            education_lines.append(line)
    
    return "; ".join(education_lines) if education_lines else "Not available"

# ========== LLaMA REQUEST + WRAPPER ==========

def parse_resume_with_llama(resume_text):
    api_key = os.getenv("GROQ_API_KEY")
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a resume parser. Return the following sections clearly:\n"
                    "**Education**\n"
                    "**Total Experience**\n"
                    "**Technical Skills**\n"
                    "**Projects**\n"
                    "**Accomplishments**\n"
                    "Use `= ` before each item inside a section."
                )
            },
            {
                "role": "user",
                "content": resume_text
            }
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    print("✅ Groq Response:\n", content)

    # Extraction
    return {
        "name": extract_name(resume_text),
        "skills": extract_skills(content),
        "experience": extract_experience(content),
        "education": extract_education(content),
        "cgpa": extract_cgpa(content)
    }
