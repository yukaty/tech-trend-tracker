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
    """Generate embeddings for articles without them."""
    conn_str = os.getenv("DATABASE_URL")

    with psycopg.connect(conn_str) as conn:
        # Get articles without embeddings
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, headline, description, content
                FROM articles
                WHERE embedding IS NULL
            """)
            articles = cur.fetchall()

        # Generate and update embeddings
        for article_id, headline, description, content in articles:
            # combined_text = f"{headline}\n\n{description}"
            combined_text = f"""
            Title: {headline}
            Description: {description}
            Content Summary: {content[:500]}
            """
            embedding = get_embedding(combined_text)

            # Update database
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE articles
                    SET embedding = %s
                    WHERE id = %s
                """, (embedding, article_id))

            conn.commit()
