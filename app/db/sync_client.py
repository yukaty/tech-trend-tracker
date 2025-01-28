import os
import json
import logging
import psycopg
from typing import List
from app.core.models import Article
from app.services.chunker import ArticleChunker

logger = logging.getLogger(__name__)

def save_articles(articles: List[Article]) -> None:
    """Save articles to database synchronously"""
    db_url = os.getenv('DATABASE_URL')
    chunker = ArticleChunker()

    success_count = 0
    error_count = 0

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            for article in articles:
                try:
                    # Save article
                    cur.execute('''
                        INSERT INTO articles (
                            id, url, headline, description,
                            publication_date, source
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    ''', (
                        article.id, article.url, article.headline,
                        article.description, article.publication_date,
                        article.source
                    ))

                    # Convert metadata to JSON because psycopg doesn't support JSONB
                    metadata = json.dumps({
                        'headline': article.headline,
                        'publication_date': article.publication_date.isoformat() if article.publication_date else None
                    })

                    # Create chunks from article and save them
                    chunks = chunker.create_chunks(article.content)
                    for i, chunk_text in enumerate(chunks):
                        cur.execute('''
                            INSERT INTO article_chunks (
                                id, article_id, chunk_text,
                                chunk_index, metadata
                            ) VALUES (
                                gen_random_uuid(), %s, %s, %s, %s
                            )
                        ''', (
                            article.id, chunk_text, i, metadata
                        ))

                    success_count += 1
                    logger.info(f"✓ Saved article and chunks: {article.id}")
                except Exception as e:
                    error_count +=1
                    logger.error(f"Failed to save {article.id}: {e}")

            conn.commit()

    logger.info(f"Saved {success_count}/{len(articles)} articles ({error_count} failed)")