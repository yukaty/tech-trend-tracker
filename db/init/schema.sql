-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;
-- Enable citext extension for case-insensitive text
CREATE EXTENSION IF NOT EXISTS citext;

-- News Articles
CREATE TABLE IF NOT EXISTS articles (
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

-- Entities
CREATE TABLE IF NOT EXISTS entities (
    name TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK (type IN ('company', 'person', 'service'))
);

-- Article Entities (Many-to-Many)
CREATE TABLE IF NOT EXISTS article_entities (
    article_id TEXT REFERENCES articles(id),
    entity_name TEXT REFERENCES entities(name),
    publication_date DATE NOT NULL,
    PRIMARY KEY (article_id, entity_name)
);

-- Index
CREATE INDEX IF NOT EXISTS idx_articles_publication_date ON articles(publication_date);
CREATE INDEX IF NOT EXISTS idx_articles_topics ON articles USING gin(topics);
CREATE INDEX IF NOT EXISTS idx_article_entities_date ON article_entities(publication_date);
CREATE INDEX IF NOT EXISTS idx_article_entities_entity_date ON article_entities(entity_id, publication_date);