import asyncio
from dotenv import load_dotenv
from app.services.news import collect_tech_news
from app.db.sync_client import save_articles

if __name__ == "__main__":
    load_dotenv()

    # Fetch articles of the last 7 days from API
    articles = asyncio.run(collect_tech_news())

    # Save the data to database
    save_articles(articles)
