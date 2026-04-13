# Next.js AI Scaffold

**CS-AI-2025 Lab 5, Spring 2026 — TypeScript / Next.js starter**

---

## Quickstart

```bash
# 1. Copy this folder into your team repo root
cp -r path/to/Lab-5/examples/nextjs-scaffold/. .

# 2. Create your .env.local
cp .env.example .env.local
# Edit .env.local — add your OPENROUTER_KEY

# 3. Install dependencies
npm install

# 4. Run
npm run dev

# 5. Verify
curl -X POST http://localhost:3000/api/ai \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is RAG in one sentence?"}'
```

---

## Model Strategy

**Start on the free tier. Only spend org credits when free quality is not enough.**

Default model: `google/gemini-2.5-flash` via OpenRouter.

On the free tier (`:free` suffix or AI Studio direct), you pay nothing. Change `DEFAULT_MODEL` in `.env.local` to switch:

```bash
# Zero cost — auto-selects best available free model
DEFAULT_MODEL=openrouter/free

# Zero cost — specific reliable free models (April 2026)
DEFAULT_MODEL=meta-llama/llama-4-maverick:free
DEFAULT_MODEL=google/gemma-3-27b-it:free

# Zero cost — Google AI Studio direct (set GEMINI_API_KEY and adjust llm-service.ts)
# gemini-2.5-flash-lite  → 15 RPM / 1,000 RPD  (fastest)
# gemini-2.5-flash       → 10 RPM / 250 RPD
# gemini-2.5-pro         → 5 RPM  / 100 RPD
```

**Deprecated — do not use:** `google/gemini-2.0-flash`, `google/gemini-2.0-flash-lite` — both shut down June 1, 2026.

See `types/ai-types.ts` for the full model registry with pricing.

---

## File Structure

```
.
├── app/
│   └── api/
│       └── ai/
│           └── route.ts          ← POST /api/ai — entry point for AI calls
├── lib/
│   ├── llm-service.ts            ← OpenRouter wrapper + call logic
│   └── cost-logger.ts            ← Logs every call to CSV + console
├── types/
│   └── ai-types.ts               ← Shared request/response types + model registry
├── logs/                         ← Created automatically on first call (local only)
│   └── cost-log.csv
├── .env.example
└── package.json
```

---

## Deploying to Vercel

Vercel is the recommended deployment platform for Next.js teams.

```bash
# One-time setup
npm install -g vercel
vercel login

# Deploy
vercel

# Or connect your GitHub repo in the Vercel dashboard for automatic deploys
```

**Before deploying:** add your environment variables in the Vercel dashboard under **Settings > Environment Variables**. Never commit `.env.local`.

```bash
# Via CLI
vercel env add OPENROUTER_KEY
vercel env add DEFAULT_MODEL
```

**Cost log on Vercel:** The CSV file cannot be written on Vercel's read-only filesystem. The cost logger automatically falls back to `console.log` in production. Export logs from the Vercel Logs dashboard for your Week 11 audit.

See `guides/vercel-deployment-guide.md` for the full deployment guide including function timeouts, streaming, and environment variable management.

---

## Vercel Free Tier Limits to Know

- Function timeout: **10 seconds** on Hobby (free) plan
- Bandwidth: 100 GB/month
- Function invocations: 100,000/month
- Unlimited deployments and preview URLs

For capstone prototyping, the free tier is enough. If your AI calls regularly take longer than 8 seconds, consider Vercel Pro ($20/month) or Railway for longer timeouts.

---

## Next Steps

1. Rename `/api/ai` to something capstone-specific (e.g. `/api/summarise`, `/api/recommend`, `/api/analyse`)
2. Add a typed request body with your domain objects, not just a generic `prompt` string
3. Wire in your RAG service if your capstone uses knowledge retrieval
4. Add a simple UI component that calls the endpoint from the browser
5. Write at least one Jest test for the route before you close the laptop

---

*Next.js scaffold for CS-AI-2025 Lab 5, Spring 2026.*
