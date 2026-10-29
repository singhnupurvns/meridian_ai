# Meridian AI

**An AI assistant for finance teams: ask questions about your documents, and review purchases with a team of AI specialists.**

Built with FastAPI, LangChain, Gemini, React and Docker. It runs fully on your laptop, and it can also be deployed to Google Cloud.

[Live slides](https://meridian-ai-course.netlify.app) · [Quick start](#quick-start) · [Architecture](#architecture) · [Configuration](#configuration)

> The company in the examples (Aldermoor Industries) and all sample documents are fictional. This is a demo of how such a system is built, not a real compliance tool.

---

## What it does

**1. Document Q&A (RAG)**
Upload PDFs such as policies, contracts and reports, then ask questions in plain English. Answers come only from your documents, and the app says "I don't know" when the answer isn't there.

**2. Purchase audit (multi-agent)**
Paste a purchase request. Three specialist agents review it (**Risk**, **Tax**, **Accounting control**) and a **CFO** step combines their reports into one memo with a decision: *approved*, *conditional hold* or *rejected*.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind, shadcn/ui |
| Backend | FastAPI, Pydantic, structlog |
| AI | Gemini, LangChain v1 (agents, tools, middleware) |
| Retrieval | Embeddings, Chroma (local) or Vertex AI Vector Search (cloud) |
| Delivery | Docker, Cloud Run, GitHub Actions |

## Architecture

```
Browser (React)
   │
   ▼
FastAPI backend
   ├── Document Q&A:  PDF → chunks → embeddings → vector store → top matches → Gemini answer
   └── Purchase audit: Risk + Tax + Control agents (with tools) → CFO memo
```

Agent middleware adds safety around every step: PII masking, loop limits, retries and tool-call logging.

**One switch, two modes**

| | `APP_MODE=local` (default) | `APP_MODE=cloud` |
|---|---|---|
| Vector DB | Chroma on disk | Vertex AI Vector Search |
| Embeddings | `gemini-embedding-001` | `text-embedding-005` |
| Uploads | Local folder | Cloud Storage |
| Google Cloud needed | No | Yes |

## Quick start

You need Python 3.12, Node.js 20+, and a free [Gemini API key](https://aistudio.google.com/apikey).

```powershell
# 1. Install
uv sync                      # or: python -m venv .venv, then pip install -r requirements-dev.txt

# 2. Configure
copy .env.example .env       # then set GOOGLE_API_KEY=your-key

# 3. Build the frontend and start the app
cd frontend; npm install; npm run build; cd ..
uv run uvicorn api.main:app --app-dir backend --port 8080
```

Open http://localhost:8080. API docs are at http://localhost:8080/docs.

**Try it:** upload the PDFs from `sample_docs/`, then ask *"What payment terms do servo motor suppliers get?"*

**Run tests (no accounts or internet needed):**

```bash
pytest backend/tests
```

### Docker

```bash
docker build -t meridian-ai .
docker run -p 8080:8080 --env-file .env meridian-ai
```

## Project structure

```
backend/
  api/       FastAPI routes and request/response schemas
  rag/       Embeddings, vector store, ingestion, retrieval
  agent/     Tools, prompts and the audit agents
  config/    Settings loaded from .env
  logger/    Structured JSON logging
  tests/     Offline tests with fake models
frontend/    React app
sample_docs/ Fictional PDFs for trying the app
Dockerfile   Container build
```

## Configuration

Copy `.env.example` to `.env`. Never commit `.env`.

| Setting | Purpose |
|---|---|
| `APP_MODE` | `local` or `cloud` |
| `GOOGLE_API_KEY` | Gemini API key |
| `VERTEX_LLM_MODEL_NAME` | Chat model (optional) |
| `LLM_TEMPERATURE` | `0` for the most repeatable answers |
| `GCP_PROJECT_ID`, `GCS_BUCKET_NAME`, `VECTOR_SEARCH_*` | Cloud mode only |

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named 'api'` | Run from the project root and keep `--app-dir backend` |
| `GOOGLE_API_KEY is empty` | Add your key to `.env` and restart |
| `model not found` | Set `VERTEX_LLM_MODEL_NAME` to a current Gemini model |
| Old answers after changing documents | Delete the local data folder and re-upload |

## Acknowledgements

Based on the open Meridian AI learner project, adapted and extended.
