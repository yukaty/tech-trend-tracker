import os, logging, httpx, json
from typing import List
from app.core.models import Article

logger = logging.getLogger(__name__)

class BrightDataClient:
    """Client for interacting with Bright Data's Web Scraper API"""

    def __init__(self, api_key: str, dataset_id: str = "gd_lyptx9h74wtlvpnfu"):
        self.api_key = api_key
        self.dataset_id = dataset_id
        self.base_url = "https://api.brightdata.com/datasets/v3"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    async def collect_by_keywords(
        self,
        keywords: List[str],
        start_date: str = None,
        end_date: str = None,
        limit: int = None,
    ) -> str:
        """Trigger article collection by keywords and return snapshot ID"""
        # Prepare request body
        keyword_params = [
            {
                "keyword": keyword,
                "start_date": start_date,
                "end_date": end_date,
            }
            for keyword in keywords
        ]

        # Prepare request params
        params = {
            "dataset_id": self.dataset_id,
            "include_errors": "true",
            "type": "discover_new",
            "discover_by": "keyword",
        }
        if limit:
            params["limit_per_input"] = limit

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/trigger",
                headers=self.headers,
                params=params,
                json=keyword_params,
            )
            response.raise_for_status()
            data = response.json()
            return data["snapshot_id"]

    async def get_collection_status(self, snapshot_id: str) -> str:
        """
        Get the status of a specific snapshot
        Returns: Status string ('ready', 'running', or 'failed')
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/progress/{snapshot_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()["status"]


    async def get_articles(self, snapshot_id: str) -> List[Article]:
        """Retrieve collected article data"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/snapshot/{snapshot_id}",
                headers=self.headers
            )
            response.raise_for_status()

        articles = []
        for line in response.text.strip().split('\n'):
            if line.strip():
                try:
                    article_data = json.loads(line)

                    if article_data.get("error_code") == "crawl_failed":
                        logger.warning(f"Skipping failed article: {article_data}")
                        continue

                    articles.append(Article(**article_data))

                except json.JSONDecodeError as e:
                    logger.warning(f"Failed to parse article data: {e}")
                    continue

                except ValidationError as e:
                    logger.warning(f"Invalid article data: {e}")
                    continue

        return articles
