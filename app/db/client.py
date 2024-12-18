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

    async def save_article(self, article):
        """Save article to database"""
        if not self.pool:
            await self.connect()

        # Convert RelatedArticle list to json
        related_articles_json = json.dumps([ra.model_dump() for ra in article.related_articles]) if article.related_articles else None

        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO articles (
                    id, url, headline, description, content,
                    topics, publication_date, updated_last,
                    source, related_articles, keyword
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                ON CONFLICT (id) DO UPDATE SET
                    updated_last = EXCLUDED.updated_last,
                    content = EXCLUDED.content
            ''', article.id, article.url, article.headline,
                article.description, article.content,
                article.topics, article.publication_date,
                article.updated_last, article.source,
                related_articles_json, article.keyword
            )

    async def close(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()