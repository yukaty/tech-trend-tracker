import logging
from typing import List, Optional, Dict
from app.db.async_client import DatabaseClient
from app.core.models import TrendingEntity

logger = logging.getLogger(__name__)

class TrendService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def _build_trend_query(self, condition: str) -> str:
        """Build common trend query with different conditions"""
        return f"""
            WITH monthly_counts AS (
                SELECT
                    e.name,
                    date_part('month', ae.publication_date) as month,
                    COUNT(*) as monthly_count
                FROM
                    entities e
                    JOIN article_entities ae ON e.name = ae.entity_name
                WHERE
                    {condition}
                GROUP BY
                    e.name, date_part('month', ae.publication_date)
            ),
            trends AS (
                SELECT
                    name,
                    SUM(monthly_count) as total_count,
                    100.0 * (
                        MAX(CASE WHEN month = 12 THEN monthly_count ELSE 0 END) -
                        MAX(CASE WHEN month = 1 THEN monthly_count ELSE 0 END)
                    ) / NULLIF(MAX(CASE WHEN month = 1 THEN monthly_count ELSE 0 END), 0) as trend
                FROM monthly_counts
                GROUP BY name
            )
            SELECT
                name,
                total_count as count,
                COALESCE(trend, 0) as trend
            FROM trends
            ORDER BY total_count DESC
            LIMIT 5;
        """

    def _build_monthly_query(self, condition: str) -> str:
        """Build common monthly query with different conditions"""
        return f"""
            WITH monthly_stats AS (
                SELECT
                    e.name,
                    COUNT(*) as count,
                    100.0 * (
                        COUNT(*) -
                        LAG(COUNT(*)) OVER (PARTITION BY e.name ORDER BY date_part('month', ae.publication_date))
                    ) / NULLIF(LAG(COUNT(*)) OVER (PARTITION BY e.name ORDER BY date_part('month', ae.publication_date)), 0) as trend,
                    date_part('month', ae.publication_date) as month
                FROM
                    entities e
                    JOIN article_entities ae ON e.name = ae.entity_name
                WHERE
                    {condition}
                GROUP BY
                    e.name, date_part('month', ae.publication_date)
            )
            SELECT
                name,
                count,
                COALESCE(trend, 0) as trend
            FROM monthly_stats
            ORDER BY count DESC
            LIMIT 5;
        """

    async def _get_trends(self, query: str, *args) -> List[TrendingEntity]:
        """Execute query and return trending entities"""
        records = await self.db.fetch(query, *args)
        return [TrendingEntity(**dict(record)) for record in records]

    async def get_trending_entities(self, category: str, year: int, month: Optional[int] = None) -> List[TrendingEntity]:
        base_condition = f"e.type = $1 AND date_part('year', ae.publication_date) = $2"

        if month is None:
            query = self._build_trend_query(base_condition)
            return await self._get_trends(query, category, year)

        query = self._build_monthly_query(f"{base_condition} AND date_part('month', ae.publication_date) = $3")
        return await self._get_trends(query, category, year, month)

    async def get_trending_keywords(self, year: int, month: Optional[int] = None) -> List[TrendingEntity]:
        base_condition = f"date_part('year', ae.publication_date) = $1"

        if month is None:
            query = self._build_trend_query(base_condition)
            return await self._get_trends(query, year)

        query = self._build_monthly_query(f"{base_condition} AND date_part('month', ae.publication_date) = $2")
        return await self._get_trends(query, year, month)
