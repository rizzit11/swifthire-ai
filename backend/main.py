import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient

from chains import generate_questions

app = FastAPI()

# Allow requests from your Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# Database connection events
# ---------------------------

@app.on_event("startup")
async def startup_db_client():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    app.mongodb_client = AsyncIOMotorClient(mongo_uri)
    app.mongodb = app.mongodb_client.swift_hire_db

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

# ---------------------------
# Health‐check endpoints
# ---------------------------

@app.get("/")
async def health_check():
    return {"status": "OK", "project": "SwiftHire AI"}

@app.get("/db-health")
async def db_health():
    info = await app.mongodb_client.server_info()
    return {
        "mongo_running": True,
        "mongo_version": info.get("version")
    }

# ---------------------------
# Models for the questions API
# ---------------------------

class QuestionRequest(BaseModel):
    job_description: str

class QuestionResponse(BaseModel):
    questions: list[str]

# ---------------------------
# Generate interview questions
# ---------------------------

@app.post("/generate-questions", response_model=QuestionResponse)
async def generate_questions_endpoint(req: QuestionRequest):
    try:
        qs = generate_questions(req.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"questions": qs}
