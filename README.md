# SwiftHire AI

A Resume Parsing, Job Matching, and AI Interview Chatbot platform.

---

## 📅 Day 1: Project Setup & Basics

- **Git & GitHub**  
  - Initialized local repo (`git init`)  
  - Created `swifthire-ai` repository on GitHub and pushed initial commit  
- **VS Code Setup**  
  - Installed Python, Docker, Tailwind, React, and MongoDB extensions  
- **Docker & MongoDB**  
  - Installed Docker Desktop  
  - Ran MongoDB in Docker (`swifthire-mongo` container on port 27017)  
- **Backend (FastAPI)**  
  - Created Python virtual env (`env`) and activated it  
  - Installed FastAPI, Uvicorn, Motor  
  - Built `main.py` with:  
    - `/` health-check endpoint  
    - `/db-health` to verify MongoDB connection  
- **Project Structure**  
  - Split into `backend/` and `frontend/` folders  
  - Captured dependencies in `backend/requirements.txt`  
- **Frontend (Next.js + Tailwind)**  
  - Scaffolded Next.js app in `frontend/` via `create-next-app`  
  - Installed Tailwind v4 via PostCSS plugin  
  - Configured `tailwind.config.js` and `postcss.config.js`  
  - Added `src/app/page.js` (Home) and `src/app/about/page.js`  
  - Updated `layout.js` with navbar links to Home & About  
  - Verified both `/` and `/about` routes  

---

## 📅 Day 2: Backend Structure & MongoDB Integration

**Goals:** Flesh out backend structure, connect to MongoDB.

- Organized code under `backend/` with `main.py`, `chains.py`, `requirements.txt`  
- Confirmed `/` and `/db-health` return correct JSON and Mongo version  
- Startup event reads `MONGO_URI` env var (default `mongodb://localhost:27017`)  

---

## 📅 Day 3: AI Chain & Dockerization

**Goals:** Integrate LangChain for question generation, containerize full stack.

### LangChain Integration

- Created `backend/chains.py` with `generate_questions()`  
- Initially used OpenAI → hit 429 quota → added static fallback list  
- Switched to VertexAI (Gemini) → installed `langchain-google-vertexai`, updated imports  
- Stubbed chain to always return fallback list when GCP credentials weren’t available  

### Docker & Compose

- **`backend/Dockerfile`** (Python 3.13-slim, `COPY`, `pip install`, `CMD uvicorn`)  
- **`docker-compose.yml`**  
  - `mongo`: official image, volume `mongo_data`  
  - `backend`: build context `backend/`, ports `8000:8000`, env_file `.env`  
- Tackled common Docker issues: stale containers, PATH for uvicorn, Compose warnings, caching  

### CORS

- Enabled CORS in `main.py` for `http://localhost:3000`  

---

## 📅 Day 4: Frontend “Generate Questions” UI & End-to-End

**Goals:** Build questions page in Next.js and wire up to `/generate-questions`.

- Created `frontend/src/app/questions/page.js` as a client component  
- Added “Questions” link in `frontend/src/app/layout.js`  
- Built form to POST `{ job_description }` → `/generate-questions` → render list  
- Handled “Failed to fetch” by fixing CORS and correct backend URL  
- Verified full flow in Docker: Next.js UI → FastAPI API → mock chain → rendered questions  

---

## 📅 Day 5 (Mar 16) – Schemas & JWT Auth

**Design & Validation**  
- Defined JSON-schema validators for three collections:  
  - **resumes**: `name`, `email`, `phone`, `skills[]`, `education[]`, `experience[]`  
  - **jobs**: `title`, `company`, `description`, `required_skills[]`, `location`  
  - **users**: `username`, `email`, `hashed_password`  
- Wrapped each `create_collection` in try/except to avoid “already exists”

**JWT Authentication**  
- Added `auth.py` with:  
  - `SECRET_KEY` (from `.env`, fallback `"change-this-secret"`)  
  - `bcrypt` password hashing & verification  
  - `create_access_token()` issuing HS256 JWTs  
- Built `/signup` and `/login` endpoints in `main.py`  
- Tested end-to-end via `curl` → returned `access_token`

**Environment & Docker**  
- Extended `.env` with:  
  ```dotenv
  MONGO_URI=mongodb://mongo:27017/swift_hire_db
  GOOGLE_API_KEY=…
  SECRET_KEY=<your‐jwt‐secret>

## Final Folder Structure (swifthire-ai/)
├─ backend/
|  ├─ .env
│  ├─ Dockerfile
│  ├─ main.py
│  ├─ chains.py
│  ├─ auth.py
│  ├─ models.py
│  └─ requirements.txt
├─ frontend/
│  └─ src/app/
│     ├─ about/page.js
|     ├─ generate-qustions/page.js
|     ├─ login/page.js
|     ├─ signup/page.js
│     ├─ layout.js
│     ├─ page.js
│     ├─ about/page.js
│     └─ questions/page.js
├─ docker-compose.yml
├─ .env.compose           ← MONGO_URI, GOOGLE_API_KEY, SECRET_KEY
└─ README.md

# Day 6: Document Upload & Parsing

## Goals
- Implement file upload functionality.
- Parse documents using PyPDF2.

## Document Upload Functionality

### Upload Endpoint
- Created `/upload-document` endpoint for uploading documents.
- Saves uploaded files to the server's `uploaded_files/` directory.
- Uses FastAPI's `UploadFile` to handle file uploads.

## Document Parsing with PyPDF2

### PyPDF2 Integration
- For now, used **PyPDF2** as a replacement for Google Document AI for PDF parsing.
- The document is parsed, and the extracted text is returned as a response.
- The part of the code using Google Document AI was commented out for later use when billing is activated.

### Code Snippet: 
## PyPDF2 Parser : The document content is extracted using `PdfReader` and returned as text:

<!-- ```python
import PyPDF2

def parse_pdf(file_location):
    with open(file_location, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text -->

## Temporary Workaround: 
Google Document AI was commented out, and PyPDF2 is used in its place for document parsing for testing purposes until billing for Google services is activated.


