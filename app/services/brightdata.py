from typing import List
from datetime import datetime
import json
import logging
import httpx
from app.core.models import Article

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
        sort: str = "newest",          # newest or relevance
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 1,
    ) -> str:
        """
        Trigger article collection by keywords and return snapshot ID

        Args:
            keywords: List of keywords to search
            limit: Number of articles per keyword

        Returns:
            str: Snapshot ID for the collection
        """
        keyword_params = [
            {
                "keyword": keyword,
                "sort": sort,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None,
            }
            for keyword in keywords
        ]

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/trigger",
                headers=self.headers,
                params={
                    "dataset_id": self.dataset_id,
                    "include_errors": "true",
                    "type": "discover_new",
                    "discover_by": "keyword",
                    "limit_per_input": limit,
                },
                json=keyword_params,
            )
            print(f"Trigger Response: {response.text}")
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
                    articles.append(Article(**article_data))
                except json.JSONDecodeError as e:
                    logging.warning(f"Failed to parse article data: {e}")
                    continue

        return articles
