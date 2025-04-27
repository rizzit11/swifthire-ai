"""
chains.py

Mock‐only version: always returns a static list of interview questions
so you can develop without hitting Vertex AI or requiring GCP credentials.
"""

def generate_questions(job_description: str) -> list[str]:
    """
    Return a static list of interview questions for any job_description.
    """
    return [
        "Tell us about your experience with Python and FastAPI.",
        "How have you optimized MongoDB schemas in past projects?",
        "What strategies do you use for cloud-based deployments?",
        "Explain your approach to designing REST APIs.",
        "How do you collaborate with frontend engineers?"
    ]
