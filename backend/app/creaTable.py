#!/usr/bin/env python3
# A python file that will create tables for testing

from database import engine, Base
from models import Application, Job, Company

Base.metadata.create_all(bind=engine)
