# FastAPI AI Scaffold

**CS-AI-2025 Lab 5, Spring 2026 — Python / FastAPI starter**

---

## Quickstart

```bash
# 1. Copy this folder into your team repo
cp -r path/to/Lab-5/examples/fastapi-scaffold/. backend/
cd backend

# 2. Create your .env
cp .env.example .env
# Edit .env — add your OPENROUTER_KEY

# 3. Install dependencies (uv preferred)
uv sync
# or: pip install -e .

# 4. Run
uv run uvicorn main:app --reload --port 8000

# 5. Verify
curl http://localhost:8000/health
# → {"status":"ok"}

# 6. Test the AI endpoint
curl -X POST http://localhost:8000/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is RAG in one sentence?"}'
```

Open `http://localhost:8000/docs` for the interactive Swagger UI.

---

## Model Strategy

**Start on the free tier. Only spend org credits when free quality is not enough.**

Default model: `google/gemini-2.5-flash` via OpenRouter (uses org credits at $0.15/$0.60 per 1M tokens).

To use the fully free tier, set `DEFAULT_MODEL` in `.env`:

```bash
# Zero cost — OpenRouter free tier (20 RPM / 200 RPD)
DEFAULT_MODEL=openrouter/free

# Zero cost — specific free model
DEFAULT_MODEL=meta-llama/llama-4-maverick:free

# Zero cost — Google AI Studio direct (also set USE_DIRECT_GEMINI=true)
DEFAULT_MODEL=gemini-2.5-flash-lite   # 15 RPM / 1,000 RPD — fastest
DEFAULT_MODEL=gemini-2.5-flash        # 10 RPM / 250 RPD
```

**Deprecated — do not use:** `gemini-2.0-flash`, `gemini-2.0-flash-lite` (shutdown June 1, 2026).

---

## File Structure

```
backend/
├── main.py                    ← FastAPI app entry point
├── routers/
│   └── ai_router.py           ← POST /api/ai/generate
├── services/
│   └── llm_service.py         ← OpenRouter / AI Studio wrapper + cost logger
├── models/
│   └── request_models.py      ← Pydantic request/response schemas
├── logs/                      ← Created automatically on first API call
│   └── cost-log.csv
├── .env.example
└── pyproject.toml
```

---

## Deploying to Railway (recommended for FastAPI)

Vercel does not support Python backends. Use Railway instead:

```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

Railway auto-detects FastAPI. Add your environment variables in the Railway dashboard under **Variables**.

---

## Next Steps

1. Replace `POST /api/ai/generate` with your capstone-specific endpoint name and logic
2. Add your Pydantic models for your domain (not just generic prompt/content)
3. Wire in your RAG pipeline from Lab 4 if your capstone uses knowledge retrieval
4. Add at least one test in `tests/test_ai_router.py` before you close the laptop

---

*FastAPI scaffold for CS-AI-2025 Lab 5, Spring 2026.*
