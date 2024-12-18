-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- News Articles
CREATE TABLE articles (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    headline TEXT NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    topics TEXT[],
    publication_date TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_last TIMESTAMP WITH TIME ZONE,
    source TEXT DEFAULT 'Reuters',
    related_articles JSONB,
    keyword TEXT,
    embedding vector(1536)         -- OpenAI text embeddings
);

-- Index
CREATE INDEX idx_articles_publication_date ON articles(publication_date);
CREATE INDEX idx_articles_topics ON articles USING gin(topics);