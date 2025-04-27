# SwiftHire AI

A Resume Parsing, Job Matching, and AI Interview Chatbot platform.

## Day 1 Completed Tasks

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
    - `/` health‐check endpoint  
    - `/db-health` to verify MongoDB connection  
- **Project Structure**  
  - Split into `backend/` and `frontend/` folders  
  - Moved all Python code into `backend/`  
  - Captured dependencies in `backend/requirements.txt`  
- **Frontend (Next.js + Tailwind)**  
  - Scaffolded Next.js app in `frontend/` using `create-next-app`  
  - Installed Tailwind v4 via PostCSS plugin  
  - Configured `tailwind.config.js` and `postcss.config.js`  
  - Added `src/app/page.js` (Home) and `src/app/about/page.js`  
  - Updated `layout.js` with navbar links to Home & About  
  - Verified both `/` and `/about` routes  

## Next Steps
1. Add Architecture Overview  

**Folder structure**  
swifthire-ai/ ├─ backend/ FastAPI app + Dockerized MongoDB
├─ frontend/ Next.js 15 (App Router) + Tailwind CSS
└─ README.md This file

**Tech stack**  
- **Frontend:** Next.js, React, Tailwind CSS  
- **Backend:** FastAPI, Python 3.13, Motor, Uvicorn  
- **Database:** MongoDB (running in Docker)

**Request flow**  
1. **Client** (Next.js) → HTTP POST `/api/upload-resume`  
2. **Server** (FastAPI) → parse & store in MongoDB  
3. **Server** → generate embeddings / run matching  
4. **Server** → respond with ranked candidates  
5. **Client** → display results


## 📅 Day 2: Backend Structure & MongoDB Integration

**Goals:** Flesh out backend structure and MongoDB connection.

- Organized code under `backend/` with `main.py`, `chains.py`, `requirements.txt`
- Confirmed `/` and `/db-health` return correct JSON and Mongo version
- Startup event reads `MONGO_URI` env var, defaults to `mongodb://localhost:27017`



## 📅 Day 3: AI Chain & Dockerization

**Goals:** Integrate LangChain for question generation, containerize full stack.

### LangChain Integration

- Created `backend/chains.py` with `generate_questions()`
- Initially used OpenAI → hit 429 quota → added static fallback in exception
- Tried VertexAI (Gemini) → installed `langchain-google-vertexai`, updated imports
- Met GCP errors (no billing) → stubbed chains to always return fallback list

### Docker Compose Setup

- **`backend/Dockerfile`** (Python 3.13-slim, `COPY`, `pip install`, `CMD uvicorn`)
- **`docker-compose.yml`**:
  - `mongo`: official image, volume `mongo_data`
  - `backend`: build context `backend/`, ports `8000:8000`, `env_file: .env`
- Issues tackled:
  - Removed stale `swifthire-mongo` container
  - Created `.env` with `GOOGLE_API_KEY`, `MONGO_URI`
  - Fixed “uvicorn not found” by installing in requirements or using `python -m uvicorn`
  - Silenced the obsolete `version:` warning
  - Managed long build times via caching

### CORS Configuration

- Enabled CORS in `main.py` for `http://localhost:3000`

### Frontend “Generate Questions” UI

- Created `frontend/src/app/questions/page.js` (client component)
- Added “Questions” link in `frontend/src/app/layout.js`
- Handled “Failed to fetch” by ensuring CORS and correct endpoint
- Verified end-to-end: UI → API → mock chain → UI renders list


## 📁 Updated Folder Structure
swifthire-ai/ 
├─ backend/ FastAPI + LangChain (mock) + Dockerfile + chains.py + main.py 
├─ frontend/ Next.js 15 (App Router) + Tailwind + src/app pages 
├─ docker-compose.yml Compose for MongoDB & backend 
├─ .env Environment vars (MONGO_URI, GOOGLE_API_KEY) 
└─ README.md This file

## 🔧 Day 4 Complete with 

- Docker Compose brings up MongoDB + FastAPI (mock chain)  
- `/generate-questions` returns JSON array of 5 questions  
- Questions UI in Next.js calls API and displays list  


