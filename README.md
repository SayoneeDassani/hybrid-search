
# Hybrid Search API

This project is a backend service that supports searching a large collection of magazine articles using both keyword-based and semantic vector search. It is designed to be fast, scalable, and developer-friendly. The system combines traditional full-text filtering with vector similarity to return the most relevant results to the user query.

## Features

- Search by keyword in title, author, and content
- Semantic search using vector similarity
- Combined relevance-based result ranking

## Technologies

- Python 3.9
- FastAPI
- PostgreSQL + pgvector
- SQLAlchemy

## How It Works (Algorithm Description)

The hybrid search combines keyword filtering with semantic vector similarity in a single SQL query:

1. **User Input**: Query passed via `/search?q=...`.
2. **Embedding Generation**: Query is converted to a 1536-dimensional vector using a dummy embedding function (or real models like OpenAI/HuggingFace).
3. **SQL Execution**:
   - `ILIKE` for keyword match
   - `<#>` for vector cosine similarity using `pgvector`
   - Example:
     ```sql
     (1 - (vector_representation <#> :vector::vector)) AS similarity
     ```
4. **Ranking**: Results are ordered by the similarity score.
5. **Response**: Top 10 results are returned as JSON.

## Data Model

### magazine_info

| Field             | Type     | Description              |
|------------------|----------|--------------------------|
| id               | Integer  | Primary key              |
| title            | String   | Magazine title           |
| author           | String   | Author                   |
| publication_date | Date     | Date of publication      |
| category         | String   | Category of magazine     |

### magazine_content

| Field                   | Type         | Description                         |
|------------------------|--------------|-------------------------------------|
| id                     | Integer      | Primary key                         |
| magazine_id            | Foreign Key  | References `magazine_info.id`       |
| content                | Text         | Full content of the magazine        |
| vector_representation  | Vector(1536) | Embedding vector for semantic search|

## API Endpoint

### `GET /search?q=<query>`

Returns a list of top 10 results based on keyword and vector similarity.

**Example:**

```
GET /search?q=br
```

**Response:**

```json

[
  {
    "id": 806,
    "title": "Lost in Time",
    "author": "Augustin Farbrace",
    "category": "Travel",
    "publication_date": "2024-04-30",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 54,
    "title": "The Secret Garden",
    "author": "Brendin Hazard",
    "category": "Health",
    "publication_date": "2024-11-29",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 730,
    "title": "Lost in Time",
    "author": "Janelle De Bruin",
    "category": "Sports",
    "publication_date": "2024-06-28",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 467,
    "title": "Whimsical Wonderland",
    "author": "Brennan Mulkerrins",
    "category": "Fashion",
    "publication_date": "2024-03-08",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 709,
    "title": "Starlight Serenade",
    "author": "Bruno Selly",
    "category": "Fashion",
    "publication_date": "2024-02-05",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 493,
    "title": "Echoes of Eternity",
    "author": "Noellyn Fellibrand",
    "category": "Food",
    "publication_date": "2024-05-10",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 964,
    "title": "The Secret Garden",
    "author": "Danella Brehault",
    "category": "Entertainment",
    "publication_date": "2024-10-18",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 732,
    "title": "Echoes of Eternity",
    "author": "Brice Lehrer",
    "category": "Health",
    "publication_date": "2024-07-05",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 952,
    "title": "The Secret Garden",
    "author": "Bryna Carnalan",
    "category": "Fashion",
    "publication_date": "2025-03-26",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  },
  {
    "id": 556,
    "title": "Enchanted Dreams",
    "author": "Brandi Gruszecki",
    "category": "Business",
    "publication_date": "2024-12-26",
    "content": "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    "similarity": 1.7598
  }

]
```

## Setup

### 1. Start PostgreSQL with Docker

```bash
docker compose up -d
```

Enable `pgvector`:

```bash
docker exec -it postgres psql -U admin -d test
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create tables and load data

```bash
python -m app.init_db
python -m app.load_data
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

Go to: http://localhost:8000/docs to test.

## Performance Considerations

- The system is designed to handle 1 million+ records efficiently.
- Vector columns use the `pgvector` extension with proper type casting.
- Queries use `LIMIT 10` and are filtered with both keyword and similarity metrics.
- Dummy embeddings are used for testing but structured for drop-in replacement with real models.
- SQLAlchemy session management is used for safe and scalable DB access.
- Docker setup ensures portability and consistent environment.

## Notes

- CSVs from Mockaroo should be placed in the `data/` folder.
- Replace the embedding generator with OpenAI or HuggingFace for production use.
