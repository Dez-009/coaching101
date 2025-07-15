import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict
from app.core.config import Settings
from app.services.orchestrator import OrchestratorService
from app.services.nl_service import NLService
from app.services.db_service import DatabaseService

# Create test settings
@pytest.fixture
def test_settings():
    return Settings(
        REDIS_HOST="localhost",
        REDIS_PORT=6379,
        REDIS_PASSWORD=None,
        OPENAI_API_KEY="test-key",
        POSTGRES_HOST="localhost",
        MONGO_URI="mongodb://localhost:27017",
        MYSQL_HOST="localhost",
        ES_HOST="localhost"
    )

import pytest_asyncio

@pytest_asyncio.fixture
async def orchestrator_service(test_settings):
    with patch("app.core.config.get_settings", return_value=test_settings):
        service = OrchestratorService()
        service.db_service = Mock()
        service.nl_service = Mock()
        # Make async methods into AsyncMocks
        service.db_service.query_postgres = AsyncMock()
        service.db_service.query_mongo = AsyncMock()
        service.db_service.query_mysql = AsyncMock()
        service.db_service.search_es = AsyncMock()
        service.db_service.cache_get = AsyncMock()
        service.db_service.cache_set = AsyncMock()
        service.nl_service.parse_query = AsyncMock()
        service.nl_service.detect_intent = AsyncMock()
        service.nl_service.validate_query = AsyncMock()
        service.nl_service.optimize_query = AsyncMock()
        return service

@pytest.mark.asyncio
async def test_postgres_query_success(orchestrator_service):
    """Test successful PostgreSQL query execution"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "postgres",
        "fields": ["id", "name"],
        "table": "users",
        "filters": "age > 18",
        "sort": "name ASC",
        "limit": 10
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    orchestrator_service.nl_service.optimize_query.return_value = {
        "target_db": "postgres",
        "fields": ["id", "name"],
        "table": "users",
        "filters": "age > 18",
        "sort": "name ASC",
        "limit": 10
    }
    
    # Mock database response
    mock_results = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
    orchestrator_service.db_service.query_postgres.return_value = mock_results

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show all users over 18"})

    # Verify success
    assert result["success"] is True
    assert len(result["results"]) == 1
    assert result["results"][0]["database"] == "postgres"
    assert result["results"][0]["table"] == "users"
    assert result["results"][0]["data"] == mock_results
    assert result["results"][0]["count"] == 2

@pytest.mark.asyncio
async def test_mongo_query_success(orchestrator_service):
    """Test successful MongoDB query execution"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "mongo",
        "collection": "sessions",
        "filters": {"active": True}
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    orchestrator_service.nl_service.optimize_query.return_value = {
        "target_db": "mongo",
        "collection": "sessions",
        "filters": {"active": True}
    }
    
    # Mock database response
    mock_results = [{"_id": "123", "user_id": "456", "active": True}]
    orchestrator_service.db_service.query_mongo.return_value = mock_results

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show active sessions"})

    # Verify success
    assert result["success"] is True
    assert len(result["results"]) == 1
    assert result["results"][0]["database"] == "mongo"
    assert result["results"][0]["table"] == "sessions"
    assert result["results"][0]["data"] == mock_results
    assert result["results"][0]["count"] == 1

@pytest.mark.asyncio
async def test_mysql_query_success(orchestrator_service):
    """Test successful MySQL query execution"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "mysql",
        "fields": ["id", "title"],
        "table": "journals",
        "filters": "created_at > '2025-01-01'"
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    orchestrator_service.nl_service.optimize_query.return_value = {
        "target_db": "mysql",
        "fields": ["id", "title"],
        "table": "journals",
        "filters": "created_at > '2025-01-01'"
    }
    
    # Mock database response
    mock_results = [{"id": 1, "title": "Journal Entry 1"}]
    orchestrator_service.db_service.query_mysql.return_value = mock_results

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show journals from 2025"})

    # Verify success
    assert result["success"] is True
    assert len(result["results"]) == 1
    assert result["results"][0]["database"] == "mysql"
    assert result["results"][0]["table"] == "journals"
    assert result["results"][0]["data"] == mock_results
    assert result["results"][0]["count"] == 1

@pytest.mark.asyncio
async def test_elasticsearch_query_success(orchestrator_service):
    """Test successful Elasticsearch query execution"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "elasticsearch",
        "index": "search_logs",
        "filters": [{"match": {"level": "error"}}]
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    orchestrator_service.nl_service.optimize_query.return_value = {
        "target_db": "elasticsearch",
        "index": "search_logs",
        "filters": [{"match": {"level": "error"}}]
    }
    
    # Mock database response
    mock_results = [{"timestamp": "2025-07-14", "level": "error", "message": "Test error"}]
    orchestrator_service.db_service.search_es.return_value = mock_results

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show error logs"})

    # Verify success
    assert result["success"] is True
    assert len(result["results"]) == 1
    assert result["results"][0]["database"] == "elasticsearch"
    assert result["results"][0]["table"] == "search_logs"
    assert result["results"][0]["data"] == mock_results
    assert result["results"][0]["count"] == 1

@pytest.mark.asyncio
async def test_cache_hit(orchestrator_service):
    """Test successful cache hit"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "postgres",
        "fields": ["id", "name"],
        "table": "users"
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    
    # Mock cache hit
    mock_cached_results = [{"id": 1, "name": "John"}]
    orchestrator_service.db_service.cache_get.return_value = json.dumps(mock_cached_results)

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show all users"})

    # Verify cache hit
    assert result["success"] is True
    assert result.get("from_cache") is True
    assert result["results"] == mock_cached_results

@pytest.mark.asyncio
async def test_database_error(orchestrator_service):
    """Test database error handling"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "postgres",
        "fields": ["id", "name"],
        "table": "users"
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    orchestrator_service.nl_service.optimize_query.return_value = {
        "target_db": "postgres",
        "fields": ["id", "name"],
        "table": "users"
    }
    
    # Mock database error
    orchestrator_service.db_service.query_postgres.side_effect = Exception("Database connection failed")

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show all users"})

    # Verify error handling
    assert result["success"] is False
    assert "Database execution error" in result["error"]
    assert result["results"] == []

@pytest.mark.asyncio
async def test_invalid_database_type(orchestrator_service):
    """Test handling of invalid database type"""
    # Mock responses with invalid database type
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "invalid_db",
        "fields": ["id", "name"],
        "table": "users"
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    orchestrator_service.nl_service.validate_query.return_value = []
    orchestrator_service.nl_service.optimize_query.return_value = {
        "target_db": "invalid_db",
        "fields": ["id", "name"],
        "table": "users"
    }

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show all users"})

    # Verify error handling
    assert result["success"] is False
    assert "Unsupported database type" in result["error"]
    assert result["results"] == []

@pytest.mark.asyncio
async def test_empty_query(orchestrator_service):
    """Test handling of empty query"""
    # Execute query with empty string
    result = await orchestrator_service.handle_query({"query": ""})

    # Verify error handling
    assert result["success"] is False
    assert "No query provided" in result["error"]
    assert result["results"] == []

@pytest.mark.asyncio
async def test_validation_error(orchestrator_service):
    """Test query validation error handling"""
    # Mock responses
    orchestrator_service.nl_service.parse_query.return_value = {
        "target_db": "postgres",
        "fields": ["id", "name"],
        "table": "users"
    }
    orchestrator_service.nl_service.detect_intent.return_value = "SEARCH"
    # Mock validation error
    orchestrator_service.nl_service.validate_query.return_value = ["Invalid table name", "Missing required field"]

    # Execute query
    result = await orchestrator_service.handle_query({"query": "Show all users"})

    # Verify error handling
    assert result["success"] is False
    assert "Validation failed" in result["error"]
    assert "Invalid table name" in result["error"]
    assert "Missing required field" in result["error"]
    assert result["results"] == []
