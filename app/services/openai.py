import logging
import re
from typing import List
from openai import AsyncOpenAI

logger = logging.getLogger(__name__)
client = AsyncOpenAI()

async def generate_answer(query: str, relevant_chunks: List[str]) -> str:
    """
    Generate an answer based on the query and relevant chunks
    Args:
        query: User's question
        relevant_chunks: List of relevant text chunks from articles
    Returns:
        Generated answer with context
    """
    try:
        # Prepare context from chunks
        cleaned_chunks = [
            re.sub(r'\([^)]*\)', '',
                re.sub(r'<[^>]+>', '', chunk)
            ) for chunk in relevant_chunks
        ]
        context = "\n\n".join(cleaned_chunks)

        prompt = f"""Based on these news excerpts, provide a clear and concise answer.
        Focuses on concrete facts and data from provided sources.
        If information is missing, state it briefly.

        Context:
        {context}

        Question: {query}"""

        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                 "content": """You are a clear and insightful technology analyst who:
                 - Structures answers in 2-3 key points
                 - Includes specific numbers to support insights
                 - Uses concise, direct language"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "Sorry, I couldn't generate an answer at this time."