"""Main FastAPI application module."""
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.orchestrator import OrchestratorService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Multi-Database Orchestrator",
    description="A service for querying multiple databases using natural language",
    version="1.0.0"
)

# Add CORS middleware
origins = [
    "http://localhost:3000",      # Next.js development server
    "http://localhost:3001",      # Alternative Next.js port
    "http://127.0.0.1:3000",     # Alternative local address
    "http://127.0.0.1:3001",     # Alternative local address port 3001
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,      # Set to False since we're not using session cookies
    allow_methods=["*"],         # Allow all methods
    allow_headers=["*"],         # Allow all headers
)

# Create orchestrator service instance
orchestrator = OrchestratorService()

@app.on_event("startup")
async def startup():
    """Initialize services on startup."""
    try:
        await orchestrator.init()
        logger.info("Services initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing services: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown."""
    try:
        await orchestrator.close()
        logger.info("Services shut down successfully")
    except Exception as e:
        logger.error(f"Error shutting down services: {e}")
        raise

from pydantic import BaseModel

class QueryRequest(BaseModel):
    text: str

@app.post("/query")
async def execute_query(query: QueryRequest) -> Dict[str, Any]:
    """Execute a natural language query across databases."""
    try:
        result = await orchestrator.handle_query(query.text)
        if not result.get('result'):
            # If no results found, return empty list but with context
            return {
                'result': [],
                'source': result.get('source', 'database'),
                'parsed_query': result.get('parsed_query'),
                'message': 'No results found for this query'
            }
        return result
    except ValueError as e:
        # Handle known errors with proper status codes
        logger.error(f"Invalid query: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log unexpected errors and return generic message
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your query. Please try again."
        )

@app.options("/query")
async def options_query():
    """Handle OPTIONS requests for the query endpoint."""
    return {}

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Middleware to add processing time header."""
    import time

    start_time = time.time()
    response: JSONResponse = await call_next(request)
    process_time = time.time() - start_time

    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Request: {request.url.path} completed in {process_time} sec")
    return response

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log request details."""
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.info(f"Headers: {request.headers}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
