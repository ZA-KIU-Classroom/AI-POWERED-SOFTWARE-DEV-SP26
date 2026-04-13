"""
FastAPI AI Scaffold — CS-AI-2025 Lab 5, Spring 2026
One working AI-powered endpoint to start your prototype sprint.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import ai_router

app = FastAPI(
    title="Capstone API",
    description="AI-powered capstone prototype — CS-AI-2025 Spring 2026",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router.router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
