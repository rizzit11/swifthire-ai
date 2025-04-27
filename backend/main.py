from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# connect on startup
@app.on_event("startup")
async def connect_db():
    app.mongodb_client = AsyncIOMotorClient("mongodb://localhost:27017")
    app.mongodb = app.mongodb_client.swift_hire_db

# close on shutdown
@app.on_event("shutdown")
async def close_db():
    app.mongodb_client.close()

@app.get("/")
async def health_check():
    return {"status": "OK", "project": "SwiftHire AI"}

@app.get("/db-health")
async def db_health():
    info = await app.mongodb_client.server_info()
    version = info.get("version")
    return {"mongo_running": True, "mongo_version": version}
