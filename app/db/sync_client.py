import os
import json
import logging
import psycopg
from typing import List
from app.core.models import Article

logger = logging.getLogger(__name__)

def save_articles(articles: List[Article]) -> None:
    """Save articles to database synchronously"""
    db_url = os.getenv('DATABASE_URL')
    success_count = 0
    error_count = 0

    with psycopg.connect(db_url) as conn:
        with conn.cursor() as cur:
            for article in articles:
                try:
                    # Convert RelatedArticle list to json
                    related_articles_json = json.dumps([ra.model_dump() for ra in article.related_articles]) if article.related_articles else None

                    cur.execute('''
                        INSERT INTO articles (
                            id, url, headline, description, content,
                            topics, publication_date, updated_last,
                            source, related_articles, keyword
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO UPDATE SET
                            updated_last = EXCLUDED.updated_last,
                            content = EXCLUDED.content
                    ''', (
                        article.id, article.url, article.headline,
                        article.description, article.content,
                        article.topics, article.publication_date,
                        article.updated_last, article.source,
                        related_articles_json, article.keyword
                    ))
                    success_count += 1
                    logger.info(f"✓ Saved: {article.id}:{article.headline}")
                except Exception as e:
                    error_count +=1
                    logger.error(f"Failed to save {article.id}: {e}")

            conn.commit()

    logger.info(f"Saved {success_count}/{len(articles)} articles ({error_count} failed)")