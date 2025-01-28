import logging, traceback
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.embedding import get_embedding_async
from app.services.openai import generate_answer
from app.services.rag import find_relevant_chunks_with_articles, get_total_relevant_articles
from app.services.keyword import search_by_keyword
from app.core.models import ArticlesResponse, RagSearchResponse, RelevantArticle

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get(
    "/similar",
    response_model=RagSearchResponse,
    operation_id="search_articles_with_rag",
    summary="Search Articles with RAG"
)
async def search_articles(
    query: str = Query(..., description="Search query text"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Results per page"),
) -> RagSearchResponse:
    """
    Search articles using RAG approach:
    1. Find relevant chunks using embedding similarity
    2. Generate AI answer based on chunks
    3. Return answer and source articles
    """
    try:
        # Get query embedding
        query_embedding = await get_embedding_async(query)

        # Find relevant chunks and articles
        chunks_with_articles = await find_relevant_chunks_with_articles(
            query_embedding=query_embedding,
            limit=limit,
            offset=(page - 1) * limit,
        )

        # Generate answer using relevant chunks
        chunks_text = [chunk.chunk_text for chunk, _ in chunks_with_articles]
        answer = await generate_answer(query, chunks_text)

        # Format response
        articles = [
            RelevantArticle(
                **article.dict(),
                relevance_score=chunk.relevance_score,
                relevant_chunk=chunk.chunk_text
            )
            for chunk, article in chunks_with_articles
        ]

        total = await get_total_relevant_articles(query_embedding)

        return RagSearchResponse(
            answer=answer,
            articles=articles,
            total=total,
            hasMore=total > page * limit  # Check if there are more pages
        )
    except Exception as e:
        logger.error(f"Failed to search similar articles: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/keyword",
    response_model=ArticlesResponse,
    operation_id="search_by_keyword",
    summary="Search Articles By Keyword"
)
async def search_by_keyword_handler(
    q: str = Query(..., description="Keyword to search for"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Results per page"),
):
    """Search for articles by keyword."""
    try:
        articles, total = await search_by_keyword(
            keyword=q,
            limit=limit,
            offset=(page - 1) * limit,
        )

        return ArticlesResponse(
            articles=articles,
            total=total,
            hasMore=total > page * limit
        )
    except Exception as e:
        logger.error(f"Failed to search articles by keyword: {e}")
        raise HTTPException(status_code=500, detail=str(e))