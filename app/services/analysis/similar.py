import logging
from typing import Tuple, List
from app.db.async_client import DatabaseClient
from app.services.embedding import get_embedding_async
from app.core.models import SimilarArticle

logger = logging.getLogger(__name__)

async def find_similar_articles(
    query: str,
    limit: int,
    offset: int,
) -> Tuple[List[SimilarArticle], int]:
    """Find similar articles based on the query"""
    try:
        # Get embedding and prepare DB connection
        embedding = await get_embedding_async(query)
        vector_str = f"[{','.join(map(str, embedding))}]"

        db = DatabaseClient()
        await db.connect()

        # Debug the actual SQL and parameters
        sql = """
            SELECT
                id, headline, description, url,
                publication_date, source, topics,
                1 - (embedding <=> $1::vector) as similarity_score
            FROM articles
            ORDER BY similarity_score DESC
            LIMIT $2 OFFSET $3
        """
        logger.debug(f"Executing query with params: {vector_str}, {limit}, {offset}")

        # Execute query
        rows = await db.fetch(sql, vector_str, limit, offset)
        total_sql = """
            SELECT COUNT(*) FROM (
                SELECT id FROM articles
                ORDER BY 1 - (embedding <=> $1::vector) DESC
            ) AS similar_articles
        """
        total = await db.fetch_val(total_sql, vector_str)

        articles = [SimilarArticle(**dict(row)) for row in rows]

        logger.info(f"Found {len(articles)} similar articles out of {total} total")
        return articles, total

    except Exception as e:
        logger.error(f"Error in find_similar_articles: {e}")
        raise

    finally:
        await db.close()