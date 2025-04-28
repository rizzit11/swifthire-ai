# backend/models.py

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class Resume(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    phone: str
    skills: List[str]
    education: List[str]
    experience: List[str]
    uploaded_at: Optional[datetime] = None

class Job(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    title: str
    company: str
    description: str
    required_skills: List[str]
    location: Optional[str] = None
    posted_at: Optional[datetime] = None

class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    username: str
    email: EmailStr
    hashed_password: str
    created_at: Optional[datetime] = None
