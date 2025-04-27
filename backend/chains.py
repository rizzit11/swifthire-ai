import os

# 1. PromptTemplate and LLMChain come from langchain core
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# 2. Import the supported VertexAI wrapper
from langchain_google_vertexai import VertexAI

# 3. Initialize Gemini via Vertex AI
llm = VertexAI(
    model_name="gemini-1.5-flash-8b",
    api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0.7,
)

# 4. Define your prompt template
template = """
You are an expert recruiter. Given the following job description,
generate 5 focused interview questions that assess both technical skills
and cultural fit.

Job Description:
----------------
{job_desc}

Interview Questions:
1.
"""

prompt = PromptTemplate(template=template, input_variables=["job_desc"])

# 5. Build the chain
interview_chain = LLMChain(llm=llm, prompt=prompt)

def generate_questions(job_description: str) -> list[str]:
    """
    Run the LLMChain on a job description and return a list of questions.
    Fallback to static list if the API call fails.
    """
    try:
        response = interview_chain.run(job_desc=job_description)
    except Exception:
        return [
            "Tell us about your experience with Python and FastAPI.",
            "How have you optimized MongoDB schemas in past projects?",
            "What strategies do you use for cloud-based deployments?",
            "Explain your approach to designing REST APIs.",
            "How do you collaborate with frontend engineers?"
        ]

    # Parse LLM output into numbered questions
    lines = [line.strip() for line in response.splitlines() if line.strip()]
    questions = [
        line.split('.', 1)[1].strip()
        for line in lines
        if line and line[0].isdigit()
    ]
    return questions
