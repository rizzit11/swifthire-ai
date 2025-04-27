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

## Day 2: Resume Parsing & Job Matching setup  
