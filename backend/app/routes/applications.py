# applications.py

from schemas import ApplicationCreate, ApplicationUpdate
from database import get_db
from sqlalchemy.orm import Session
from models import Application, Company, Job
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func

router = APIRouter(prefix="/applications")

@router.get("/")
def get_applications(db: Session = Depends(get_db)):
    execution = db.execute(select(Application, Job, Company).join(Job, Application.job_id == Job.id).join(Company, Job.company_id == Company.id))
    rows = execution.all()
    
    results = []

    for application, job, company in rows:
        results.append({
            "company_name": company.name,
            "career_url": company.career_url,
            
            "job_title": job.title,
            "job_url": job.job_url,
            "role_type": job.role_type,
            "employment_type": job.employment_type,
            "work_location": job.work_location,
            "location": job.location,
            
            "id": application.id,
            "status": application.status,
            "notes": application.notes,
            "date_applied": application.date_applied
        })

    return results

@router.get("/{application_id}")
def get_application(application_id: int, db: Session = Depends(get_db)):
    execution = db.execute(select(Application, Job, Company).join(Job, Application.job_id == Job.id).join(Company, Job.company_id == Company.id).where(Application.id == application_id))
    row = execution.one_or_none()
    if row:
        application, job, company = row
        return {
            "company_name": company.name,
            "career_url": company.career_url,
            
            "job_title": job.title,
            "job_url": job.job_url,
            "role_type": job.role_type,
            "employment_type": job.employment_type,
            "work_location": job.work_location,
            "location": job.location,
            
            "id": application.id,
            "status": application.status,
            "notes": application.notes,
            "date_applied": application.date_applied
        }
    else:
        raise HTTPException(status_code=404, detail="Application not found")

@router.post("/")
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    company_name = application.company_name.strip()
    job_title = application.job_title.strip()

    company = db.execute(select(Company).where(func.lower(Company.name) == company_name.lower())).scalar_one_or_none()
    
    if company is None:
        company = Company(name=company_name,
                          career_url=application.career_url)
        db.add(company)
        db.flush()

    job = db.execute(select(Job).where(func.lower(Job.title) == job_title.lower(),
                                       Job.company_id == company.id)).scalar_one_or_none()
    if job is None:
        job = Job(company_id = company.id,
                  title = job_title,
                  job_url = application.job_url,
                  role_type = application.role_type,
                  employment_type = application.employment_type,
                  work_location = application.work_location,
                  location = application.location)
        db.add(job)
        db.flush()

    new_app = Application(
            job_id = job.id,
            status = application.status,
            notes = application.notes,
            date_applied = application.date_applied
            )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)

    execution = db.execute(
        select(Application, Job, Company)
        .join(Job, Application.job_id == Job.id)
        .join(Company, Job.company_id == Company.id)
        .where(Application.id == new_app.id)
    )

    application, job, company = execution.one()

    return {
        "company_name": company.name,
        "career_url": company.career_url,
        
        "job_title": job.title,
        "job_url": job.job_url,
        "role_type": job.role_type,
        "employment_type": job.employment_type,
        "work_location": job.work_location,
        "location": job.location,
        
        "id": application.id,
        "status": application.status,
        "notes": application.notes,
        "date_applied": application.date_applied 
    }

    return new_app

@router.put("/{application_id}")
def update_application(application_id: int, application: ApplicationUpdate, db: Session = Depends(get_db)):
    app = db.execute(select(Application).where(Application.id == application_id)).scalar_one_or_none()
    if app is not None:
        company_name = application.company_name.strip()
        job_title = application.job_title.strip()

        company = db.execute(select(Company).where(func.lower(Company.name) == company_name.lower())).scalar_one_or_none()
       
        if company is not None:
            company.career_url = application.career_url

        if company is None:
            company = Company(name=company_name,
                              career_url=application.career_url)
            db.add(company)
            db.flush()

        job = db.execute(select(Job).where(func.lower(Job.title) == job_title.lower(),
                                           Job.company_id == company.id)).scalar_one_or_none()

        if job is not None:
            job.job_url = application.job_url
            job.role_type = application.role_type
            job.employment_type = application.employment_type
            job.work_location = application.work_location
            job.location = application.location

        if job is None:
            job = Job(company_id = company.id,
                      title = job_title,
                      job_url = application.job_url,
                      role_type = application.role_type,
                      employment_type = application.employment_type,
                      work_location = application.work_location,
                      location = application.location)
            db.add(job)
            db.flush()

        app.job_id = job.id
        app.status = application.status
        app.notes = application.notes
        app.date_applied = application.date_applied

        db.commit()
        db.refresh(app)

        execution = db.execute(
            select(Application, Job, Company)
            .join(Job, Application.job_id == Job.id)
            .join(Company, Job.company_id == Company.id)
            .where(Application.id == app.id)
        )

        application, job, company = execution.one()

        return {
            "company_name": company.name,
            "career_url": company.career_url,
            
            "job_title": job.title,
            "job_url": job.job_url,
            "role_type": job.role_type,
            "employment_type": job.employment_type,
            "work_location": job.work_location,
            "location": job.location,
            
            "id": application.id,
            "status": application.status,
            "notes": application.notes,
            "date_applied": application.date_applied 
        }
    else:
        raise HTTPException(status_code=404, detail="Application not found")

@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    app = db.execute(select(Application).where(Application.id == application_id)).scalar_one_or_none()
    # may want to return 404 for failing to find app
    if app:
        db.delete(app)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Application not found")
