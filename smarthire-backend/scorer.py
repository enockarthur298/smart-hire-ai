def calculate_score(parsed):
    score = 0

    # Skill match (50%)
    required_skills = {"react", "node.js", "python", "flask", "docker"}
    match_count = len(set(skill.lower() for skill in parsed["skills"]) & required_skills)
    score += (match_count / len(required_skills)) * 50

    # Experience (30%)
    years = parsed["experience"]
    if years >= 5:
        score += 30
    elif years >= 3:
        score += 20
    else:
        score += 10

    # Education (20%)
    if "computer" in parsed["education"].lower():
        score += 20
    elif "engineering" in parsed["education"].lower():
        score += 10

    return int(score)
