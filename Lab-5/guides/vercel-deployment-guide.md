# Vercel Deployment Guide

**For Next.js capstone teams — CS-AI-2025 Spring 2026**

Vercel is the fastest path from a working local Next.js prototype to a live URL. For most capstone projects it is the right default. This guide covers setup, environment variables, AI-specific gotchas, and when to consider an alternative.

---

## Is Vercel Right for Your Project?

| You should use Vercel if... | You should consider Railway or Render instead if... |
|---|---|
| Your stack is Next.js (App Router or Pages Router) | Your backend is FastAPI, Flask, or any Python framework |
| Your AI calls are in Next.js API routes or Server Actions | You need long-running processes (>60 seconds per request) |
| You want zero-config deployment from GitHub | You need a persistent background worker or queue |
| You are prototyping and want instant preview URLs | You are running an embedding pipeline or RAG ingestion job |

**Important:** Vercel is not designed for Python backends. If your team chose FastAPI, use Railway (`railway.app`) instead — the workflow is nearly identical but without the timeout and framework constraints.

---

## First Deployment (5 minutes)

### Step 1: Push your project to GitHub

Your team repo should already be on GitHub. Make sure your latest working code is on the `main` branch.

```bash
git add .
git commit -m "feat: initial prototype ready for deployment"
git push origin main
```

### Step 2: Import the project on Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **Add New Project**
3. Find your team repo and click **Import**
4. Vercel auto-detects Next.js — no configuration needed
5. **Do not click Deploy yet** — set environment variables first

### Step 3: Add environment variables

In the **Environment Variables** section before clicking Deploy:

| Name | Value | Notes |
|---|---|---|
| `OPENROUTER_KEY` | Your OpenRouter API key | Required for all AI calls |
| `GEMINI_API_KEY` | Your Google AI Studio key | Required if using Gemini direct |
| `NEXT_PUBLIC_APP_NAME` | Your app name | Optional, for display purposes |

**Do not add `NEXT_PUBLIC_` prefix to your API keys.** That prefix exposes variables to the browser. API keys must stay server-side only.

### Step 4: Deploy

Click **Deploy**. Vercel builds your app and gives you a live URL like `your-app-name.vercel.app` within about 60 seconds.

Every subsequent push to `main` triggers an automatic redeploy.

---

## Environment Variables in Detail

### Local vs Vercel

Your local `.env.local` file is never sent to Vercel. You must add variables manually in the Vercel dashboard or via the CLI.

```bash
# Vercel CLI — add variable to all environments
vercel env add OPENROUTER_KEY

# Or add to production only
vercel env add OPENROUTER_KEY production
```

### Accessing variables in Next.js API routes

```typescript
// app/api/ai/route.ts — server-side only
export async function POST(req: Request) {
  const apiKey = process.env.OPENROUTER_KEY;  // safe — never reaches the browser
  // ...
}
```

```typescript
// NEVER do this in a client component:
const apiKey = process.env.OPENROUTER_KEY;  // undefined in the browser
// NEVER do this:
const apiKey = process.env.NEXT_PUBLIC_OPENROUTER_KEY;  // exposes key to everyone
```

---

## AI-Specific Vercel Gotchas

### Function timeout limits

Vercel Hobby (free) plan: **10-second function timeout**.
Vercel Pro plan: **300-second timeout**.

AI model calls typically take 1–5 seconds for simple completions, but can take longer for complex prompts or large outputs. On the free plan you will hit timeouts if:

- Your prompt is very long
- You are using a slow or overloaded model
- You are doing any heavy processing (embedding a large document, etc.)

**Mitigation for the free plan:**

```typescript
// Set a client-side timeout before Vercel cuts you off
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 8000); // 8s — leave margin

const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
  signal: controller.signal,
  // ...
});
clearTimeout(timeout);
```

For demo day, consider upgrading to Vercel Pro ($20/month) or switching to Railway if your AI calls regularly exceed 10 seconds.

### Streaming responses

Streaming works on Vercel but requires the Edge Runtime for best results:

```typescript
// app/api/ai/stream/route.ts
export const runtime = "edge";  // enables streaming without timeout concerns

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${process.env.OPENROUTER_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model:  "google/gemini-2.5-flash",
      stream: true,
      messages: [{ role: "user", content: prompt }],
    }),
  });

  // Stream the response directly to the client
  return new Response(response.body, {
    headers: { "Content-Type": "text/event-stream" },
  });
}
```

### File system — there is none

Vercel functions are stateless and have no writable filesystem. This means:

- You cannot write `logs/cost-log.csv` on Vercel the same way you do locally
- You cannot persist FAISS indexes to disk between requests
- Any file written in a function is lost when the function finishes

**For Lab 5:** Log cost data to the console (`console.log`) on Vercel — Vercel captures all logs in its dashboard under **Logs**. Export them manually for your audit. For production, use a database (Vercel Postgres, Neon, Supabase) or a logging service.

```typescript
// Cost logging on Vercel — console only
export function logCallVercel(record: CallRecord): void {
  console.log(JSON.stringify({ event: "ai_call", ...record }));
  // Vercel Logs captures this — export from dashboard
}
```

---

## Preview Deployments

Every pull request on your repo automatically gets its own preview URL:

```
https://your-app-name-git-branch-name-your-team.vercel.app
```

This is useful for reviewing features before merging to main. Share preview URLs with your instructor during milestone reviews.

---

## Checking Logs and Errors

1. Go to your project on [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click your project
3. Click **Logs** in the top navigation
4. Filter by **Runtime Logs** to see `console.log` output from your functions
5. Filter by **Error** to find 500 errors and timeout failures

Alternatively via CLI:

```bash
vercel logs your-app-name --follow
```

---

## Custom Domain (Optional)

If you want `your-capstone.com` instead of `your-app.vercel.app`:

1. Buy a domain (Namecheap, Google Domains, Vercel Domains)
2. In Vercel dashboard: **Settings** > **Domains** > **Add Domain**
3. Follow the DNS configuration instructions

Not required for Lab 5 or the capstone demo. A `.vercel.app` URL is fine for everything including Demo Day.

---

## Recommended Stack with Vercel

For teams on the Next.js path, this is the stack that works best together:

| Layer | Tool | Free tier |
|-------|------|-----------|
| Framework | Next.js (App Router) | Always free |
| Hosting | Vercel | 100GB bandwidth, 100k invocations/month |
| Database | Neon (Postgres) | 0.5GB storage, 191 compute hours/month |
| Auth (if needed) | Clerk | 10,000 MAU free |
| AI models | Google AI Studio (Gemini 2.5 Flash) | 10 RPM / 250 RPD |
| AI models fallback | OpenRouter `:free` models | 20 RPM / 200 RPD |
| AI models paid | OpenRouter (org credits) | Pay per token |

---

## When to Switch to Railway

If you hit Vercel's function timeout regularly, need a Python backend, or need a persistent process, switch to Railway:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Railway supports FastAPI, Next.js, and any Dockerfile out of the box. Hobby plan is $5/month with no function timeout limit. For teams with FastAPI backends this is the right choice over Vercel.

---

*Vercel deployment guide for CS-AI-2025 Lab 5, Spring 2026.*
*Verified against Vercel documentation April 2026.*
