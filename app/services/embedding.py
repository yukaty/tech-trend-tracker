import os
from openai import OpenAI, AsyncOpenAI
from typing import List
import psycopg

client = OpenAI()

def get_embedding(text: str) -> List[float]:
    """Generate embedding using OpenAI API (sync)."""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding

async def get_embedding_async(text: str) -> List[float]:
    """Generate embedding using OpenAI API (async)."""
    client = AsyncOpenAI()
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return response.data[0].embedding

def generate_embeddings() -> None:
    """Generate embeddings for article chunks."""
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            # Get chunks without embeddings
            cur.execute("""
                SELECT c.id, c.chunk_text, c.metadata->>'headline' as headline
                FROM article_chunks c
                WHERE c.chunk_embedding IS NULL
            """)
            chunks = cur.fetchall()

        for chunk_id, chunk_text, headline in chunks:
            try:
                # Create combined text for embedding
                combined_text = f"Title: {headline}\n\nContent: {chunk_text}"
                embedding = get_embedding(combined_text)

                # Update database
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE article_chunks
                        SET chunk_embedding = %s
                        WHERE id = %s
                    """, (embedding, chunk_id))
                conn.commit()

            except Exception as e:
                print(f"Failed to generate embedding for chunk {chunk_id}: {e}")