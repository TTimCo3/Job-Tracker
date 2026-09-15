# jobs.py

from fastapi import APIRouter, Depends, HTTPException
from models import Job
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from schemas import JobCreate, JobUpdate

job_router = APIRouter(prefix="/jobs")

@job_router.get("/")
def get_jobs(db: Session = Depends(get_db)):
    execution = db.execute(select(Job))
    return execution.scalars().all()

@job_router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    res_job = db.execute(select(Job).where(Job.id == job_id)).scalar_one_or_none()
    if res_job:
        return res_job
    raise HTTPException(status_code=404, detail="Job not found")

@job_router.post("/")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(
            company_id = job.company_id,
            title = job.title,
            job_url = job.job_url,
            role_type = job.role_type,
            employment_type = job.employment_type,
            work_location = job.work_location,
            location = job.location
            )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@job_router.put("/{job_id}")
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    res_job = db.execute(select(Job).where(Job.id == job_id)).scalar_one_or_none()
    if res_job:
        res_job.company_id = job.company_id
        res_job.title = job.title
        res_job.job_url = job.job_url
        res_job.role_type = job.role_type
        res_job.employment_type = job.employment_type
        res_job.work_location = job.work_location
        res_job.location = job.location
        db.commit()
        db.refresh(res_job)
        return res_job
    raise HTTPException(status_code=404, detail="Job not found")

@job_router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    res_job = db.execute(select(Job).where(Job.id == job_id)).scalar_one_or_none()
    if res_job:
        db.delete(res_job)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Job not found")
