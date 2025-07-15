# FastAPI entry point for orchestrator service
from fastapi import FastAPI
from .routes import orchestrator

app = FastAPI(title="Admin Orchestrator API")

app.include_router(orchestrator.router, prefix="/orchestrator", tags=["orchestrator"])

@app.get("/")
def read_root():
    return {"message": "Admin Orchestrator running"}
