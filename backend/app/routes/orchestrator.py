# API routes for orchestrator endpoints
from fastapi import APIRouter, Depends
from ..services.orchestrator import OrchestratorService
from ..models.schema import QueryRequest, QueryResponse

router = APIRouter()

service = OrchestratorService()

def get_service():
    return service

@router.post("/query", response_model=QueryResponse)
def execute_query(req: QueryRequest, svc: OrchestratorService = Depends(get_service)):
    """Accepts a natural language query and returns structured results."""
    return svc.handle_query(req)
