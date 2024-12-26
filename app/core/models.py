from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class RelatedArticle(BaseModel):
    article_title: str
    article_url: str
    model_config = ConfigDict(from_attributes=True)

class Article(BaseModel):
    id: str
    url: str
    headline: str
    description: Optional[str] = None
    content: str = None
    topics: List[str] = None
    publication_date: datetime
    updated_last: Optional[datetime] = None
    source: Optional[str] = "Reuters"
    related_articles: Optional[List[RelatedArticle]] = None
    keyword: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @property
    def formatted_date(self) -> str:
        return self.publication_date.strftime("%b %d, %Y")

class SimilarArticle(Article):
    similarity_score: float

class ArticlesResponse(BaseModel):
    articles: List[Article]
    total: int
    hasMore: bool

class SimilarArticlesResponse(BaseModel):
    articles: List[SimilarArticle]
    total: int
    hasMore: bool

class TrendingEntity(BaseModel):
    name: str
    count: int
    trend: float