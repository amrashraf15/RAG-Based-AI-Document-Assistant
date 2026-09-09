# 🧠 RAG-Based AI Document Assistant

> **A production-oriented Retrieval-Augmented Generation (RAG) system for grounded question answering over user-uploaded documents, with semantic retrieval, source citations, evaluation, and deployment support.**

---

## 📌 Overview

The **RAG-Based AI Document Assistant** is an AI engineering project designed to go beyond a basic **"Chat with PDF"** application.

The system combines:

* Natural Language Processing
* Information Retrieval
* Embeddings
* Vector Databases
* Large Language Models
* Retrieval and generation evaluation
* Production software engineering

The core objective is simple:

> **Retrieve the right evidence, generate a grounded answer, and show the user where the answer came from.**

The project is being developed progressively from a working MVP into a stronger RAG system and finally into a research-oriented, production-ready application.

---

## 🎯 Why This Project?

Many document QA systems focus primarily on connecting an LLM to a PDF.

This project focuses on understanding and evaluating the **complete RAG pipeline**:

* Document ingestion
* PDF text extraction
* Text cleaning
* Chunking
* Embedding generation
* Vector search
* Retrieval configuration
* Reranking
* Context construction
* LLM generation
* Source citations
* Hallucination mitigation
* Quantitative evaluation
* Error analysis
* API design
* Testing
* Docker deployment

This makes the project both an **AI engineering portfolio project** and a foundation for **research into RAG retrieval and generation quality**.

---

# 🏗️ Architecture

```text
                              USER
                               │
              ┌────────────────┴────────────────┐
              │                                 │
         Upload PDFs                       Ask Question
              │                                 │
              ▼                                 ▼
      Document Pipeline                   Query Pipeline
              │                                 │
        PDF Extraction                    Query Embedding
              │                                 │
          Cleaning                              │
              │                                 │
          Chunking                              │
              │                                 │
         Embeddings                             │
              │                                 │
              ▼                                 ▼
       ┌────────────────────────────────────────────┐
       │                   QDRANT                   │
       │                                            │
       │        Vectors + Metadata + Text           │
       └──────────────────────┬─────────────────────┘
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

# ✨ Core Features

## 📄 Document Processing

* PDF upload and validation
* PDF text extraction with PyMuPDF
* Text cleaning and normalization
* Page-level metadata preservation
* Document IDs
* Processing status
* Multiple-document support
* Document deletion
* Duplicate detection

## 🔎 Retrieval

* Semantic vector search
* Configurable `top_k`
* Similarity thresholds
* Metadata filtering
* Dense retrieval
* Reranking
* Hybrid retrieval experiments

## 🤖 Generation

* Context-aware prompting
* Context-only answering
* Source citations
* Conversation history
* "Insufficient evidence" behavior
* Hallucination mitigation
* LLM abstraction layer

## 📊 Evaluation & Research

The system is designed to support quantitative evaluation using:

* Recall@K
* Precision@K
* MRR
* Hit Rate
* Faithfulness
* Answer relevance
* Citation correctness
* Context relevance
* Hallucination tests
* Error analysis
* Ablation / controlled experiments

---

# 🛠️ Technology Stack

| Layer                      | Technology                                 |
| -------------------------- | ------------------------------------------ |
| Language                   | Python 3.11+                               |
| API                        | FastAPI                                    |
| Validation / Configuration | Pydantic / Pydantic Settings               |
| PDF Processing             | PyMuPDF                                    |
| Embeddings                 | Hugging Face Sentence Transformers         |
| Initial Embedding Model    | `BAAI/bge-small-en-v1.5`                   |
| Vector Database            | Qdrant                                     |
| LLM                        | API-based LLM through an abstraction layer |
| Initial Frontend           | Streamlit                                  |
| Optional Final Frontend    | React + TypeScript                         |
| Database / Persistence     | SQLAlchemy-compatible architecture         |
| Testing                    | Unit + Integration Tests                   |
| Containerization           | Docker                                     |
| Orchestration              | Docker Compose                             |
| CI/CD                      | GitHub Actions                             |

---

# 🔄 End-to-End RAG Pipeline

```text
PDF
 │
 ▼
Text Extraction
 │
 ▼
Text Cleaning
 │
 ▼
Chunking
 │
 ▼
Embedding Generation
 │
 ▼
Vector Storage
 │
 ▼
User Question
 │
 ▼
Query Embedding
 │
 ▼
Vector Retrieval
 │
 ▼
Optional Reranking
 │
 ▼
Context Construction
 │
 ▼
LLM
 │
 ▼
Grounded Answer + Citations
```

---

# 📁 Project Structure

The target architecture is organized around clear system boundaries:

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
├── docker/
├── docs/
├── notebooks/
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# 🌐 API

The production API is designed around the following endpoints:

| Method   | Endpoint                           | Purpose                         |
| -------- | ---------------------------------- | ------------------------------- |
| `POST`   | `/documents/upload`                | Upload and process a PDF        |
| `GET`    | `/documents`                       | List uploaded documents         |
| `GET`    | `/documents/{document_id}`         | Retrieve document information   |
| `DELETE` | `/documents/{document_id}`         | Delete a document               |
| `POST`   | `/search`                          | Search indexed document content |
| `POST`   | `/chat`                            | Ask a grounded question         |
| `GET`    | `/conversations/{conversation_id}` | Retrieve conversation history   |
| `GET`    | `/health`                          | Service health check            |

### Example Response

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

# 🎯 Grounded Generation

The assistant is designed to answer **from retrieved document context rather than relying blindly on the LLM's general knowledge**.

Conceptually:

```text
Relevant evidence exists
        │
        ▼
   Generate answer
        │
        ▼
   Return citations
```

When evidence is insufficient:

```text
Insufficient evidence
        │
        ▼
Do not fabricate an answer
        │
        ▼
Return an insufficient-evidence response
```

This behavior is reinforced through:

* Context-only prompting
* Retrieval score thresholds
* Citation requirements
* Explicit insufficient-evidence handling
* Retrieval evaluation
* Hallucination testing

---

# 🔬 Research & Experiments

A major objective is to make the system **measurable rather than relying only on subjective "it seems to work" evaluation**.

## Experiment 1 — Chunk Size

Compare:

```text
300
500
800
1000
1500 tokens
```

Measure:

* Recall@5
* MRR
* Answer quality
* Latency

---

## Experiment 2 — Chunk Overlap

Compare:

```text
0%
10%
20%
```

---

## Experiment 3 — Embedding Models

Compare:

```text
BGE-small
BGE-base
API-based embedding model
```

Track:

* Embedding dimension
* Latency
* Memory usage
* Recall@K
* MRR
* Cost

---

## Experiment 4 — Retrieval Depth

Compare:

```text
K = 1
K = 3
K = 5
K = 10
```

---

## Experiment 5 — Reranking

```text
Vector Search
      │
      ▼
  Reranker
      │
      ▼
 Top Results
```

Compare reranked retrieval against the baseline vector-search approach.

---

## Experiment 6 — Hybrid Retrieval

Compare:

```text
Dense Retrieval
```

against:

```text
Dense + Keyword Retrieval
```

---

# ❓ Research Question

The central research direction is:

> **How do chunking strategies, embedding models, and retrieval configurations affect the accuracy and faithfulness of Retrieval-Augmented Generation systems for technical documents?**

Additional research questions include:

1. How does chunk size affect retrieval quality in technical PDF documents?
2. How does embedding model selection affect RAG performance?
3. Does reranking significantly improve answer faithfulness?
4. How does hybrid retrieval compare with dense retrieval for technical documents?
5. What retrieval configuration provides the best accuracy-latency tradeoff?

---

# 📚 Evaluation Dataset

The evaluation framework is designed around an initial dataset of approximately **50–100 questions** covering:

* Factual questions
* Definition questions
* Comparison questions
* Multi-hop questions
* Numerical questions
* Ambiguous questions
* Questions with no answer in the documents

Each evaluation example should contain:

```text
Question
Expected Answer
Relevant Document
Relevant Page
Relevant Chunk
```

---

# 🧪 Error Analysis

Evaluation should not stop at aggregate metrics.

The project also investigates failure cases such as:

* Incorrect chunk retrieval
* Relevant chunk ranked too low
* Multi-chunk reasoning failures
* LLM ignoring retrieved context
* Unsupported citations
* PDF extraction failures
* Tables and structured content
* Long-context questions
* Insufficient-evidence detection failures

---

# ⚙️ Production Engineering

The final system is designed to include:

* RESTful API
* Input validation
* Configuration management
* Structured logging
* Unit tests
* Integration tests
* Docker
* Docker Compose
* CI/CD
* API documentation
* Environment-based secrets
* Latency monitoring
* Retrieval observability

### Environment Variables

```env
LLM_API_KEY=
QDRANT_URL=
QDRANT_API_KEY=
DATABASE_URL=
```

> `.env` files and secrets should never be committed to the repository. Use `.env.example` for documented configuration.

---

# 🐳 Docker Architecture

The target deployment architecture is:

```text
Docker Compose

├── backend
├── frontend
├── qdrant
└── database
```

The application will be containerized so the main services can be started consistently across development and deployment environments.

---

# 🗺️ Development Roadmap

The project is being developed through ten progressive phases:

| Phase | Focus                          |
| ----: | ------------------------------ |
|     0 | Planning & Environment         |
|     1 | PDF Processing                 |
|     2 | Chunking Pipeline              |
|     3 | Embeddings                     |
|     4 | Vector Database                |
|     5 | Retrieval                      |
|     6 | RAG Generation                 |
|     7 | Citations & Conversations      |
|     8 | Evaluation & Research          |
|     9 | Production API & UI            |
|    10 | Docker, Deployment & Portfolio |

### Current Focus

**Phase 10 — Docker, Deployment & Portfolio**

The project intentionally evolves from:

```text
Working MVP
     ↓
Strong RAG System
     ↓
Research + Production System
```

---

# 🎓 Learning Objectives

The project is also used as a structured learning vehicle for AI, NLP, Information Retrieval, and Machine Learning.

## NLP

* Tokenization
* TF-IDF
* BM25
* Word embeddings
* Contextual embeddings
* Transformers
* Attention

## Information Retrieval

* Inverted indexes
* Sparse retrieval
* Dense retrieval
* Vector similarity
* Ranking
* Precision
* Recall
* MRR

## Machine Learning

* Vectors and matrices
* Optimization
* Probability
* Similarity
* Classification
* Evaluation

## Deep Learning

* Neural networks
* Backpropagation
* Transformers
* Attention
* Encoder/decoder architectures

## LLMs

* Tokenization
* Context windows
* Prompting
* Temperature
* Hallucination
* Instruction tuning
* Embeddings

---

# 🧠 Engineering Principles

## 1. Understand Before Abstracting

Core RAG components are implemented and understood before relying heavily on high-level frameworks.

## 2. Measure Before Optimizing

Changes to chunking, embeddings, retrieval, and reranking should be evaluated quantitatively.

## 3. Preserve Source Traceability

Document metadata is retained throughout the pipeline so generated answers can be connected back to their sources.

## 4. Separate Components

Embeddings, retrieval, generation, configuration, and API layers are designed behind clear interfaces.

## 5. Build Progressively

The system is developed phase-by-phase rather than copying a complete RAG tutorial.

---

# 🔀 Example Git Workflow

Meaningful commits are preferred:

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

# 📈 Project Status

**Status:** Active Development

The project is being developed as a long-term **AI engineering and research portfolio project**.

The final release will include:

* Production API
* User interface
* Evaluation results
* Research experiments
* Containerized deployment
* Documentation
* Portfolio materials

> **Important:** Performance metrics shown in planning examples are not project results. Final metrics will be reported only after running the corresponding experiments.

---

# 🏆 Portfolio Deliverables

The completed project is intended to include:

* Clean GitHub repository
* Production-oriented architecture
* Working RAG application
* REST API
* User interface
* Evaluation dataset
* Retrieval benchmarks
* Generation evaluation
* Error analysis
* Research experiments
* Results visualizations
* Technical report
* Docker deployment
* Project screenshots
* Demonstration of the deployed system

---

# 🚀 Future Work

Potential extensions include:

* OCR for scanned PDFs
* Table extraction
* Multimodal RAG
* Graph RAG
* Improved hybrid retrieval
* Advanced rerankers
* Agentic retrieval
* Multilingual RAG

---

# 👨‍💻 Author

**Amr Ashraf Ali**

Computer Engineering Student
Cairo University

GitHub: `github.com/amrashraf15`

---

# 📄 License

This project is intended as an educational, engineering, and research portfolio project.

Add the project's chosen open-source license here once finalized.

