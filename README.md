# 🧠 RAG-Based AI Document Assistant

## Intelligent PDF Knowledge Assistant

**Project Type:** AI Engineering / NLP / Information Retrieval / RAG
**Primary Language:** Python
**Development Period:** September 2026 → 2027
**Primary Goal:** Build a production-quality Retrieval-Augmented Generation system that allows users to upload documents, ask questions, retrieve relevant evidence, and receive grounded answers with source citations.

---

# 1. Project Vision

The goal is **not** to build another basic "Chat with PDF" application.

The goal is to build a complete **Retrieval-Augmented Generation (RAG) system** that demonstrates understanding of:

* Natural Language Processing
* Information Retrieval
* Vector databases
* Embeddings
* Semantic search
* Large Language Models
* Prompt engineering
* Retrieval evaluation
* Generation evaluation
* Hallucination detection
* API design
* Software architecture
* Docker deployment
* Experimental methodology

The final system should answer questions using information contained in uploaded documents and clearly identify where each answer came from.

---

# 2. Final Product

The final application should work approximately like this:

```text
                    ┌──────────────────────┐
                    │       User           │
                    │                      │
                    │ Upload PDF / Ask Q   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FastAPI         │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌────────────────┐          ┌─────────────────┐
       │ Document       │          │ Question        │
       │ Processing     │          │ Processing      │
       └───────┬────────┘          └────────┬────────┘
               │                            │
               ▼                            ▼
       ┌────────────────┐          ┌─────────────────┐
       │ Text           │          │ Query           │
       │ Extraction     │          │ Embedding       │
       └───────┬────────┘          └────────┬────────┘
               │                            │
               ▼                            ▼
       ┌────────────────┐          ┌─────────────────┐
       │ Chunking       │          │ Vector Search   │
       └───────┬────────┘          └────────┬────────┘
               │                            │
               ▼                            │
       ┌────────────────┐                    │
       │ Embeddings     │                    │
       └───────┬────────┘                    │
               │                            │
               ▼                            ▼
       ┌────────────────────────────────────────────┐
       │              Vector Database               │
       │                 Qdrant                     │
       └──────────────────────┬─────────────────────┘
                              │
                              ▼
                   ┌────────────────────┐
                   │ Relevant Chunks    │
                   │ + Metadata         │
                   └─────────┬──────────┘
                             │
                             ▼
                   ┌────────────────────┐
                   │       LLM          │
                   │ Context + Question │
                   └─────────┬──────────┘
                             │
                             ▼
                   ┌────────────────────┐
                   │ Answer + Citations │
                   └────────────────────┘
```

---

# 3. Core Features

## MVP

The first working version must support:

* PDF upload
* PDF text extraction
* Text cleaning
* Document chunking
* Embedding generation
* Vector storage
* Similarity search
* Question answering
* LLM integration
* Source citations

---

# 4. Advanced Features

The final system should additionally support:

### Document management

* Multiple PDFs
* Document IDs
* Metadata
* Document deletion
* Duplicate detection
* Processing status

### Retrieval

* Semantic search
* Configurable `top_k`
* Similarity threshold
* Metadata filtering
* Hybrid retrieval
* Reranking

### Generation

* Context-aware prompts
* Citation generation
* Conversation history
* "I don't know" behavior
* Hallucination mitigation

### Evaluation

* Retrieval metrics
* Generation metrics
* Recall@K
* Precision@K
* MRR
* Faithfulness
* Answer relevance
* Citation correctness

### Engineering

* REST API
* Unit tests
* Integration tests
* Logging
* Configuration management
* Docker
* Docker Compose
* CI/CD
* API documentation

---

# 5. Recommended Technology Stack

## Backend

Python

FastAPI

Pydantic

SQLAlchemy

---

## Document Processing

Start simple:

```text
PyMuPDF
```

Later experiment with:

```text
Unstructured
pypdf
```

---

## Text Chunking

Initial implementation:

```text
Recursive Character Text Splitter
```

Then experiment with:

* fixed-size chunks
* sentence-based chunks
* paragraph-based chunks
* semantic chunking

---

## Embeddings

Start with a Hugging Face sentence-transformer model.

Example:

```text
BAAI/bge-small-en-v1.5
```

Later compare against:

```text
BAAI/bge-base-en-v1.5
```

and an API-based embedding model if desired.

---

## Vector Database

Recommended:

```text
Qdrant
```

Alternatives:

```text
FAISS
Chroma
```

Use Qdrant for the final system because it gives the project a more production-oriented architecture.

---

## LLM

Use an API-based LLM initially.

Keep the LLM behind an abstraction layer so the system can later support:

```text
OpenAI
Anthropic
Google
Ollama
Hugging Face
```

---

## API

```text
FastAPI
```

---

## Frontend

Start with:

```text
Streamlit
```

Then optionally build:

```text
React + TypeScript
```

for the final version.

---

## Infrastructure

```text
Docker
Docker Compose
GitHub Actions
```

---

# 6. Project Architecture

Recommended final architecture:

```text
rag-document-assistant/
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── documents.py
│   │   │   ├── chat.py
│   │   │   ├── search.py
│   │   │   └── health.py
│   │   │
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── exceptions.py
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── cleaner.py
│   │   ├── chunker.py
│   │   └── pipeline.py
│   │
│   ├── embeddings/
│   │   ├── base.py
│   │   ├── huggingface.py
│   │   └── factory.py
│   │
│   ├── retrieval/
│   │   ├── vector_store.py
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── hybrid.py
│   │
│   ├── generation/
│   │   ├── llm.py
│   │   ├── prompts.py
│   │   └── answer.py
│   │
│   ├── evaluation/
│   │   ├── datasets.py
│   │   ├── retrieval.py
│   │   ├── generation.py
│   │   └── metrics.py
│   │
│   ├── models/
│   │   ├── document.py
│   │   ├── chunk.py
│   │   └── conversation.py
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── evaluation/
│   ├── datasets/
│   ├── experiments/
│   └── results/
│
├── scripts/
│   ├── ingest.py
│   ├── evaluate.py
│   └── benchmark.py
│
├── frontend/
│
├── docker/
│
├── docs/
│
├── notebooks/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── PROJECT_PLAN.md
```

---

# 7. Development Phases

The project will be developed in 10 phases.

```text
Phase 0  → Planning & Environment
Phase 1  → PDF Processing
Phase 2  → Chunking Pipeline
Phase 3  → Embeddings
Phase 4  → Vector Database
Phase 5  → Retrieval
Phase 6  → RAG Generation
Phase 7  → Citations & Conversations
Phase 8  → Evaluation & Research
Phase 9  → Production API & UI
Phase 10 → Docker, Deployment & Portfolio
```

---

# PHASE 0 — Planning & Environment

## Objective

Prepare the development environment and understand the architecture before writing the RAG system.

---

## Tasks

### 0.1 Install

Install:

* Python 3.11+
* Git
* VS Code
* Docker Desktop
* Postman or Insomnia

---

## 0.2 Create repository

```bash
mkdir rag-document-assistant

cd rag-document-assistant

git init
```

---

## 0.3 Create virtual environment

Windows:

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 0.4 Create initial dependencies

```bash
pip install fastapi uvicorn
pip install pymupdf
pip install sentence-transformers
pip install qdrant-client
pip install pydantic-settings
pip install python-multipart
pip install python-dotenv
```

Later add the LLM SDK and LangChain/LlamaIndex components only when needed.

---

## 0.5 Create first Git commit

```bash
git add .

git commit -m "chore: initialize project"
```

---

## Deliverables

By the end of Phase 0:

```text
✓ Repository
✓ Python environment
✓ Dependency management
✓ Project structure
✓ README
✓ Git workflow
✓ Architecture diagram
```

---

# PHASE 1 — PDF DOCUMENT PROCESSING

## Objective

Build the ingestion pipeline.

Input:

```text
PDF
```

Output:

```text
Document
    ↓
Pages
    ↓
Clean text
    ↓
Metadata
```

---

# 1.1 PDF extraction

Use PyMuPDF.

The system should extract:

```text
document_id
filename
page_number
text
```

Example internal representation:

```python
{
    "document_id": "doc_123",
    "page": 4,
    "text": "Machine learning is..."
}
```

---

# 1.2 Metadata

Every extracted page should maintain metadata:

```text
document_id
filename
page_number
title
source
```

This becomes extremely important later for citations.

---

# 1.3 Text cleaning

Implement:

* whitespace normalization
* repeated newline removal
* header/footer handling
* empty page detection
* malformed character cleanup

Do not aggressively modify the text.

The original document should remain recoverable.

---

# 1.4 Document ingestion pipeline

Build:

```text
upload
   ↓
validate PDF
   ↓
extract pages
   ↓
clean text
   ↓
store metadata
   ↓
return document ID
```

---

## Deliverable

A script such as:

```bash
python scripts/ingest.py example.pdf
```

should produce:

```text
Document processed successfully

Document ID: abc123
Pages: 42
Characters: 183,421
```

---

# PHASE 2 — CHUNKING

## Objective

Convert documents into retrieval-friendly pieces.

```text
Document
    ↓
Pages
    ↓
Chunks
```

---

# 2.1 Why chunking matters

LLMs and vector databases should not receive an entire 200-page PDF for every question.

Instead:

```text
PDF
 ↓
1000 chunks
 ↓
retrieve 5 relevant chunks
 ↓
send only those chunks to LLM
```

---

# 2.2 Baseline chunking

Start with:

```text
chunk_size = 500–1000 tokens
overlap = 50–150 tokens
```

Do not treat these values as final.

They become experimental variables later.

---

# 2.3 Store chunk metadata

Each chunk should contain:

```text
chunk_id
document_id
page_number
chunk_index
text
```

Example:

```json
{
  "chunk_id": "chunk_982",
  "document_id": "doc_123",
  "page_number": 15,
  "chunk_index": 31,
  "text": "Gradient descent is..."
}
```

---

# 2.4 Chunking experiments

Later compare:

```text
Experiment A
chunk = 300 tokens

Experiment B
chunk = 500 tokens

Experiment C
chunk = 800 tokens

Experiment D
chunk = 1200 tokens
```

Measure retrieval performance.

This is where the project starts becoming research-oriented.

---

## Deliverable

A reusable:

```text
Chunker
```

with configurable parameters.

---

# PHASE 3 — EMBEDDINGS

## Objective

Convert text into numerical vectors.

Concept:

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Example:

```text
"Machine learning uses data"
              ↓
[0.012, -0.238, 0.451, ...]
```

---

# 3.1 Understand embeddings

Study:

* semantic similarity
* vector representations
* cosine similarity
* dot product
* Euclidean distance
* embedding dimensions

You should understand these mathematically.

---

# 3.2 Implement embedding service

Create an abstraction:

```python
class EmbeddingModel:
    def embed_documents(self, texts):
        ...

    def embed_query(self, query):
        ...
```

This allows you to change models later without rewriting the system.

---

# 3.3 Initial model

Start with a lightweight Hugging Face embedding model.

For example:

```text
BAAI/bge-small-en-v1.5
```

---

# 3.4 Embedding experiments

Compare models.

Example:

```text
Model A → BGE Small
Model B → BGE Base
Model C → API embedding model
```

Record:

```text
embedding dimension
latency
memory usage
retrieval Recall@K
MRR
cost
```

---

# PHASE 4 — VECTOR DATABASE

## Objective

Store and search embeddings.

Recommended:

```text
Qdrant
```

Architecture:

```text
Chunk
 ↓
Embedding
 ↓
Qdrant
```

---

# 4.1 Start Qdrant

Use Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Later use Docker Compose.

---

# 4.2 Collection

Create a collection:

```text
documents
```

Each point contains:

```text
vector
payload
```

Payload:

```json
{
    "document_id": "doc_123",
    "filename": "machine_learning.pdf",
    "page": 15,
    "chunk_id": "chunk_31",
    "text": "..."
}
```

---

# 4.3 Similarity search

Input:

```text
"What is gradient descent?"
```

Convert question into vector.

Then:

```text
query vector
      ↓
Qdrant
      ↓
Top K chunks
```

---

# PHASE 5 — RETRIEVAL ENGINE

## Objective

Build a proper information retrieval system.

This phase is extremely important for your Master's applications.

---

# 5.1 Baseline retrieval

Implement:

```text
query
 ↓
embedding
 ↓
vector search
 ↓
top_k results
```

---

# 5.2 Retrieval parameters

Make configurable:

```text
top_k
score_threshold
collection
filters
```

Example:

```text
top_k = 5
```

---

# 5.3 Retrieval result

Return:

```json
{
    "chunk_id": "chunk_42",
    "score": 0.87,
    "text": "...",
    "document": "ml.pdf",
    "page": 18
}
```

---

# 5.4 Retrieval evaluation

Create a dataset:

```text
Question
Expected document
Expected page/chunk
```

Example:

```json
{
  "question": "What is gradient descent?",
  "relevant_chunks": [
      "chunk_42",
      "chunk_43"
  ]
}
```

---

# 5.5 Metrics

Implement:

### Recall@K

Measures whether relevant information appears in the top K results.

```text
Recall@1
Recall@3
Recall@5
Recall@10
```

---

### Precision@K

Measures how many retrieved results are relevant.

---

### MRR

Mean Reciprocal Rank.

Useful for measuring where the first relevant result appears.

---

### Hit Rate

Measures whether at least one relevant result appears.

---

# 5.6 Retrieval experiment

Run experiments such as:

```text
Experiment 1
chunk = 500
top_k = 3

Experiment 2
chunk = 500
top_k = 5

Experiment 3
chunk = 1000
top_k = 5

Experiment 4
chunk = 1000
top_k = 10
```

Record results in:

```text
evaluation/results/
```

---

# PHASE 6 — RAG GENERATION

## Objective

Connect retrieval to an LLM.

Architecture:

```text
Question
   ↓
Retriever
   ↓
Relevant chunks
   ↓
Prompt construction
   ↓
LLM
   ↓
Answer
```

---

# 6.1 Context construction

Example:

```text
SYSTEM:

You are a document question-answering assistant.

Answer the user's question using only the supplied context.

If the context does not contain enough information,
say that you do not have enough information.

Always cite the sources used.
```

Then:

```text
CONTEXT:

[Source 1]
Document: ML.pdf
Page: 12

...

[Source 2]
Document: ML.pdf
Page: 15

...
```

Then:

```text
QUESTION:

What is gradient descent?
```

---

# 6.2 Grounded answering

The model must not answer based purely on its general knowledge.

The target behavior is:

```text
Context contains answer
        ↓
Answer

Context doesn't contain answer
        ↓
"I couldn't find sufficient information in the documents."
```

---

# 6.3 Hallucination protection

Implement:

* strict system prompt
* context-only answering
* relevance threshold
* "insufficient evidence" response
* source citation requirement

---

# 6.4 LLM abstraction

Create:

```python
class LLM:
    def generate(self, prompt):
        ...
```

Then implementations can include:

```text
OpenAI
Ollama
Hugging Face
Anthropic
```

---

# PHASE 7 — CITATIONS + CONVERSATION MEMORY

## Objective

Make the assistant genuinely useful.

---

# 7.1 Source citations

Every answer should contain citations.

Example:

```text
Gradient descent is an optimization algorithm that
iteratively updates model parameters to minimize a
loss function.

[Source: Machine Learning.pdf, Page 15]
```

---

# 7.2 Citation metadata

Each source should contain:

```text
document
page
chunk
similarity score
```

---

# 7.3 Multiple documents

The user should be able to upload:

```text
paper1.pdf
paper2.pdf
thesis.pdf
lecture_notes.pdf
```

Then ask:

```text
Compare the approaches described in the papers.
```

---

# 7.4 Conversation history

Support:

```text
User:
What is gradient descent?

Assistant:
...

User:
What are its limitations?

Assistant:
...
```

The second question should understand the conversation context.

---

# 7.5 Conversation architecture

```text
Conversation
   │
   ├── Message
   ├── Message
   ├── Message
   │
   └── Retrieved Context
```

---

# PHASE 8 — EVALUATION + RESEARCH

## Objective

This is the phase that transforms the project from an application into a serious academic/engineering project.

---

# 8.1 Create evaluation dataset

Create approximately:

```text
50–100 questions
```

Initially.

Questions should cover:

* factual questions
* multi-hop questions
* comparison questions
* definition questions
* numerical questions
* questions with no answer in documents
* ambiguous questions

---

# 8.2 Ground-truth data

Each question should have:

```text
question
expected answer
relevant document
relevant page
relevant chunk
```

---

# 8.3 Retrieval evaluation

Measure:

```text
Recall@1
Recall@3
Recall@5
Recall@10

Precision@K

MRR

Hit Rate
```

---

# 8.4 Generation evaluation

Measure:

### Faithfulness

Does the answer actually follow from the retrieved context?

---

### Answer relevance

Does the answer address the question?

---

### Citation correctness

Do citations actually support the claims?

---

### Context relevance

Did the retriever provide useful information?

---

# 8.5 Hallucination evaluation

Create questions where the answer does not exist.

Example:

```text
Document:
Information about neural networks.

Question:
What is the population of Mars?
```

Expected:

```text
I cannot find this information in the provided documents.
```

The system should not invent an answer.

---

# 8.6 Major research experiments

This is where you should spend significant time.

## Experiment 1 — Chunk size

Compare:

```text
300
500
800
1000
1500 tokens
```

Measure:

```text
Recall@5
MRR
Answer quality
Latency
```

---

## Experiment 2 — Chunk overlap

Compare:

```text
0%
10%
20%
```

---

## Experiment 3 — Embedding models

Compare:

```text
BGE-small
BGE-base
API embedding
```

---

## Experiment 4 — Top K

Compare:

```text
K = 1
K = 3
K = 5
K = 10
```

---

## Experiment 5 — Reranking

Baseline:

```text
Vector search
```

Improved:

```text
Vector search
      ↓
Reranker
      ↓
Top results
```

Compare the two approaches.

---

## Experiment 6 — Hybrid retrieval

Compare:

```text
Dense retrieval
```

against:

```text
Dense + keyword retrieval
```

---

# 8.7 Research question

Your project can eventually investigate:

> **How do chunking strategies, embedding models, and retrieval configurations affect the accuracy and faithfulness of Retrieval-Augmented Generation systems for technical documents?**

This is a legitimate research-oriented question.

---

# PHASE 9 — PRODUCTION API + FRONTEND

## Objective

Turn the research prototype into a real application.

---

# 9.1 FastAPI endpoints

Implement:

```http
POST /documents/upload
```

Upload PDF.

---

```http
GET /documents
```

List documents.

---

```http
GET /documents/{document_id}
```

Get document information.

---

```http
DELETE /documents/{document_id}
```

Delete document.

---

```http
POST /search
```

Search documents.

---

```http
POST /chat
```

Ask a question.

---

```http
GET /conversations/{conversation_id}
```

Get conversation history.

---

```http
GET /health
```

Health check.

---

# 9.2 API response

Example:

```json
{
  "answer": "Gradient descent is...",
  "sources": [
    {
      "document": "machine_learning.pdf",
      "page": 15,
      "chunk_id": "chunk_42",
      "score": 0.91
    }
  ]
}
```

---

# 9.3 Frontend

Initial frontend:

```text
Streamlit
```

Interface:

```text
┌─────────────────────────────────────┐
│       Intelligent Document AI       │
├─────────────────────────────────────┤
│                                     │
│ Upload Documents                    │
│ [ Upload PDF ]                      │
│                                     │
│ Documents                           │
│ ✓ ML.pdf                            │
│ ✓ NLP.pdf                           │
│ ✓ Research.pdf                      │
│                                     │
├─────────────────────────────────────┤
│ Chat                                │
│                                     │
│ You: What is gradient descent?      │
│                                     │
│ AI: Gradient descent is...          │
│                                     │
│ Sources:                            │
│ ML.pdf — Page 15                    │
│                                     │
│ [ Ask a question... ]               │
└─────────────────────────────────────┘
```

---

# PHASE 10 — DOCKER + DEPLOYMENT + PORTFOLIO

## Objective

Deploy the complete system professionally.

---

# 10.1 Docker services

Final architecture:

```text
Docker Compose

├── backend
├── frontend
├── qdrant
└── database
```

---

# 10.2 Dockerfile

Build backend:

```text
Python
 ↓
Dependencies
 ↓
FastAPI
 ↓
Application
```

---

# 10.3 Environment variables

Never commit API keys.

Use:

```text
.env
```

Example:

```env
LLM_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
DATABASE_URL=
```

Commit:

```text
.env.example
```

but never:

```text
.env
```

---

# 10.4 Logging

Log:

```text
document upload
processing time
chunk count
embedding latency
retrieval latency
LLM latency
total request latency
errors
```

Example:

```text
INFO document_processed
document_id=123
pages=42
chunks=387
processing_time=4.21s
```

---

# 10.5 Observability

Track:

```text
retrieval latency
LLM latency
total latency
tokens
cost
retrieval scores
```

This allows proper system analysis.

---

# 10.6 Testing

Implement:

## Unit tests

Test:

```text
PDF extraction
cleaning
chunking
embedding
retrieval
prompt construction
```

---

## Integration tests

Test:

```text
PDF
 ↓
ingestion
 ↓
chunking
 ↓
embedding
 ↓
Qdrant
 ↓
retrieval
 ↓
LLM
```

---

# 11. Development Workflow

Do not build everything at once.

Use this progression:

```text
Week 1
Environment + architecture

Week 2
PDF processing

Week 3
Chunking

Week 4
Embeddings

Week 5
Vector database

Week 6
Retrieval

Week 7
RAG generation

Week 8
Citations + conversations

Week 9–11
Evaluation

Week 12–13
Experiments

Week 14
FastAPI

Week 15
Frontend

Week 16
Docker

Week 17
Deployment

Week 18
Documentation + paper
```

This is approximately an 18-week roadmap.

---

# 12. What You Should Study Alongside the Project

Do not blindly copy RAG tutorials.

Study the concepts behind every component.

---

## NLP

Study:

* tokenization
* TF-IDF
* BM25
* word embeddings
* contextual embeddings
* transformers
* attention

---

## Information Retrieval

Study:

* inverted index
* TF-IDF
* BM25
* dense retrieval
* vector similarity
* cosine similarity
* precision
* recall
* MRR
* ranking

---

## Machine Learning

Study:

* vectors
* matrices
* optimization
* probability
* similarity
* classification
* evaluation

---

## Deep Learning

Study:

* neural networks
* backpropagation
* transformers
* attention
* encoder/decoder architecture

---

## LLMs

Study:

* tokenization
* context window
* prompting
* temperature
* hallucination
* instruction tuning
* embeddings

---

# 13. Git Strategy

Use meaningful commits.

Bad:

```text
update
fix
changes
test
```

Good:

```text
feat: add pdf text extraction
feat: implement recursive chunking
feat: add embedding service
feat: integrate qdrant vector store
feat: implement semantic retrieval
feat: add rag generation pipeline
feat: add source citations
feat: add retrieval evaluation
feat: add reranking experiment
test: add ingestion pipeline tests
docs: document retrieval experiments
```

---

# 14. GitHub Repository

Your README should contain:

```text
# Intelligent PDF Knowledge Assistant

## Overview

## Architecture

## Features

## Tech Stack

## Installation

## Usage

## API

## Evaluation

## Experiments

## Results

## Limitations

## Future Work

## Research Question

## License
```

---

# 15. README Architecture Diagram

Include:

```text
                ┌───────────────┐
                │      User     │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │    FastAPI    │
                └───────┬───────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       Document Pipeline       Query Pipeline
              │                   │
              ▼                   ▼
          Chunking             Embedding
              │                   │
              ▼                   ▼
         Embeddings          Vector Search
              │                   │
              └─────────┬─────────┘
                        ▼
                  Retrieved Context
                        │
                        ▼
                       LLM
                        │
                        ▼
                Answer + Citations
```

---

# 16. Final Research Report

At the end, create:

```text
research_report.pdf
```

Suggested structure:

## Abstract

Briefly explain the system and findings.

---

## 1. Introduction

Explain:

* LLMs
* hallucinations
* RAG
* motivation

---

## 2. Related Concepts

Discuss:

* information retrieval
* embeddings
* vector search
* RAG

---

## 3. System Architecture

Explain every component.

---

## 4. Methodology

Describe:

* datasets
* chunking
* embeddings
* retrieval
* LLM
* evaluation

---

## 5. Experiments

Compare:

```text
chunk sizes
embedding models
top-k
reranking
hybrid retrieval
```

---

## 6. Results

Use tables and graphs.

Example:

| Configuration | Recall@5 |  MRR | Faithfulness |
| ------------- | -------: | ---: | -----------: |
| 500 chunk     |     0.82 | 0.71 |         0.86 |
| 800 chunk     |     0.87 | 0.76 |         0.89 |
| 1000 chunk    |     0.84 | 0.74 |         0.87 |

These numbers are examples only. Your actual experiments must produce the real values.

---

## 7. Error Analysis

Study failure cases.

Examples:

```text
Wrong chunk retrieved

Correct chunk ranked too low

Question requires multiple chunks

LLM ignored retrieved context

Citation doesn't support claim

Document contains tables

PDF extraction failed
```

This section is extremely valuable.

---

## 8. Limitations

Be honest.

Possible limitations:

* scanned PDFs
* tables
* images
* OCR
* long-context questions
* multilingual documents
* retrieval failures
* LLM hallucinations

---

## 9. Future Work

Possible improvements:

* multimodal RAG
* OCR
* table extraction
* graph RAG
* hybrid retrieval
* better rerankers
* agentic retrieval
* multilingual RAG

---

# 17. Advanced Version

After completing the baseline, consider:

```text
                   RAG SYSTEM
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
    Dense           Sparse           Hybrid
  Retrieval        Retrieval        Retrieval
       │               │                │
       └───────────────┼────────────────┘
                       ▼
                    Reranker
                       │
                       ▼
                 Context Builder
                       │
                       ▼
                      LLM
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
          Answer              Citations
```

---

# 18. Possible Advanced Research

Once the baseline works, investigate:

## Research Question 1

> How does chunk size affect retrieval quality in technical PDF documents?

---

## Research Question 2

> How does embedding model selection affect RAG performance?

---

## Research Question 3

> Does reranking significantly improve answer faithfulness?

---

## Research Question 4

> How does hybrid retrieval compare with dense retrieval for technical documents?

---

## Research Question 5

> What retrieval configuration provides the best accuracy-latency tradeoff?

---

# 19. Portfolio Presentation

Your GitHub project should demonstrate three things.

## Engineering

```text
Python
FastAPI
Qdrant
Docker
Testing
API
```

## AI

```text
Embeddings
Vector Search
RAG
LLMs
Reranking
Prompting
```

## Research

```text
Experiments
Evaluation
Metrics
Error Analysis
Ablation Studies
```

The combination is much stronger than simply saying:

> "I built a chatbot using LangChain."

---

# 20. CV Description

After completing the project, a strong CV description could look like:

**Intelligent PDF Knowledge Assistant — RAG / NLP / Information Retrieval**

* Designed and implemented a Retrieval-Augmented Generation system for multi-document question answering using Python, FastAPI, Hugging Face embeddings, Qdrant, and LLMs.
* Developed an end-to-end document ingestion pipeline with PDF extraction, configurable chunking, semantic embeddings, vector retrieval, contextual generation, and source-level citations.
* Conducted controlled experiments comparing chunk sizes, embedding models, retrieval depth, and reranking strategies using Recall@K, Precision@K, MRR, faithfulness, and answer relevance metrics.
* Investigated retrieval failures and hallucination cases through systematic error analysis and developed context-grounded response mechanisms to reduce unsupported answers.
* Containerized the system using Docker and exposed document ingestion, retrieval, and conversational QA functionality through a RESTful FastAPI service.

Use the actual metrics you obtain once the experiments are complete.

---

# 21. Master's Application Value

This project can demonstrate experience across several areas:

```text
Machine Learning
       +
Natural Language Processing
       +
Information Retrieval
       +
LLMs
       +
Software Engineering
       +
Research Methodology
```

For a research-oriented Master's application, the most valuable part is **not the UI**.

The strongest evidence will be:

```text
1. Clear research question
2. Reproducible experiments
3. Evaluation dataset
4. Quantitative metrics
5. Baselines
6. Ablation studies
7. Error analysis
8. Technical report
9. Clean GitHub repository
10. Working deployed system
```

---

# 22. Definition of Done

The project is considered complete only when:

## Core System

* [ ] PDF upload works
* [ ] PDF extraction works
* [ ] Text cleaning works
* [ ] Chunking works
* [ ] Embeddings work
* [ ] Qdrant works
* [ ] Semantic search works
* [ ] LLM generation works
* [ ] Citations work

## Advanced RAG

* [ ] Multiple documents
* [ ] Conversation history
* [ ] Metadata filtering
* [ ] Configurable top-k
* [ ] Similarity threshold
* [ ] Reranking
* [ ] Hybrid retrieval

## Evaluation

* [ ] Evaluation dataset
* [ ] Recall@K
* [ ] Precision@K
* [ ] MRR
* [ ] Hit Rate
* [ ] Faithfulness
* [ ] Answer relevance
* [ ] Citation evaluation
* [ ] Hallucination tests

## Research

* [ ] Chunk-size experiment
* [ ] Embedding experiment
* [ ] Top-k experiment
* [ ] Reranking experiment
* [ ] Hybrid retrieval experiment
* [ ] Error analysis
* [ ] Results visualization
* [ ] Research report

## Engineering

* [ ] FastAPI
* [ ] Tests
* [ ] Logging
* [ ] Configuration
* [ ] Docker
* [ ] Docker Compose
* [ ] CI/CD
* [ ] Documentation

## Portfolio

* [ ] Clean GitHub repository
* [ ] Architecture diagram
* [ ] README
* [ ] Demo
* [ ] Technical report
* [ ] Research results
* [ ] CV entry
* [ ] Project screenshots

---

# 23. Most Important Rule

Do **not** start by installing LangChain and copying a tutorial.

Build the system progressively.

The learning path should be:

```text
PDF
 ↓
Text
 ↓
Chunks
 ↓
Embeddings
 ↓
Vector Search
 ↓
Retrieval
 ↓
LLM
 ↓
RAG
 ↓
Citations
 ↓
Evaluation
 ↓
Experiments
 ↓
Production System
```

You should understand every arrow in this diagram.

---

# 24. Final Architecture

The completed project should look approximately like:

```text
                           USER
                            │
              ┌─────────────┴─────────────┐
              │                           │
         Upload PDFs                 Ask Question
              │                           │
              ▼                           ▼
       Document Pipeline            Query Pipeline
              │                           │
         PDF Extraction               Query Embed
              │                           │
          Cleaning                        │
              │                           │
          Chunking                        │
              │                           │
          Embeddings                      │
              │                           │
              ▼                           ▼
        ┌──────────────────────────────────────┐
        │              QDRANT                  │
        │                                      │
        │  vectors + metadata + source text    │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                      Retrieval
                           │
                           ▼
                       Reranking
                           │
                           ▼
                    Context Builder
                           │
                           ▼
                          LLM
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
               Answer             Sources
                 │                   │
                 └─────────┬─────────┘
                           ▼
                      Final Response
```

---

# 25. Recommended Starting Point

Do not implement Phase 1–10 simultaneously.

Start with exactly this:

```text
Phase 0
   ↓
Create repository
   ↓
Create virtual environment
   ↓
Create project structure
   ↓
Install dependencies
   ↓
Create FastAPI hello-world
   ↓
Commit to Git
   ↓
Phase 1
```

Then build the PDF processor.

The first milestone should simply be:

```bash
python scripts/ingest.py example.pdf
```

and:

```text
PDF processed successfully

Document ID: doc_001
Pages: 27
Characters: 91,432
```

Once that works reliably, move to chunking.

---

# 26. Project Philosophy

The project should evolve through three stages:

```text
                    ┌─────────────────┐
                    │   Stage 1       │
                    │   Working MVP   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Stage 2       │
                    │   Strong RAG    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Stage 3       │
                    │ Research +      │
                    │ Production      │
                    └─────────────────┘
```

### Stage 1

Make it work.

### Stage 2

Make retrieval and generation good.

### Stage 3

Measure it, experiment with it, explain failures, and deploy it.

**Stage 3 is what makes this project valuable for a research-oriented Master's application.**

---

# END OF PROJECT PLAN

