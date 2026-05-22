# Deploying Your Docker Image to Railway

Once your Dockerfile builds locally, deploying to Railway takes about five minutes.

---

## Before You Start

Confirm these work locally before touching Railway:

```bash
# Build the image
cd backend
docker build -t capstone-app .

# Run it
docker run -p 8000:8000 \
  -e OPENROUTER_API_KEY=your-key-here \
  capstone-app

# Test it
curl http://localhost:8000/health
# Expected: {"status": "ok", ...}
```

If that sequence fails locally, fix it locally first. Railway will fail for the same reasons.

---

## Deploying to Railway

### Option A — Deploy from GitHub (Recommended)

Railway can detect your Dockerfile and deploy automatically on every push to main.

1. Go to [railway.app](https://railway.app) and sign in with GitHub
2. Click **New Project**
3. Select **Deploy from GitHub repo**
4. Choose your capstone repo
5. Railway will detect your `backend/Dockerfile` automatically
6. Click **Deploy**

Railway builds the image and deploys it. The first deploy takes 2–3 minutes.

**Set your environment variables in Railway:**

1. Click on your service in the Railway dashboard
2. Go to the **Variables** tab
3. Add each variable from your `.env.example`:
   - `OPENROUTER_API_KEY` = your actual key
   - `DATABASE_URL` = your Neon PostgreSQL URL
   - Any other variables your app requires
4. Railway restarts the service automatically after you save variables

### Option B — Deploy with Railway CLI

```bash
# Install the Railway CLI
npm install -g @railway/cli

# Log in
railway login

# Link to your project (run from repo root)
railway link

# Deploy
railway up --service backend
```

---

## Confirming the Deploy

Once Railway shows the deployment as active:

1. Click on your service
2. Find the generated URL (looks like `https://capstone-app-production.up.railway.app`)
3. Test the health endpoint:

```bash
curl https://your-app.up.railway.app/health
```

Expected response:
```json
{
  "status": "ok",
  "uptime_seconds": 42,
  "timestamp": "2026-05-22T10:30:00.000000",
  "version": "1.0.0"
}
```

4. Add this URL to your README under "Live Application"

---

## Common Railway Issues

**Build fails with "No Dockerfile found"**
Railway looks for the Dockerfile at the root of the service context. If your Dockerfile is in `backend/`, set the root directory in Railway: Service → Settings → Source → Root Directory → `backend`.

**App starts but returns 502**
Your app is crashing on startup. Check the Railway logs tab for the error. The most common cause is a missing environment variable — your app raises an error when it cannot find `OPENROUTER_API_KEY`.

**Health check failing, container restarting in a loop**
Your `/health` endpoint is calling the LLM or taking longer than the 10-second timeout. The health endpoint must respond in under 100ms with no external calls.

**App works locally but not on Railway**
Check that all packages in your `requirements.txt` are available on PyPI and that your Python version constraint matches Railway's. Railway defaults to Python 3.11 when using the `python:3.11-slim` base image.

---

## Adding the Live URL to Your README

The Repository Review checks for a live URL. Add it to your README:

```markdown
## Live Application

The application is deployed at: https://your-app.up.railway.app

Health check: https://your-app.up.railway.app/health
```

A working live URL at Demo Day is worth bonus points toward the final Capstone score.

---

*Docker on Railway Guide · Lab 10 · CS-AI-2025 · Spring 2026 · KIU*
