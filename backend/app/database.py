import os

from dotenv import load_dotenv

load_dotenv()

#database.py
#import the create_engine function which will allow for creating an interface to the PostgreSQL database
#sessionmaker and DeclarativeBase are also added as to be used later
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#Put in environment variables, .env, before publishing to github.
#this is a url for the corresponding database, using psycopg to actually perform the work on PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

#provide said url to the create_engine function, this will create the engine that can interface with the PostgreSQL database
engine = create_engine(DATABASE_URL)

#create the Base class to be used by models
class Base(DeclarativeBase):
    pass

#create a session maker to be called by other files when in need of a session for the corresponding PostgreSQL database
SessionLocal = sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False
      )

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
