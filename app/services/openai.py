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
            re.sub(r"\([^)]*\)", "", re.sub(r"<[^>]+>", "", chunk))
            for chunk in relevant_chunks
        ]
        context = "\n\n".join(cleaned_chunks)

        prompt = f"""Based on these news excerpts, provide a clear and concise answer.
        Focuses on concrete facts and data from provided sources.
        If information is missing, state it briefly.

        Context:
        {context}

        Question: {query}"""

        response = await client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {
                    "role": "system",
                    "content": """You are a clear and insightful technology analyst who:
                 - Structures answers in 2-3 key points
                 - Includes specific numbers to support insights
                 - Uses concise, direct language""",
                },
                {"role": "user", "content": prompt},
            ],
            max_completion_tokens=2000,
        )

        # Debug: log token usage for reasoning model
        logger.info(
            f"Token usage - Reasoning: {response.usage.completion_tokens_details.reasoning_tokens}, "
            f"Total completion: {response.usage.completion_tokens}, "
            f"Finish reason: {response.choices[0].finish_reason}"
        )

        content = response.choices[0].message.content
        if not content:
            logger.warning(
                f"Empty response from gpt-5-nano. Reasoning tokens: {response.usage.completion_tokens_details.reasoning_tokens}"
            )
            return "Sorry, I couldn't generate an answer at this time."

        return content

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        return "Sorry, I couldn't generate an answer at this time."
