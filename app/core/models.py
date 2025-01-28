from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class Article(BaseModel):
    id: str
    url: str
    headline: str
    description: Optional[str] = None
    publication_date: datetime
    source: Optional[str] = "Reuters"

    model_config = ConfigDict(from_attributes=True)

    @property
    def formatted_date(self) -> str:
        return self.publication_date.strftime("%b %d, %Y")

class ArticlesResponse(BaseModel):
    articles: List[Article]
    total: int
    hasMore: bool

class TrendingEntity(BaseModel):
    name: str
    count: int
    trend: float | None = None

# RAG Search
class ChunkWithScore(BaseModel):
    chunk_text: str
    relevance_score: float

    model_config = ConfigDict(from_attributes=True)

class RelevantArticle(Article):
    relevance_score: float
    relevant_chunk: str

class RagSearchResponse(BaseModel):
    answer: str
    articles: List[RelevantArticle]
    total: int
    hasMore: bool
