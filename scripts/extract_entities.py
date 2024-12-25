import os
import asyncio
import asyncpg
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

class EntityExtractor:
    def __init__(self):
        self.client = AsyncOpenAI()

    async def extract(self, text: str):
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": """Extract tech companies, people, and services mentioned in the text.
                    Only include technology-related entities.
                    Always maintain the exact name format as it appears in the text.

                    Examples:
                    - Companies: OpenAI, Microsoft, Meta
                    - People: Sam Altman, Satya Nadella, Mark Zuckerberg
                    - Services: ChatGPT, GitHub Copilot, Microsoft Azure

                    Return in JSON format with exactly this structure:
                    {
                        "entities": [
                            {"name": "exact name from text", "type": "company|person|service"}
                        ]
                    }
                    """},
                    {"role": "user", "content": text}
                ],
                response_format={ "type": "json_object" }
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in entity extraction: {str(e)}")
            return '{"entities": []}'

class DatabaseManager:
    def __init__(self, connection_url: str):
        self.pool = None
        self.connection_url = connection_url

    async def connect(self):
        self.pool = await asyncpg.create_pool(self.connection_url)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def save_entities(self, article_id: str, publication_date: datetime, entities_json: str):
        entities = json.loads(entities_json)['entities']
        if not entities:
            return

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                for entity in entities:
                    await conn.execute("""
                        INSERT INTO entities (name, type)
                        VALUES ($1, $2)
                        ON CONFLICT (name) DO UPDATE
                        SET type = EXCLUDED.type
                    """, entity['name'], entity['type'])

                    await conn.execute("""
                        INSERT INTO article_entities
                        (article_id, entity_name, publication_date)
                        VALUES ($1, $2, $3)
                        ON CONFLICT (article_id, entity_name) DO NOTHING
                    """, article_id, entity['name'], publication_date)

async def main():
    db_url = os.getenv("DATABASE_URL")

    try:
        db = DatabaseManager(db_url)
        await db.connect()

        extractor = EntityExtractor()

        async with db.pool.acquire() as conn:
            articles = await conn.fetch("""
                SELECT id, headline, content, publication_date
                FROM articles
                ORDER BY publication_date
            """)

        print(f"Processing {len(articles)} articles...")

        for i, article in enumerate(articles, 1):
            try:
                text = f"Headline: {article['headline']}\n\nContent: {article['content']}"
                entities_json = await extractor.extract(text)

                await db.save_entities(
                    article['id'],
                    article['publication_date'],
                    entities_json
                )

                print(f"Processed article {i}/{len(articles)}")
                await asyncio.sleep(1)  # Rate limit to avoid API errors

            except Exception as e:
                print(f"Error processing article {article['id']}: {str(e)}")
                continue

    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())