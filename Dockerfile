# Dockerfile for backend (FastAPI + Uvicorn/Gunicorn, production-ready)
# For GPU support, use a CUDA base image (uncomment below)
# FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04 AS backend
FROM python:3.11-slim AS backend

WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy backend code
COPY backend/ ./

# Copy .env if present (for local dev; in prod, use secrets/env vars)
COPY backend/.env ./

# Expose backend port
EXPOSE 5000

# Run Gunicorn with Uvicorn workers for production
CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120"]
