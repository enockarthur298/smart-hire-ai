import os
import json
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_questions_from_resume(raw_json):
    print("✅ Resume Data Received:", raw_json)

    prompt = f"""
You are a technical interviewer. Based on this candidate's resume JSON, generate 5 personalized interview questions.
Only return the questions in plain text, numbered 1 to 5.

Resume JSON:
{json.dumps(raw_json, indent=2)}
"""

    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful AI interviewer."},
            {"role": "user", "content": prompt}
        ]
    )

    questions_text = response.choices[0].message.content.strip()
    print("✅ Questions Generated:", questions_text)
    return questions_text
