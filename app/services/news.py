import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import List
import os
from dotenv import load_dotenv

from app.services.brightdata import BrightDataClient
from app.core.models import Article
from app.db.client import DatabaseClient
from app.core import config

# Configure logging
logging.basicConfig(level=logging.INFO,)
logger = logging.getLogger(__name__)

async def collect_tech_news(
    keywords: List[str] = None,
    days: int = 7,
    articles_per_batch: int = 10
) -> List[Article]:
    """
    Collect technology articles using Bright Data API
    """
    load_dotenv()
    api_key = os.getenv("BRIGHTDATA_API_KEY")
    client = BrightDataClient(api_key=api_key)

    search_keywords = config.TECH_KEYWORDS
    print(search_keywords)
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    print(f"start: ${start_date}")
    print(f"end: ${end_date}")

    try:
        # Initialize collection
        snapshot_id = await client.collect_by_keywords(
            keywords=search_keywords,
            start_date=start_date,
            end_date=end_date,
            limit=articles_per_batch
        )
        logger.info(f"Collection started: {snapshot_id}")

        # Wait for completion
        while True:
            status = await client.get_collection_status(snapshot_id)
            if status == "ready":
                break
            if status == "failed":
                raise Exception("Collection failed")
            await asyncio.sleep(15)

        # For TEST
        # snapshot_id = "s_m4u5l1vu2q2wqcirp3"

        # Retrieve articles
        articles = await client.get_articles(snapshot_id)
        logger.info(f"Retrieved {len(articles)} articles")
        return articles

    except Exception as e:
        logger.error(f"Error during collection: {e}")
        raise

async def fetch_and_save_news(
    keywords: List[str] = None,
    days: int = 7,
    articles_per_batch: int = 10
):
    """News collection main function"""
    db = DatabaseClient()

    try:
        articles = await collect_tech_news(
            keywords=keywords,
            days=days,
            articles_per_batch=articles_per_batch
        )
        await db.connect()
        for article in articles:
            try:
                await db.save_article(article)
                logger.info(f"✓ Saved: {article.headline}")
            except Exception as e:
                logger.error(f"Failed to save {article.headline}: {e}")

    finally:
        await db.close()