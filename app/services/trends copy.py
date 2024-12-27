import logging
from typing import List, Optional, Dict
from app.db.async_client import DatabaseClient
from app.core.models import TrendingEntity

logger = logging.getLogger(__name__)

class TrendService:
    def __init__(self, db: DatabaseClient):
        self.db = db

    def _build_trend_query(self, condition: str) -> str:
        """Build trend query with different conditions"""
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
                    {condition} AND
                    date_part('month', ae.publication_date) IN (1, 12)  -- January and December
                GROUP BY
                    e.name, date_part('month', ae.publication_date)
            ),
            trends AS (
                SELECT
                    name,
                    SUM(monthly_count) as total_count,
                    CASE
                        WHEN COUNT(DISTINCT month) = 2 THEN  -- Both January and December are present
                            ROUND(
                                100.0 * (
                                    MAX(CASE WHEN month = 12 THEN monthly_count END) -
                                    MAX(CASE WHEN month = 1 THEN monthly_count END)
                                ) / NULLIF(MAX(CASE WHEN month = 1 THEN monthly_count END), 0),
                                1
                            )
                        ELSE NULL -- trend score is NULL when either January or December is missing
                    END as trend
                FROM monthly_counts
                GROUP BY name
                HAVING SUM(monthly_count) > 0
            )
            SELECT
                name,
                total_count as count,
                trend
            FROM trends
            ORDER BY total_count DESC
            LIMIT 5;
        """

    def _build_monthly_query(self, condition: str) -> str:
        """Build monthly trend query with different conditions"""
        return f"""
            WITH monthly_stats AS (
                SELECT
                    e.name,
                    COUNT(*) AS current_count
                FROM
                    entities e
                    JOIN article_entities ae ON e.name = ae.entity_name
                WHERE
                    {condition}
                GROUP BY
                    e.name
            ),
            prev_month_stats AS (
                SELECT
                    e.name,
                    COUNT(*) AS prev_count
                FROM
                    entities e
                    JOIN article_entities ae ON e.name = ae.entity_name
                WHERE
                    e.type = $1
                    AND date_part('year', ae.publication_date) = $4
                    AND date_part('month', ae.publication_date) = $5
                GROUP BY
                    e.name
            )
            SELECT
                m.name,
                m.current_count AS count,
                CASE
                    WHEN p.prev_count > 0 THEN
                        ROUND(
                            100.0 * (m.current_count - p.prev_count) / p.prev_count,
                            1
                        )
                    ELSE NULL
                END AS trend
            FROM
                monthly_stats m
            LEFT JOIN
                prev_month_stats p ON m.name = p.name
            ORDER BY
                count DESC
            LIMIT 5;
        """

    async def _get_trends(self, query: str, *args) -> List[TrendingEntity]:
        """Execute query and return trending entities"""
        logger.info("Executing SQL Query:\n%s\nWith Parameters:\n%s", query, args)
        records = await self.db.fetch(query, *args)
        return [TrendingEntity(**dict(record)) for record in records]

    async def get_trending_entities(self, category: str, year: int, month: Optional[int] = None) -> List[TrendingEntity]:
        base_condition = f"e.type = $1 AND date_part('year', ae.publication_date) = $2"

        if month is None:
            query = self._build_trend_query(base_condition)
            return await self._get_trends(query, category, year)

        # Calculate previous month
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        # Build query for monthly trends
        query = self._build_monthly_query(f"{base_condition} AND date_part('month', ae.publication_date) = $3")
        return await self._get_trends(query, category, year, month, prev_year, prev_month)

    async def get_trending_keywords(self, year: int, month: Optional[int] = None) -> List[TrendingEntity]:
        base_condition = f"date_part('year', ae.publication_date) = $2"

        if month is None:
            query = self._build_trend_query(base_condition)
            return await self._get_trends(query, "", year)

        # Calculate previous month
        if month == 1:
            prev_year = year - 1
            prev_month = 12
        else:
            prev_year = year
            prev_month = month - 1

        # Build query for monthly trends
        query = self._build_monthly_query(f"{base_condition} AND date_part('month', ae.publication_date) = $3")
        return await self._get_trends(query, "", year, month, prev_year, prev_month)

