# Lab 6 Quickstart

**Verify your environment for streaming and MCP in 10 minutes.**

This is a pre-flight check, not a setup guide. Lab 5 should already be working. If your Lab 5 endpoint is broken, fix that before Friday — do not use Lab 6 time for Lab 5 debugging.

---

## Step 1: Confirm Your Lab 5 Endpoint Still Works (2 min)

```bash
# FastAPI
cd your-team-repo/backend
uv run uvicorn main:app --reload --port 8000

curl -X POST http://localhost:8000/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Reply with: lab5 still works"}'
```

```bash
# Next.js
cd your-team-repo
npm run dev

curl -X POST http://localhost:3000/api/ai \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Reply with: lab5 still works"}'
```

You should see a JSON response with a real AI-generated string and token counts. If not, stop here and fix Lab 5 before today's lab begins.

---

## Step 2: Confirm Your OpenRouter Key Is Active (1 min)

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Say: key active"}]
  }'
```

If you get a `401`, email the instructor before Friday morning — do not wait until lab starts.

---

## Step 3: Verify Streaming Works at the API Level (2 min)

Before adding streaming to your app, confirm the API itself streams:

```bash
# The --no-buffer flag is required to see tokens arrive in real time
curl -N https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Count slowly from 1 to 10, one number per second."}],
    "stream": true
  }'
```

You should see a stream of `data: {...}` chunks arriving one at a time. If you see them all at once, your terminal is buffering — that is fine, the API is still streaming. Your app code handles this correctly.

---

## Step 4: Install the MCP SDK (3 min)

Pick the SDK that matches your stack. You only need one.

**TypeScript (recommended for Next.js teams):**

```bash
# In your team repo root or a new mcp-server/ directory
npm install @modelcontextprotocol/sdk zod
```

Verify installation:

```bash
node -e "require('@modelcontextprotocol/sdk'); console.log('MCP SDK ready')"
```

**Python (recommended for FastAPI teams):**

```bash
# In your backend directory or a new mcp-server/ directory
uv add mcp
# or: pip install mcp --break-system-packages
```

Verify installation:

```bash
python -c "import mcp; print('MCP SDK ready')"
```

---

## Step 5: Verify the MCP Inspector Can Run (1 min)

The MCP Inspector lets you test your server without configuring Cursor. Run it once now to confirm it works.

```bash
npx @modelcontextprotocol/inspector --version
```

If it prints a version number, you are ready. If it fails, check that Node 18+ is installed:

```bash
node --version   # must be v18.0.0 or higher
```

---

## You Are Ready

If all five steps passed, your environment is ready for Lab 6. You will:

1. Add a streaming endpoint to your existing capstone app (Part 1)
2. Add session memory to that endpoint (Part 2)
3. Build and test a minimal MCP server with one of your capstone tools (Part 3)

If anything failed, check `guides/streaming-guide.md` or `guides/mcp-setup-guide.md`, or raise your hand when lab starts. Do not spend more than 5 minutes debugging setup alone.
