from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class RelatedArticle(BaseModel):
    """Related article reference"""
    article_title: str
    article_url: str

    model_config = ConfigDict(from_attributes=True)

class Article(BaseModel):
    """Article data model for tech trend analysis"""
    id: str
    url: str
    headline: str
    description: Optional[str] = None
    content: str
    topics: List[str]
    publication_date: datetime
    updated_last: Optional[datetime] = None
    source: Optional[str] = "Reuters"
    related_articles: Optional[List[RelatedArticle]] = None
    keyword: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class SimilarArticle(BaseModel):
    """Article model for similarity search results"""
    id: str
    url: str
    headline: str
    description: Optional[str] = None
    publication_date: datetime
    source: str = "Reuters"
    topics: List[str]
    similarity_score: float

    model_config = ConfigDict(from_attributes=True)

    @property
    def formatted_date(self) -> str:
        """Return formatted date for frontend display"""
        return self.publication_date.strftime("%b %d, %Y")

class SimilarArticlesResponse(BaseModel):
    """Response model for similar articles search"""
    articles: List[SimilarArticle]
    total: int
    hasMore: bool

class TrendingEntity(BaseModel):
    """Response model for trending entities"""
    name: str
    count: int
    trend: float  # Trend percentage