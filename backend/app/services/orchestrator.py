"""Query orchestrator service."""
from typing import Dict, List, Any
import hashlib
import json
from datetime import datetime
import logging

from .database import DatabaseService
from .nl_service import NLService

logger = logging.getLogger(__name__)

class OrchestratorService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.nl_service = NLService()

    async def init(self):
        """Initialize services."""
        await self.db_service.init()

    async def close(self):
        """Close services."""
        await self.db_service.close()

    async def handle_query(self, query: str) -> Dict[str, Any]:
        """Handle a natural language query."""
        # Parse the natural language query
        parsed_query = await self.nl_service.parse_query(query)
        
        # Generate cache key based on the parsed query to avoid caching similar but different queries
        cache_key = self._generate_cache_key(str(parsed_query))
        
        # Try to get from cache first
        cached_result = await self.db_service.get_cache(cache_key)
        if cached_result:
            return {
                'result': cached_result,
                'source': 'cache',
                'parsed_query': parsed_query
            }

        # Execute the query
        result = await self.execute_query(parsed_query)
        
        # Cache the result
        await self.db_service.set_cache(cache_key, result)
        
        return {
            'result': result,
            'source': 'database',
            'parsed_query': parsed_query
        }

    def _generate_cache_key(self, query: str) -> str:
        """Generate a cache key for a query."""
        return hashlib.md5(query.encode()).hexdigest()

    async def execute_query(self, parsed_query: Dict) -> List[Dict]:
        """Execute a parsed query on the appropriate database."""
        logger.info(f"Executing parsed query: {parsed_query}")
        target_db = parsed_query['target_db']
        operation = parsed_query['operation']
        conditions = parsed_query['conditions']

        if target_db == 'postgres':
            # Convert conditions to SQL
            where_clause = self._build_postgres_where(conditions)
            query = f"SELECT * FROM users {where_clause}"
            logger.info(f"Generated SQL query: {query}")
            return await self.db_service.query_postgres(query)

        elif target_db == 'mongo':
            # Convert conditions to MongoDB query
            mongo_query = self._build_mongo_query(conditions)
            logger.info(f"Generated MongoDB query: {mongo_query}")
            return await self.db_service.query_mongo('sessions', mongo_query)

        elif target_db == 'mysql':
            # Convert conditions to MySQL query
            where_clause = self._build_mysql_where(conditions)
            query = f"SELECT * FROM journals {where_clause}"
            logger.info(f"Generated MySQL query: {query}")
            return await self.db_service.query_mysql(query)

        elif target_db == 'elasticsearch':
            # Convert conditions to Elasticsearch query
            es_query = self._build_es_query(conditions)
            logger.info(f"Generated Elasticsearch query: {es_query}")
            return await self.db_service.search_es('documents', es_query)

        raise ValueError(f"Unsupported database: {target_db}")

    def _build_postgres_where(self, conditions: Dict) -> str:
        """Build a WHERE clause for PostgreSQL."""
        logger.info(f"Building WHERE clause from conditions: {conditions}")
        
        if not conditions:
            logger.info("No conditions provided, returning empty WHERE clause")
            return ""
            
        clauses = []
        # Skip 'object' if it's 'users' since that's the table name
        if 'subject' in conditions:
            clauses.append(f"username = '{conditions['subject']}'")
        if 'object' in conditions and conditions['object'] != 'users':
            clauses.append(f"role = '{conditions['object']}'")
        if 'role' in conditions:
            clauses.append(f"role = '{conditions['role']}'")
            
        where_clause = "WHERE " + " AND ".join(clauses) if clauses else ""
        logger.info(f"Generated WHERE clause: {where_clause}")
        return where_clause

    def _build_mongo_query(self, conditions: Dict) -> Dict:
        """Build a MongoDB query."""
        query = {}
        if 'subject' in conditions:
            query['user_id'] = conditions['subject']
        if 'object' in conditions:
            query['type'] = conditions['object']
        return query

    def _build_mysql_where(self, conditions: Dict) -> str:
        """Build a WHERE clause for MySQL."""
        if not conditions:
            return ""
            
        clauses = []
        if 'subject' in conditions:
            clauses.append(f"author = '{conditions['subject']}'")
        if 'object' in conditions:
            clauses.append(f"category = '{conditions['object']}'")
            
        return "WHERE " + " AND ".join(clauses) if clauses else ""

    def _build_es_query(self, conditions: Dict) -> Dict:
        """Build an Elasticsearch query."""
        must_clauses = []
        if 'subject' in conditions:
            must_clauses.append({"match": {"author": conditions['subject']}})
        if 'object' in conditions:
            must_clauses.append({"match": {"content": conditions['object']}})
            
        return {
            "query": {
                "bool": {
                    "must": must_clauses or [{"match_all": {}}]
                }
            }
        }
