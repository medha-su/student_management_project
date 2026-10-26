from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routes.base import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables at startup for a simple, reproducible internship project.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Student Management API",
    description=(
        "A modular FastAPI + SQLite CRUD application for student records. "
        "The optional local AI endpoint uses Ollama when configured."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)

@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Welcome to the Student Management API.",
        "docs": "/docs",
        "health": "/health",
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
