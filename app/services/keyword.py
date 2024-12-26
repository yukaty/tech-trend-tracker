import logging
from typing import Tuple, List
from app.db.async_client import DatabaseClient
from app.core.models import Article

logger = logging.getLogger(__name__)

async def search_by_keyword(
    keyword: str,
    limit: int,
    offset: int,
) -> Tuple[List[Article], int]:
    """Search for articles by keyword"""
    try:
        db = DatabaseClient()
        await db.connect()

        logger.info(f"Searching with keyword: {keyword}, limit: {limit}, offset: {offset}")

        sql = """
            SELECT
                id,
                url,
                headline,
                description,
                publication_date,
                source
            FROM articles
            WHERE
                content ILIKE $1
                OR headline ILIKE $1
                OR keyword ILIKE $1
            ORDER BY publication_date DESC
            LIMIT $2 OFFSET $3
        """

        total_sql = """
            SELECT COUNT(*)
            FROM articles
            WHERE
                content ILIKE $1
                OR headline ILIKE $1
                OR keyword ILIKE $1
        """

        search_pattern = f"%{keyword}%"
        rows = await db.fetch(sql, search_pattern, limit, offset)
        total = await db.fetch_val(total_sql, search_pattern)

        articles = [Article(**dict(row)) for row in rows]
        logger.info(f"Found {len(articles)} articles out of {total} total for pattern: {search_pattern}")

        if len(articles) == 0 and total > 0:
            logger.warning(f"No articles returned despite having {total} matches. Check LIMIT/OFFSET values.")

        return articles, total

    except Exception as e:
        logger.error(f"Error in search_by_keyword: {e}")
        raise
    finally:
        await db.close()