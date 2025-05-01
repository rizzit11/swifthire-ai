import re

def extract_resume_fields(text: str) -> dict:
    # Extract name (first line or bold assumption)
    name = text.split('\n')[0].strip()

    # Extract email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    email = email_match.group(0) if email_match else ""

    # Extract phone number (Indian format assumed)
    phone_match = re.search(r'\b\d{10}\b', text)
    phone = phone_match.group(0) if phone_match else ""

    # Extract skills (basic hardcoded section match)
    skills = []
    if "TECHNICAL SKILLS" in text:
        skill_section = text.split("TECHNICAL SKILLS")[1]
        if "WORK EXPERIENCE" in skill_section:
            skill_text = skill_section.split("WORK EXPERIENCE")[0]
        else:
            skill_text = skill_section
        skills = re.findall(r'[A-Za-z\+#.]+', skill_text)
        skills = [s.strip() for s in skills if len(s.strip()) > 1]

    # Extract education (basic)
    education = []
    if "EDUCATION" in text:
        edu_section = text.split("EDUCATION")[1]
        if "TECHNICAL SKILLS" in edu_section:
            edu_text = edu_section.split("TECHNICAL SKILLS")[0]
        else:
            edu_text = edu_section
        education = [line.strip() for line in edu_text.split("\n") if len(line.strip()) > 5]

    # Extract experience
    experience = []
    if "WORK EXPERIENCE" in text:
        exp_section = text.split("WORK EXPERIENCE")[1]
        if "PROJECTS" in exp_section:
            exp_text = exp_section.split("PROJECTS")[0]
        else:
            exp_text = exp_section
        experience = [line.strip() for line in exp_text.split("\n") if len(line.strip()) > 5]

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience
    }
