from dotenv import load_dotenv
load_dotenv()   

import os
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import CollectionInvalid, OperationFailure
# from google.cloud import documentai_v1 as documentai  # Commenting out Document AI import
# from google.oauth2 import service_account  # Commenting out Document AI auth

# Import PyPDF2 for PDF text extraction
import PyPDF2  # Adding PyPDF2

from chains import generate_questions
from models import Resume, Job, User
from auth import get_password_hash, verify_password, create_access_token

app = FastAPI()

# CORS so your Next.js can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Commented out Google Document AI setup
# Set up credentials for Google Document AI
# credentials = service_account.Credentials.from_service_account_file(
#     "/app/swifthire-458117-50f3c5f19084.json"  # Replace with your credentials file path
# )
# client = documentai.DocumentProcessorServiceClient(credentials=credentials)

@app.on_event("startup")
async def startup_db_client():
    # Read from .env.compose via docker-compose env_file
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name  = os.getenv("MONGO_DB", "swift_hire_db")

    client = AsyncIOMotorClient(mongo_uri)
    app.mongodb_client = client
    app.mongodb = client[db_name]

    # helper to create a collection if missing
    async def try_create(name: str, schema: dict):
        try:
            await app.mongodb.create_collection(name, validator=schema)
        except (CollectionInvalid, OperationFailure):
            pass

    # JSON‐Schema validators
    resume_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "email", "phone", "skills", "education", "experience"],
            "properties": {
                "name":        {"bsonType": "string"},
                "email":       {"bsonType": "string"},
                "phone":       {"bsonType": "string"},
                "skills":      {"bsonType": "array",  "items": {"bsonType": "string"}},
                "education":   {"bsonType": "array",  "items": {"bsonType": "string"}},
                "experience":  {"bsonType": "array",  "items": {"bsonType": "string"}},
            },
        }
    }
    jobs_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["title", "company", "description", "required_skills"],
            "properties": {
                "title":           {"bsonType": "string"},
                "company":         {"bsonType": "string"},
                "description":     {"bsonType": "string"},
                "required_skills": {"bsonType": "array", "items": {"bsonType": "string"}},
                "location":        {"bsonType": ["string", "null"]},
            },
        }
    }
    users_schema = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "email", "hashed_password"],
            "properties": {
                "username":        {"bsonType": "string"},
                "email":           {"bsonType": "string"},
                "hashed_password": {"bsonType": "string"},
            },
        }
    }

    # create collections if they don’t exist
    await try_create("resumes", resume_schema)
    await try_create("jobs",    jobs_schema)
    await try_create("users",   users_schema)


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/")
async def health_check():
    return {"status": "OK", "project": "SwiftHire AI"}


@app.get("/db-health")
async def db_health():
    info = await app.mongodb_client.server_info()
    return {"mongo_running": True, "mongo_version": info.get("version")}


# ———————————————————————————
# Interview Questions endpoint
# ———————————————————————————
class QuestionRequest(BaseModel):
    job_description: str

class QuestionResponse(BaseModel):
    questions: list[str]

@app.post(
    "/generate-questions",
    response_model=QuestionResponse,
    summary="Generate AI interview questions",
)
async def generate_questions_endpoint(req: QuestionRequest):
    try:
        qs = generate_questions(req.job_description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"questions": qs}


# ———————————————————————————
# Upload document and extract text
# ———————————————————————————

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    file_location = f"uploaded_files/{file.filename}"

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    # Save the uploaded file to disk
    with open(file_location, "wb") as f:
        f.write(await file.read())

    # Commented out: Google Document AI part
    # Process the document using Google Document AI
    # with open(file_location, "rb") as document:
    #     document_content = document.read()
    #
    # project_id = "swifthire-458117"
    # location = "us"  # or your respective location
    # processor_id = "8c649504b9e81d90"
    # name = f"projects/{project_id}/locations/{location}/processors/{processor_id}"
    #
    # raw_document = documentai.types.RawDocument(content=document_content)
    # request = documentai.types.ProcessRequest(
    #     name=name,
    #     raw_document=raw_document
    # )
    #
    # response = client.process_document(request=request)
    # extracted_text = response.document.text

    # Using PyPDF2 to extract text from PDF instead
    extracted_text = extract_text_from_pdf(file_location)

    return {"text": extracted_text}


# Auth models
class UserIn(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginIn(BaseModel):
    email: EmailStr
    password: str


# Signup
@app.post("/signup", response_model=Token)
async def signup(user: UserIn):
    users = app.mongodb["users"]
    if await users.find_one({"email":user.email}):
        raise HTTPException(400, "Email already registered")
    hashed = get_password_hash(user.password)
    await users.insert_one({
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed,
        "created_at": datetime.utcnow()
    })
    token = create_access_token({"sub":user.email})
    return {"access_token":token}


# Login
@app.post("/login", response_model=Token)
async def login(form: LoginIn):
    users = app.mongodb["users"]
    u = await users.find_one({"email":form.email})
    if not u or not verify_password(form.password, u["hashed_password"]):
        raise HTTPException(401, "Incorrect email or password")
    token = create_access_token({"sub":form.email})
    return {"access_token":token}
