import os
from openai import OpenAI
from typing import List
import psycopg

client = OpenAI()

def get_embedding(text: str) -> List[float]:
    """Generate embedding using OpenAI API."""
    response = client.embeddings.create(
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
                SELECT id, headline, description
                FROM articles
                WHERE embedding IS NULL
                LIMIT 100
            """)
            articles = cur.fetchall()

        # Generate and update embeddings
        for article_id, headline, description in articles:
            combined_text = f"{headline}\n\n{description}"
            embedding = get_embedding(combined_text)

            # Update database
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE articles
                    SET embedding = %s
                    WHERE id = %s
                """, (embedding, article_id))

            conn.commit()
