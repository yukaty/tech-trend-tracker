import asyncio
from dotenv import load_dotenv
from app.services.news import collect_tech_news
from app.db.sync_client import save_articles

if __name__ == "__main__":
    load_dotenv()

    # Fetch articles asynchronously from API
    articles = asyncio.run(collect_tech_news())

    # Fetch 10 articles per keyword from the last 7 days
    # articles = asyncio.run(collect_tech_news(articles_per_keyword=10))

    # Full data collection: All articles within 2024
    # articles = asyncio.run(collect_tech_news(start_date="20240101"))

    # Save the data to database synchronously
    save_articles(articles)
