# GenAI RAG Frontend

## Setup

1. Install dependencies:
   ```bash
   npm install
   # or
   bun install
   ```

2. Start the dev server:
   ```bash
   npm run dev
   # or
   bun run dev
   ```

- The app runs at http://localhost:5173 by default.
- API requests to `/api` are proxied to the backend (see `vite.config.ts`).

## Features
- Chat UI for asking PubMed diabetes research questions
- Answers with citations
- Document preview panel

## Notes
- Ensure the backend is running at http://localhost:8000 for API calls to work.
