from dotenv import load_dotenv
from app.services.embedding import generate_embeddings

if __name__ == "__main__":
    load_dotenv()
    generate_embeddings()
