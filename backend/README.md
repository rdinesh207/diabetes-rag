# GenAI RAG Backend

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Gemini API key and Entrez email:
   ```bash
   cp .env.example .env
   # Edit .env
   ```

   Add the following to your `.env` file:
   ```env
   PINECONE_INDEX_NAME=diabetes-papers
   ```

## Data Ingestion

1. Download PubMed PDFs (placeholder URLs in ingest.py):
   ```bash
   python ingest.py
   ```

2. Extract and embed text, add to ChromaDB:
   ```bash
   python embed.py
   ```

## Running the API

- Local dev:
  ```bash
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

- With Docker:
  ```bash
  docker build -t genai-rag-backend .
  docker run --env-file .env -p 8000:8000 genai-rag-backend
  ```

## Endpoints

- `POST /ask` — JSON `{ "question": "..." }` → `{ "answer": "...", "citations": [...] }`

## Notes
- Update PDF download logic in `ingest.py` for real PubMed/EPMC access.
- ChromaDB is local by default; configure for production as needed. 