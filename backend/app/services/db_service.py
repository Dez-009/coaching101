from typing import Any, Dict, List
import asyncpg
import motor.motor_asyncio
import aiomysql
import redis.asyncio as redis
from elasticsearch import AsyncElasticsearch
from ..core.config import get_settings

settings = get_settings()

class DatabaseService:
    def __init__(self):
        self.pg_pool = None
        self.mongo_client = None
        self.mysql_pool = None
        self.redis_client = None
        self.es_client = None

    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    async def connect(self):
        # PostgreSQL connection
        self.pg_pool = await asyncpg.create_pool(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB
        )

        # MongoDB connection
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
        self.mongo_db = self.mongo_client[settings.MONGO_DB]

        # MySQL connection
        self.mysql_pool = await aiomysql.create_pool(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            user=settings.MYSQL_USER,
            password=settings.MYSQL_PASSWORD,
            db=settings.MYSQL_DB
        )

        # Redis connection
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            decode_responses=True
        )

        # Elasticsearch connection
        self.es_client = AsyncElasticsearch(
            hosts=[f"http://{settings.ES_HOST}:{settings.ES_PORT}"],
            basic_auth=(settings.ES_USER, settings.ES_PASSWORD) if settings.ES_USER else None
        )

    async def disconnect(self):
        if self.pg_pool:
            await self.pg_pool.close()
        if self.mongo_client:
            self.mongo_client.close()
        if self.mysql_pool:
            self.mysql_pool.close()
        if self.redis_client:
            await self.redis_client.close()
        if self.es_client:
            await self.es_client.close()

    async def query_postgres(self, query: str, params: List[Any] = None) -> List[Dict]:
        async with self.pg_pool.acquire() as conn:
            result = await conn.fetch(query, *params) if params else await conn.fetch(query)
            return [dict(row) for row in result]

    async def query_mongo(self, collection: str, query: Dict) -> List[Dict]:
        cursor = self.mongo_db[collection].find(query)
        return await cursor.to_list(length=None)

    async def query_mysql(self, query: str, params: tuple = None) -> List[Dict]:
        async with self.mysql_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(query, params)
                return await cur.fetchall()

    async def cache_get(self, key: str) -> Any:
        return await self.redis_client.get(key)

    async def cache_set(self, key: str, value: Any, expire: int = 3600) -> None:
        await self.redis_client.set(key, value, ex=expire)

    async def search_es(self, index: str, query: Dict) -> List[Dict]:
        result = await self.es_client.search(index=index, body=query)
        return [hit["_source"] for hit in result["hits"]["hits"]]
