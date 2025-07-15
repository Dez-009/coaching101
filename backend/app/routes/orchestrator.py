# API routes for orchestrator endpoints
from fastapi import APIRouter, Depends
from ..services.orchestrator import OrchestratorService
from ..models.schema import QueryRequest, QueryResponse

router = APIRouter(
    prefix="/orchestrator",
    tags=["orchestrator"],
    responses={404: {"description": "Not found"}},
)

service = OrchestratorService()

def get_service():
    return service

@router.post("/query", response_model=QueryResponse)
async def execute_query(req: QueryRequest, svc: OrchestratorService = Depends(get_service)) -> QueryResponse:
    """Accepts a natural language query and returns structured results."""
    return await svc.handle_query(req.dict())
