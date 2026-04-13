# Lab 5 Quickstart

**Get your environment verified and your first AI call working in 10 minutes.**

This is an environment check, not a setup guide. If you need to install tools from scratch, stop and see `guides/openrouter-setup-guide.md`.

---

## Step 1: Verify Your OpenRouter Key (2 min)

```bash
# Test your key with a single curl call
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-2.0-flash-001",
    "messages": [{"role": "user", "content": "Reply with: key works"}]
  }'
```

You should see a JSON response containing `key works`. If you get a 401, your key is wrong or expired. Email the instructor before lab starts.

**Python equivalent:**

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_KEY"],
)

response = client.chat.completions.create(
    model="google/gemini-2.0-flash-001",
    messages=[{"role": "user", "content": "Reply with: key works"}],
)
print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

---

## Step 2: Clone and Enter the Right Scaffold (3 min)

```bash
# From your team repo root
cd your-team-repo

# Pick your scaffold and copy it in
# For Python / FastAPI:
cp -r path/to/Lab-5/examples/fastapi-scaffold/. backend/

# For Next.js / TypeScript:
cp -r path/to/Lab-5/examples/nextjs-scaffold/. .
```

Then create your `.env` from the example:

```bash
# FastAPI
cp backend/.env.example backend/.env

# Next.js
cp .env.example .env.local
```

Fill in your real `OPENROUTER_KEY`. Never commit this file.

---

## Step 3: Install Dependencies (3 min)

**FastAPI:**

```bash
cd backend
uv sync          # preferred
# or: pip install -r requirements.txt
```

**Next.js:**

```bash
npm install
```

---

## Step 4: Run the Scaffold and Confirm It Works (2 min)

**FastAPI:**

```bash
uv run uvicorn main:app --reload --port 8000
```

Open `http://localhost:8000/docs` — you should see the Swagger UI with one route: `POST /api/ai/generate`.

Send a test request:

```bash
curl -X POST http://localhost:8000/api/ai/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "system": "Reply briefly."}'
```

**Next.js:**

```bash
npm run dev
```

Open `http://localhost:3000`. Send a test request:

```bash
curl -X POST http://localhost:3000/api/ai \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "system": "Reply briefly."}'
```

---

## You Are Ready

If you saw a real AI response with token counts logged to the terminal, your environment is working. Now go to `templates/design-decisions.md` and start Part 1 of the lab.

If anything failed, check `guides/openrouter-setup-guide.md` or raise your hand immediately — do not spend more than 5 minutes debugging setup alone.
