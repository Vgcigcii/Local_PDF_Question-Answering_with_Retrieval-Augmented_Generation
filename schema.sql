--The following command tells psql to activate pgvector extension in  the target database
CREATE EXTENSION IF NOT EXISTS  vector;

--Creating a table named documents with the following values to hold the documents metadata that we upload on the rag bot
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL UNIQUE,
    uploaded_at TIMESTAMP DEFAULT now(),
    metadata JSONB DEFAULT '{}'
);
--Create a table to hold chunks from the documents that will be created by the text splitter
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding VECTOR(384),
    tsv tsvector GENERATED ALWAYS AS (to_tsvector('english', chunk_text)) STORED,
    UNIQUE (document_id, chunk_index)
);
--Hierarchical navigable small world or hnsw is a type of index that builds graph that lets the search skips most vectors so it finds the approximate nearest neighbour searches over embedding vectors.
CREATE INDEX IF NOT EXISTS idx_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops);
--A Generalized Inverted INdex indexes individual values  that appears inside your JSONB and for each one it keeps a list of which rows contain it.
CREATE INDEX IF NOT EXISTS idx_chunks_tsv ON chunks USING GIN (tsv);

---We are using HNSW  and GIN inorder to speed up vector similarity and full-text searches.