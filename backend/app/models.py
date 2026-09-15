#models.py

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from database import Base

#handles information on a particular company
class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    career_url: Mapped[Optional[str]]

#jobs is a separate table handling information specific to jobs, keeping it separate will allow for potential future
#features to be easier to implement
class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    title: Mapped[str]
    job_url: Mapped[Optional[str]]
    role_type: Mapped[Optional[str]]
    employment_type: Mapped[Optional[str]]
    work_location: Mapped[Optional[str]]
    location: Mapped[Optional[str]]
    

#Represents an application and the information required to track it
class Application(Base):
    __tablename__ = "applications"
    id: Mapped[int] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.id"))
    status: Mapped[str]
    notes: Mapped[Optional[str]]
    date_added: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    date_applied: Mapped[Optional[datetime]]
