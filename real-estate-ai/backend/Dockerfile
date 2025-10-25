# Backend Dockerfile for Real Estate AI (FastAPI)
FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for building/scientific packages (faiss, xgboost, scikit-learn, spacy)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	   build-essential \
	   gcc \
	   g++ \
	   curl \
	   libopenblas-dev \
	   libomp-dev \
	   libffi-dev \
	   git \
	&& rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer cache)
COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
	&& pip install -r requirements.txt

# Copy application code
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Default environment (override via compose/env)
ENV UVICORN_HOST=0.0.0.0 \
	UVICORN_PORT=8000

# Start the API
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

