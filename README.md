# Hybrid Search API

This project implements a high-performance hybrid search API using Python 3.9, FastAPI, PostgreSQL, and the `pgvector` extension. The system supports keyword-based and vector-based searches on magazine records and is designed to efficiently handle up to 1 million entries.

## Table of Contents

- [Overview](#overview)
- [Data Model](#data-model)
- [Search Functionality](#search-functionality)
- [API Endpoint](#api-endpoint)
- [Setup Instructions](#setup-instructions)
- [Performance Considerations](#performance-considerations)
- [Deliverables](#deliverables)
- [Future Improvements](#future-improvements)

## Overview

The goal is to create a hybrid search system combining:

- **Keyword Search**: Traditional filtering using SQL ILIKE queries on metadata and content.
- **Vector Search**: Semantic similarity search using vectors stored with the `pgvector` extension.
- **Hybrid Search**: A SQL-based approach that combines both keyword and vector similarity to return the most relevant results.

This API is built using FastAPI for modern async capabilities, and SQLAlchemy for ORM-based interaction with the PostgreSQL database.

## Data Model

### Table 1: `magazine_info`

| Field             | Type     | Description                  |
|------------------|----------|------------------------------|
| `id`             | Integer  | Primary key                  |
| `title`          | String   | Title of the magazine        |
| `author`         | String   | Author of the magazine       |
| `publication_date` | Date   | Date of publication          |
| `category`       | String   | Category (e.g., Tech, Health)|

### Table 2: `magazine_content`

| Field                   | Type         | Description                         |
|------------------------|--------------|-------------------------------------|
| `id`                   | Integer      | Primary key                         |
| `magazine_id`          | Foreign Key  | References `magazine_info.id`       |
| `content`              | Text         | Full text content of the magazine   |
| `vector_representation`| Vector(1536) | Semantic vector using `pgvector`    |

## Search Functionality

The hybrid search combines two core search strategies:

- **Keyword Search**: Full-text match using `ILIKE` on `title`, `author`, and `content`.
- **Vector Search**: Semantic similarity using cosine distance (`<#>`) between the query vector and precomputed content vectors.

### SQL Hybrid Ranking
Results are ordered by a computed similarity score:

```sql
(1 - (vector_representation <#> query_vector)) AS similarity
```

## API Endpoint

### `GET /search`

Performs a hybrid search on the magazine data.

#### Parameters

| Name | Type | Description |
|------|------|-------------|
| `q`  | str  | Required. Search term or phrase. |

#### Example

```
GET /search?q=artificial intelligence
```

#### Example Response

```json
[
  {
    "id": 12,
    "title": "AI in Healthcare",
    "author": "Jane Doe",
    "category": "Health",
    "publication_date": "2024-05-01",
    "content": "This article discusses the impact of artificial intelligence in healthcare...",
    "similarity": 0.9421
  }
]
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd hybrid-search-api
```

### 2. Start PostgreSQL with pgvector using Docker

Create or use the provided `docker-compose.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres
    container_name: postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: test
    volumes:
      - db:/data/postgres
    restart: unless-stopped

volumes:
  db: {}
```

Then run:

```bash
docker-compose up -d
```

Enable the `pgvector` extension:

```bash
docker exec -it postgres psql -U admin -d test
```

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Exit with `\q`.

### 3. Set up the environment and install dependencies

```bash
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate

pip install -r requirements.txt
```

### 4. Create tables and load sample data

```bash
python -m app.init_db
python -m app.load_data
```

Make sure your `data/` directory contains `magazine_info.csv` and `magazine_content.csv`.

### 5. Run the API

```bash
uvicorn app.main:app --reload
```

Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

## Performance Considerations

- Efficient indexing using the `pgvector` extension for vector similarity search.
- Search queries are optimized using SQL with explicit vector casting.
- Dummy embeddings are generated using NumPy (can be replaced with production models).
- `LIMIT` used to cap results for fast response time.
- SQLAlchemy used with session management and merge logic for efficient data loading.

## Deliverables

- **Source Code**: Full Python FastAPI application with all dependencies listed in `requirements.txt`.
- **Database Schema**: ORM models defined in `app/models.py`.
- **Documentation**: This `README.md` provides setup and usage instructions.
- **Performance Report**: See “Performance Considerations”.

## Future Improvements

- Integrate real semantic embeddings using OpenAI or HuggingFace.
- Add query filters (e.g., filter by category, date range, or author).
- Support pagination in the search endpoint.
- Add unit and integration tests.
- Dockerize the FastAPI app for easier deployment.
