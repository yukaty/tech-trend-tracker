import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from app.db.async_client import DatabaseClient
from app.services.trends import TrendService
from app.core.models import TrendingEntity

logger = logging.getLogger(__name__)

router = APIRouter()

async def get_db():
    db = DatabaseClient()
    await db.connect()
    try:
        yield db
    finally:
        await db.close()

@router.get("/entities", response_model=List[TrendingEntity])
async def get_trending_entities(
    category: str,
    year: int = 2024,
    month: Optional[int] = None,
    db: DatabaseClient = Depends(get_db)
):
    service = TrendService(db)
    return await service.get_trending_entities(category, year, month)

@router.get("/keywords", response_model=List[TrendingEntity])
async def get_trending_keywords(
    year: int = 2024,
    month: Optional[int] = None,
    db: DatabaseClient = Depends(get_db)
):
    service = TrendService(db)
    return await service.get_trending_keywords(year, month)