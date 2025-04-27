from chains import generate_questions
from chains import generate_questions

jd = """
We are looking for a Python developer with 3+ years experience in FastAPI,
MongoDB, and cloud deployment. Responsibilities include designing REST APIs,
optimizing database schemas, and collaborating with the frontend team.
"""

qs = generate_questions(jd)
print("Generated Interview Questions:")
for i, q in enumerate(qs, 1):
    print(f"{i}. {q}")
