import asyncio
from dotenv import load_dotenv
from app.services.news import fetch_and_save_news

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(fetch_and_save_news())

    # For Demo
    # asyncio.run(fetch_and_save_news(days=365, articles_per_batch=50))