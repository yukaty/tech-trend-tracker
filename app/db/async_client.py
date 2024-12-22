import asyncpg
import os
import json
from urllib.parse import urlparse

class DatabaseClient:
    def __init__(self):
        self.pool = None
        db_url = urlparse(os.getenv('DATABASE_URL'))
        self.config = {
            'user': db_url.username,
            'password': db_url.password,
            'database': db_url.path[1:],
            'host': db_url.hostname,
            'port': db_url.port
        }

    async def connect(self):
        """Initialize database connection pool"""
        self.pool = await asyncpg.create_pool(**self.config)
        if not self.pool:
            raise Exception("Failed to create database connection pool")

    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()

    async def fetch(self, query: str, *args):
        """Execute a query and return all results"""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetch_val(self, query: str, *args):
        """Execute a query and return a single value"""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)