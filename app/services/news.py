import asyncio, logging, os
from datetime import datetime, timezone, timedelta
from typing import List, Tuple

from app.services.brightdata import BrightDataClient
from app.core.models import Article
from app.core import config

logger = logging.getLogger(__name__)

def parse_date_range(
    start_date: str = None,
    end_date: str = None
) -> Tuple[datetime, datetime]:
    """Parse date range from YYYYMMDD strings to datetime objects

    Args:
        start_date: Optional start date in YYYYMMDD format
        end_date: Optional end date in YYYYMMDD format

    Returns:
        Tuple of (start_datetime, end_datetime) in UTC
        Start time will be set to 00:00:00
        End time will be set to 23:59:59
        If dates are not provided, returns range of last 7 days
    """
    if end_date:
        end_dt = datetime.strptime(f"{end_date}235959", "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    else:
        end_dt = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59)

    if start_date:
        start_dt = datetime.strptime(f"{start_date}000000", "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    else:
        start_dt = end_dt.replace(hour=0, minute=0, second=0) - timedelta(7)

    logger.debug(f"Start date: {start_dt}")
    logger.debug(f"End date: {end_dt}")
    return start_dt, end_dt

async def collect_tech_news(
    start_date: str = None,  # YYYYMMDD format
    end_date: str = None,    # YYYYMMDD format
    articles_per_keyword: int = None
) -> List[Article]:
    """Collect technology news using Bright Data API"""
    client = BrightDataClient(api_key=os.getenv("BRIGHTDATA_API_KEY"))

    # Handle date parameters
    start_dt, end_dt = parse_date_range(start_date, end_date)

    try:
        # Start collection and get snapshot ID
        snapshot_id = await client.collect_by_keywords(
            keywords=config.TECH_KEYWORDS,
            start_date=start_dt.isoformat(),
            end_date=end_dt.isoformat(),
            limit=articles_per_keyword
        )
        logger.info(f"Collection started: snapshot_id[{snapshot_id}]")

        # Poll until ready
        while True:
            status = await client.get_collection_status(snapshot_id)
            logger.info(f"Polling... status[{status}]")
            if status == "ready":
                break
            if status == "failed":
                raise Exception("Collection failed")
            await asyncio.sleep(15)

        # Retrieve articles
        articles = await client.get_articles(snapshot_id)
        logger.info(f"Retrieved {len(articles)} articles")

        return articles

    except Exception as e:
        logger.error(f"Error during collection: {e}")
        raise
