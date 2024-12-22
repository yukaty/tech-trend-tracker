import logging
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.analysis.similar import find_similar_articles
from app.core.models import SimilarArticlesResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/similar", response_model=SimilarArticlesResponse)
async def search_similar_articles(
    query: str = Query(..., description="Search query text"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Results per page"),
):
    """Search for similar articles based on the query."""
    try:
        articles, total = await find_similar_articles(
            query=query,
            limit=limit,
            offset=(page - 1) * limit,
        )

        return SimilarArticlesResponse(
            articles=articles,
            total=total,
            hasMore=total > page * limit  # Check if there are more pages
        )
    except Exception as e:
        logger.error(f"Failed to search similar articles: {e}")
        raise HTTPException(status_code=500, detail=str(e))