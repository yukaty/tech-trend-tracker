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
    publication_date TIMESTAMP WITH TIME ZONE NOT NULL,
    source TEXT DEFAULT 'Reuters'
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

-- Article Chunks
CREATE TABLE article_chunks (
    id UUID PRIMARY KEY,
    article_id TEXT REFERENCES articles(id),
    chunk_text TEXT NOT NULL,
    chunk_embedding vector(1536),
    chunk_index INTEGER,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX IF NOT EXISTS idx_articles_publication_date ON articles(publication_date);
CREATE INDEX IF NOT EXISTS idx_article_entities_date ON article_entities(publication_date);
CREATE INDEX IF NOT EXISTS idx_article_entities_entity_date ON article_entities(entity_name, publication_date);

-- Index for article_chunks
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON article_chunks
USING ivfflat (chunk_embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_chunks_text ON article_chunks USING gin(to_tsvector('english', chunk_text));
CREATE INDEX IF NOT EXISTS idx_chunks_metadata ON article_chunks USING gin(metadata);
CREATE INDEX IF NOT EXISTS idx_chunks_article_index ON article_chunks(article_id, chunk_index);