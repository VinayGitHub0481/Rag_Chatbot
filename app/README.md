
# RAG Chatbot

A Retrieval-Augmented Generation (RAG) application built using FastAPI, Redis Queue (RQ), OpenAI Embeddings, and Qdrant Vector Database. The application allows users to upload PDF documents, generate vector embeddings from their content, store them in Qdrant, and retrieve the most relevant chunks for a given query.
 
---

## Architecture Overview

The project follows an asynchronous processing architecture using Redis Queue (RQ).

### Workflow

1. User uploads a PDF file through a FastAPI endpoint.
2. The file upload request is queued using Redis Queue.
3. `worker1.py` processes the uploaded PDF asynchronously.
4. Text is extracted, chunked, converted into embeddings, and stored in Qdrant.
5. User submits a query through another FastAPI endpoint.
6. The query request is queued using Redis Queue.
7. `worker2.py` retrieves the most relevant chunks from Qdrant.
8. Results are returned to the user through a job status endpoint.

---

## Components

### redis_queue.py

Responsible for creating and managing the Redis Queue connection.

Functions:

* Connects to Redis.
* Creates job queues.
* Used by FastAPI endpoints to enqueue background jobs.

---

### worker1.py

Contains the `loading_file()` function.

#### Purpose

Processes uploaded PDF files and stores their vector embeddings in Qdrant.

#### Steps Performed

1. Reads uploaded PDF file.
2. Extracts text content.
3. Splits text into smaller chunks.
4. Generates embeddings using OpenAI Embeddings.
5. Creates or uses a Qdrant collection.
6. Inserts chunk embeddings into Qdrant.

#### Function

```python
loading_file()
```

Input:

* PDF file path

Output:

* Vectorized document stored in Qdrant

---

### worker2.py

Contains the `retrieve_info()` function.

#### Purpose

Retrieves the most relevant chunks from Qdrant based on a user query.

#### Steps Performed

1. Receives a user query.
2. Generates embedding for the query.
3. Searches Qdrant using vector similarity.
4. Retrieves the most relevant document chunks.
5. Returns the retrieved information.

#### Function

```python
retrieve_info()
```

Input:

* User query

Output:

* Relevant chunks from uploaded PDF documents

---

## FastAPI Endpoints

### 1. Upload PDF

**POST Endpoint**

```http
POST /upload
```

Purpose:

* Uploads a PDF file.
* Enqueues `loading_file()` job.

Response:

```json
{
  "status": "queued",
  "job_id": "123456"
}
```

---

### 2. Query Documents

**POST Endpoint**

```http
POST /query
```

Purpose:

* Accepts a user query.
* Enqueues `retrieve_info()` job.

Request:

```json
{
  "query": "What skills are mentioned in the resume?"
}
```

Response:

```json
{
  "status": "queued",
  "job_id": "abcd1235Eelf"
}
```

---

### 3. Get Job Status

**GET Endpoint**

```http
GET /job/{job_id}
```

Purpose:

* Checks the status of a queued or completed job.
* Returns the final result when processing is complete.

Possible Status Values:

* queued
* started
* finished
* failed

Example Response:

```json
{
  "status": "finished",
  "result": "Skills extracted from the document..."
}
```

---
## RAG Pipeline

PDF Upload
    ↓
Text Extraction
    ↓
Chunking
    ↓
OpenAI Embeddings
    ↓
Qdrant Vector Storage
    ↓
User Query
    ↓
Query Embedding Generation
    ↓
Similarity Search (Qdrant)
    ↓
CrossEncoder Re-ranking
    ↓
Top Relevant Chunks
    ↓
Prompt Construction
    ↓
OpenAI LLM
    ↓
Generated Response
---

## Technologies Used

* Python
* FastAPI
* Redis
* Redis Queue (RQ)
* OpenAI Embeddings
* Qdrant Vector Database
* PDF Processing Libraries

---

## Running the Project

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start Infrastructure

```bash
docker-compose up -d
```

### Run FastAPI Server

```bash
uvicorn app.server.main:app --reload
```

### Start RQ Worker

```bash
rq worker --worker-class rq.worker.SimpleWorker default             #here for running up of workers in windows i used this command 
```

---

## Key Features

* PDF Upload and Processing
* Asynchronous Background Jobs
* Vector Embedding Generation
* Qdrant Vector Storage
- Semantic search using vector similarity
- Cross-Encoder re-ranking for improved retrieval accuracy
- Context-aware question answering
* FastAPI REST APIs
* Job Status Tracking

---

## Future Improvements

* Multi-document support
* Multiple collections
* Conversational chat interface

