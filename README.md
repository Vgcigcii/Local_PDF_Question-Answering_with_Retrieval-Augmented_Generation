# Local PDF Question-Answering with Retrieval-Augmented Generation

A local Retrieval-Augmented Generation (RAG) application for asking questions about PDF documents. Upload a PDF through the Streamlit interface, store its text chunks and embeddings in PostgreSQL/pgvector, and receive answers from a local Ollama model grounded in the retrieved document content.

## How it works

1. The app extracts text from an uploaded PDF and keeps page markers in the text.
2. It splits the text into overlapping chunks (500 characters with 100-character overlap).
3. Each chunk is embedded with the `all-MiniLM-L6-v2` SentenceTransformers model (384 dimensions).
4. The chunks and vectors are saved to PostgreSQL with the pgvector extension.
5. For each question, the app retrieves the five nearest chunks using cosine distance and sends them as context to Ollama's `llama3.2` model.

The prompt instructs the model to use only the retrieved context. The UI also shows the source filename, chunk number, and retrieval distance for each answer.

## Prerequisites

- Python 3.10 or newer
- PostgreSQL with the [pgvector](https://github.com/pgvector/pgvector) extension available
- [Ollama](https://ollama.com/) running locally

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Create a database named `rag` (or choose another name) and apply the schema:

```powershell
psql -U postgres -d rag -f schema.sql
```

`schema.sql` enables pgvector and creates the `documents` and `chunks` tables, including HNSW vector and full-text indexes.

Copy `.env.example` to `.env`, then update the values for your local PostgreSQL instance:

```env
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=rag
DB_USER=postgres
DB_PASSWORD=your_password
```

The example uses port `5433`; use `5432` instead if that is your PostgreSQL port. `DB_PASSWORD` must be present, even when it is empty.

### 4. Download the Ollama model

```powershell
ollama pull llama3.2
```

Make sure the Ollama service is running before starting the app. The default model can be changed in `main.py` when creating `OllamaChatBot`.

### 5. Run the application

```powershell
streamlit run web_app.py
```

Open the local Streamlit URL shown in the terminal, upload a PDF, click **Process Document**, and ask questions in the chat box.

## Project structure

| File                 | Purpose                                                                       |
|----------------------|-------------------------------------------------------------------------------|
| `web_app.py`         | Streamlit upload and chat interface.                                          |
| `main.py`            | Coordinates ingestion, retrieval, prompt construction, and answer generation. |
| `Document_work.py`   | Extracts PDF text and splits it into chunks.                                  |
| `Embeddings_work.py` | Creates document and query embeddings.                                        |
| `Building_Model.py`  | Builds the grounded RAG prompt and calls Ollama.                              |
| `db.py`              | Loads database configuration and opens PostgreSQL connections.                |
| `schema.sql`         | Database tables, pgvector extension, and indexes.                             |
| `retrieve.py`        | Retrieves the nearest stored chunks using cosine distance                     |
| `store.py`           | Stores,lists,replaces,and deletes indexed documents.                          |
## Notes

- Reprocessing a file with the same filename replaces that document's stored chunks.
- Only text-based, unencrypted PDFs are supported. Scanned PDFs without an embedded text layer will not produce chunks.
- Retrieval searches all documents stored in the database, including documents indexed in earlier Streamlit sessions. If no sufficiently relevant chunk is found, the app reports that it could not find an answer in the stored documents.
- Documents remain in the database between Streamlit sessions. To remove all indexed content, clear the `documents` table; its related chunks are deleted automatically through the foreign-key cascade.
- Documents can be deleted in the sidebar.Anyone using the app can delete anything.
## Troubleshooting

- **`extension "vector" is not available`**: install pgvector for your PostgreSQL server, then run `schema.sql` again.
- **Database connection error**: confirm the values in `.env`, PostgreSQL is running, and the configured port matches the server.
- **Ollama error**: start Ollama and run `ollama pull llama3.2` to ensure the selected model exists locally.
- **No useful answer**: verify that the PDF was processed successfully and that it contains selectable text.
