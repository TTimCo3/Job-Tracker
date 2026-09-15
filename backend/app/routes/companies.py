# companies.py

from fastapi import APIRouter, Depends, HTTPException
from models import Company
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from schemas import CompanyCreate, CompanyUpdate

comp_router = APIRouter(prefix="/companies")

@comp_router.get("/")
def get_companies(db: Session = Depends(get_db)):
    execution = db.execute(select(Company))
    return execution.scalars().all()

@comp_router.get("/{company_id}")
def get_company(company_id: int, db: Session = Depends(get_db)):
    comp = db.execute(select(Company).where(Company.id == company_id)).scalar_one_or_none()
    if comp:
        return comp
    raise HTTPException(status_code=404, detail="Company not found")

@comp_router.post("/")
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    new_comp = Company(
            name = company.name,
            career_url = company.career_url
            )
    db.add(new_comp)
    db.commit()
    db.refresh(new_comp)
    return new_comp

@comp_router.put("/{company_id}")
def update_company(company_id: int, company: CompanyUpdate, db: Session = Depends(get_db)):
    comp = db.execute(select(Company).where(Company.id == company_id)).scalar_one_or_none()
    if comp:
        comp.name = company.name
        comp.career_url = company.career_url
        db.commit()
        db.refresh(comp)
        return comp
    raise HTTPException(status_code=404, detail="Company not found")

@comp_router.delete("/{company_id}")
def delete_company(company_id: int, db: Session = Depends(get_db)):
    comp = db.execute(select(Company).where(Company.id == company_id)).scalar_one_or_none()
    if comp:
        db.delete(comp)
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Company not found")
