-- RUN THIS IN SUPABASE SQL EDITOR
-- ===============================

-- 1. Enable the pgvector extension to work with embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Add the embedding column for the BGE-M3 model (1024 dimensions)
-- Note: If you already have a column named 'embedding', drop it first or rename it.
ALTER TABLE knowledge_chunks 
ADD COLUMN IF NOT EXISTS embedding vector(1024);

-- 3. (Optional) Create an HNSW index for high-performance search
-- HNSW is faster than IVFFlat for smaller datasets like ours
CREATE INDEX IF NOT EXISTS idx_knowledge_chunks_embedding 
ON knowledge_chunks 
USING hnsw (embedding vector_cosine_ops);

-- 4. Drop the existing function first (required because we changed dimensions from 768/1536 to 1024)
DROP FUNCTION IF EXISTS match_knowledge(vector, float, int);

-- 5. Create the updated function with 1024 dimensions
CREATE OR REPLACE FUNCTION match_knowledge (
  query_embedding vector(1024),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id bigint,
  content text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    knowledge_chunks.id,
    knowledge_chunks.content,
    1 - (knowledge_chunks.embedding <=> query_embedding) AS similarity
  FROM knowledge_chunks
  WHERE 1 - (knowledge_chunks.embedding <=> query_embedding) > match_threshold
  ORDER BY similarity DESC
  LIMIT match_count;
END;
$$;
