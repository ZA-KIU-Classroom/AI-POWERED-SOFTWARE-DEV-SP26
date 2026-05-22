# .env.example Template

Copy the block below into a file called `.env.example` at the root of your capstone repo. Replace the placeholder comments with descriptions of what each variable does. Never put real values in this file.

This file is committed to git. It tells collaborators and the Repository Review grader what environment variables your application requires.

---

```bash
# .env.example
# Copy this file to .env and fill in your real values.
# The .env file is gitignored and must never be committed.

# ── AI Model API ──────────────────────────────────────────────────────────────
# Your OpenRouter API key. Get one at openrouter.ai
# All LLM calls in this application route through OpenRouter.
OPENROUTER_API_KEY=your-openrouter-key-here

# ── Database ──────────────────────────────────────────────────────────────────
# PostgreSQL connection string (Neon, Railway, or local)
# Format: postgresql://user:password@host:port/database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# ── Application ───────────────────────────────────────────────────────────────
# Environment identifier. Use "development" locally, "production" on Railway.
ENVIRONMENT=development

# Version string shown in the /health endpoint response.
APP_VERSION=1.0.0

# ── Redis (if using session state) ───────────────────────────────────────────
# Redis connection string for conversation memory.
# Remove this section if your app does not use Redis.
REDIS_URL=redis://localhost:6379

# ── Security ─────────────────────────────────────────────────────────────────
# Secret key for JWT token signing. Generate with: openssl rand -hex 32
JWT_SECRET=your-jwt-secret-here

# ── Optional ──────────────────────────────────────────────────────────────────
# MCP server authentication token.
MCP_AUTH_TOKEN=your-mcp-token-here
```

---

## What to Check Before Committing

- Every variable your app reads from `os.environ` or `os.getenv` appears here
- All values are placeholders — no real keys, passwords, or tokens
- The file is named exactly `.env.example` (with the dot)
- Your `.env` file (with real values) is listed in `.gitignore`

---

*env-example Template · Lab 10 · CS-AI-2025 · Spring 2026 · KIU*
