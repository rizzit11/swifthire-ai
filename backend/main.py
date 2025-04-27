from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from chains import generate_questions

app = FastAPI()

# Existing health checks
@app.get("/")
async def health_check():
    return {"status": "OK", "project": "SwiftHire AI"}

@app.get("/db-health")
async def db_health():
    info = await app.mongodb_client.server_info()
    return {"mongo_running": True, "mongo_version": info.get("version")}

# 1. Define request model
class QuestionRequest(BaseModel):
    job_description: str

# 2. Define response model
class QuestionResponse(BaseModel):
    questions: list[str]

# 3. Add the new endpoint
@app.post("/generate-questions", response_model=QuestionResponse)
async def generate_questions_endpoint(req: QuestionRequest):
    try:
        qs = generate_questions(req.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"questions": qs}
