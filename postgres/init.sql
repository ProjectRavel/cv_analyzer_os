
-- Initialize the database with the necessary extensions and tables for storing documents and their embeddings.
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create an index on the embedding column to optimize similarity searches.
CREATE INDEX IF NOT EXISTS documents_embedding_idx
ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);