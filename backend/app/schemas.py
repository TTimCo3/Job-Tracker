# schemas.py

from datetime import datetime
from pydantic import BaseModel

class CompanyCreate(BaseModel):
    name: str
    career_url: str | None = None

class CompanyUpdate(BaseModel):
    name: str
    career_url: str | None = None

class JobCreate(BaseModel):
    company_id: int
    title: str
    job_url: str | None = None
    role_type: str | None = None
    employment_type: str | None = None
    work_location: str | None = None
    location: str | None = None

class JobUpdate(BaseModel):
    company_id: int
    title: str
    job_url: str | None = None
    role_type: str | None = None
    employment_type: str | None = None
    work_location: str | None = None
    location: str | None = None

class ApplicationCreate(BaseModel):
    company_name: str
    career_url: str | None = None

    job_title: str
    job_url: str | None = None
    role_type: str | None = None
    employment_type: str | None = None
    work_location: str | None = None
    location: str | None = None

    status: str
    notes: str | None = None
    date_applied: datetime | None = None

class ApplicationUpdate(BaseModel):
    company_name: str
    career_url: str | None = None

    job_title: str
    job_url: str | None = None
    role_type: str | None = None
    employment_type: str | None = None
    work_location: str | None = None
    location: str | None = None

    status: str
    notes: str | None = None
    date_applied: datetime | None = None
