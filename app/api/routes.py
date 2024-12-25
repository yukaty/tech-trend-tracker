from fastapi import APIRouter
from app.api.endpoints import search, trends

router = APIRouter()
router.include_router(search.router, prefix="/search", tags=["search"])
router.include_router(trends.router, prefix="/trends", tags=["trends"])
