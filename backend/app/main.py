# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.applications import router
from routes.companies import comp_router
from routes.jobs import job_router

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
        )
app.include_router(router)
app.include_router(comp_router)
app.include_router(job_router)
