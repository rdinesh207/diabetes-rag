# GenAI RAG Assessment App

## Overview

This project is a full-stack web application for question-answering and document search over a collection of medical/scientific papers (PDFs). It uses a Retrieval-Augmented Generation (RAG) approach, combining a FastAPI backend with a modern React frontend.

- **Backend**: Python (FastAPI), handles PDF ingestion, embedding (with sentence-transformers), and question answering using LLMs (local or Gemini). Stores embeddings in Pinecone and/or ChromaDB.
- **Frontend**: React (TypeScript, Vite, Tailwind), provides a chat UI for asking questions, viewing answers with citations, and previewing documents.
- **DevOps**: Docker and Docker Compose for local and production deployment. Optional Ollama service for running local LLMs.

---

## Features

- Ingest and embed scientific PDFs for semantic search.
- Ask questions and receive answers with citations.
- Modern, responsive chat UI.
- Supports both local and commercial LLMs (Ollama, Gemini, etc.).

---

## Prerequisites

- [Docker](https://www.docker.com/get-started) and [Docker Compose](https://docs.docker.com/compose/)
- (Optional) API keys for Pinecone, Gemini, etc. (see below)

---

## Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
PINECONE_INDEX_NAME=diabetes-papers
GEMINI_API_KEY=your_gemini_api_key
ENTREZ_EMAIL=your_email_for_entrez
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=hf.co/mradermacher/MediPhi-PubMed-i1-GGUF:Q6_K
```

Adjust as needed for your deployment.

---

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # if available, otherwise create .env as above
python ingest.py      # Download and process PDFs
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install           # or bun install
npm run dev           # or bun run dev
# App runs at http://localhost:5173
```

---

## Docker Deployment

### 1. Build and Run with Docker Compose

From the project root:

```bash
docker-compose up --build
```

- **Backend**: http://localhost:5000
- **Frontend**: http://localhost:8080
- **Ollama (LLM)**: http://localhost:11434

### 2. Stopping the Services

```bash
docker-compose down
```

---

## Project Structure

```
assessment/
  backend/      # FastAPI backend, PDF ingestion, embedding, API
  frontend/     # React frontend, chat UI
  Dockerfile    # Backend Docker build
  docker-compose.yml  # Multi-service orchestration
```

---

## Notes

- Update `backend/papers` with real PDF sources as needed.
- For GPU support, uncomment the relevant lines in `docker-compose.yml` and use a CUDA base image in the Dockerfile.
- Ensure all required environment variables are set in `backend/.env`.

---

## API

- `POST /api/ask` — `{ "question": "..." }` → `{ "answer": "...", "citations": [...] }`

--- 
