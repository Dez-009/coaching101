# Pydantic models for requests and responses
from pydantic import BaseModel
from typing import Any, List

class QueryRequest(BaseModel):
    """Incoming query from frontend or other services."""
    user_id: str
    query: str

class QueryResult(BaseModel):
    database: str
    table: str
    data: List[Any]
    count: int
    execution_time: float
    from_cache: bool

class QueryResponse(BaseModel):
    """Structured response returned to clients."""
    success: bool
    results: List[QueryResult]
    error: str | None = None
