import logging
from typing import List, Tuple
from app.db.async_client import DatabaseClient
from app.core.models import Article, ChunkWithScore

logger = logging.getLogger(__name__)

async def find_relevant_chunks_with_articles(
    query_embedding: list,
    limit: int,
    offset: int
) -> List[Tuple[ChunkWithScore, Article]]:
    """
    Find most relevant chunks and their corresponding articles
    using vector similarity search
    """
    try:
        db = DatabaseClient()
        await db.connect()

        vector_str = f"[{','.join(map(str, query_embedding))}]"
        logger.info(f"Query with vector size: {len(query_embedding)}")

        sql = """
            SELECT DISTINCT ON (a.id)
                c.chunk_text,
                c.article_id,
                1 - (c.chunk_embedding <=> $1::vector) as relevance_score,
                a.url,
                a.headline,
                a.description,
                a.publication_date,
                a.source
            FROM article_chunks c
            JOIN articles a ON c.article_id = a.id
            WHERE (c.chunk_embedding <=> $1::vector) < 0.8
            ORDER BY a.id, relevance_score DESC, a.publication_date DESC
            LIMIT $2 OFFSET $3;
        """

        rows = await db.fetch(sql, vector_str, limit, offset)
        logger.info(f"Found {len(rows)} results")


        return [(
            ChunkWithScore(
                chunk_text=row['chunk_text'],
                relevance_score=row['relevance_score']
            ),
            Article(
                id=row['article_id'],
                url=row['url'],
                headline=row['headline'],
                description=row['description'],
                publication_date=row['publication_date'],
                source=row['source']
            )
        ) for row in rows]

    except Exception as e:
        logger.error(f"Error in find_relevant_chunks: {e}")
        raise

    finally:
        await db.close()

async def get_total_relevant_articles(query_embedding: list) -> int:
    """Get total count of relevant articles for pagination"""
    try:
        db = DatabaseClient()
        await db.connect()

        vector_str = f"[{','.join(map(str, query_embedding))}]"

        sql = """
            SELECT COUNT(DISTINCT a.id)
            FROM article_chunks c
            JOIN articles a ON c.article_id = a.id
            WHERE (c.chunk_embedding <=> $1::vector) < 0.8
        """

        total = await db.fetch_val(sql, vector_str)
        return total

    except Exception as e:
        logger.error(f"Error in get_total_relevant_articles: {e}")
        raise

    finally:
        await db.close()