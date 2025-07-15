"""Database service module for handling multi-database connections."""
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncpg
from motor.motor_asyncio import AsyncIOMotorClient
import aiomysql
from elasticsearch import AsyncElasticsearch
from redis.asyncio import Redis
import json

class DatabaseService:
    def __init__(self):
        self._postgres_pool = None
        self._mongo_client = None
        self._mysql_pool = None
        self._es_client = None
        self._redis_client = None

    async def init(self):
        """Initialize all database connections."""
        # Initialize PostgreSQL connection pool
        self._postgres_pool = await asyncpg.create_pool(
            user='postgres',
            password='postgres',
            database='admin_db',
            host='localhost',
            port=5433
        )

        # Initialize MongoDB client
        self._mongo_client = AsyncIOMotorClient('mongodb://localhost:27017')
        self._mongo_db = self._mongo_client['admin_sessions']

        # Initialize MySQL pool
        self._mysql_pool = await aiomysql.create_pool(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            db='journals'
        )

        # Initialize Elasticsearch client
        self._es_client = AsyncElasticsearch(
            hosts=['http://localhost:9200']
        )

        # Initialize Redis client
        self._redis_client = Redis.from_url('redis://localhost:6379')

    async def close(self):
        """Close all database connections."""
        if self._postgres_pool:
            await self._postgres_pool.close()
        if self._mongo_client:
            self._mongo_client.close()
        if self._mysql_pool:
            self._mysql_pool.close()
            await self._mysql_pool.wait_closed()
        if self._es_client:
            await self._es_client.close()
        if self._redis_client:
            await self._redis_client.close()

    async def query_postgres(self, query: str, *args) -> List[Dict]:
        """Execute a PostgreSQL query."""
        async with self._postgres_pool.acquire() as conn:
            records = await conn.fetch(query, *args)
            return [self._serialize_record(dict(r)) for r in records]

    def _serialize_record(self, record: Dict) -> Dict:
        """Convert record values to JSON-serializable format."""
        for key, value in record.items():
            if isinstance(value, datetime):
                record[key] = value.isoformat() if value else None
        return record

    async def query_mongo(self, collection: str, filter_dict: Dict) -> List[Dict]:
        """Execute a MongoDB query."""
        cursor = self._mongo_db[collection].find(filter_dict)
        return await cursor.to_list(length=None)

    async def query_mysql(self, query: str, *args) -> List[Dict]:
        """Execute a MySQL query."""
        async with self._mysql_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, args)
                return await cur.fetchall()

    async def search_es(self, index: str, query: Dict) -> List[Dict]:
        """Execute an Elasticsearch query."""
        result = await self._es_client.search(index=index, body=query)
        return [hit['_source'] for hit in result['hits']['hits']]

    async def get_cache(self, key: str) -> Optional[Any]:
        """Get data from Redis cache."""
        data = await self._redis_client.get(key)
        return json.loads(data) if data else None

    async def set_cache(self, key: str, value: Any, expire: int = 3600):
        """Set data in Redis cache."""
        await self._redis_client.set(
            key,
            json.dumps(value),
            ex=expire
        )
