from fastapi import APIRouter
from app.api.endpoints import similar

router = APIRouter()
router.include_router(similar.router, prefix="/articles", tags=["articles"])
