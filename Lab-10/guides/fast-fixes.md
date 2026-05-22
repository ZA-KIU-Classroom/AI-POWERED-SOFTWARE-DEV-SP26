# Fast Fixes

One-line solutions to the most common Lab 10 blockers.

---

## Part 1 — Secrets Audit

**"git filter-repo is not installed"**
```bash
pip install git-filter-repo --break-system-packages
```

**"git filter-repo says 'nothing to do'"**
Your file was never committed so there is nothing to remove. Confirm `.env` is in `.gitignore` and move on.

**"After filter-repo, git push fails with 'rejected'"**
```bash
git push --force --all
git push --force --tags
```
Force push is required after rewriting history. This is expected.

**"My teammate's local clone still has the old commits"**
They must delete their local clone and re-clone from GitHub after your force push. There is no other safe option.

---

## Part 2 — GitHub Actions

**"Workflow file not triggering"**
The file must be at `.github/workflows/ci.yml` — exact path, exact spelling. Check with:
```bash
ls .github/workflows/
```
If the directory does not exist, create it:
```bash
mkdir -p .github/workflows
```

**"Error: OPENROUTER_API_KEY not found"**
The secret is not set in GitHub. Go to repo Settings → Secrets and variables → Actions → New repository secret. Add `OPENROUTER_API_KEY` with your actual key value.

**"FileNotFoundError: eval/run_golden_set.py"**
CI runs from the repo root. Your script path in the workflow is wrong. Fix it:
```yaml
# If your eval folder is inside backend/:
run: python backend/eval/run_golden_set.py
# If it is at the repo root:
run: python eval/run_golden_set.py
```

**"ModuleNotFoundError in CI"**
A package is missing from `requirements.txt`. Add it locally, push, and the next CI run picks it up.

**"Golden set score below 0.70 in CI"**
This is a real evaluation failure, not a CI configuration problem. Review which questions failed in the results file and improve your agent's responses before Demo Day.

---

## Part 3 — Docker

**"docker: command not found"**
Docker is not installed. Go to [docs.docker.com/get-docker](https://docs.docker.com/get-docker) and install Docker Desktop. Restart your terminal after installing.

**"permission denied while trying to connect to the Docker daemon socket"**
On Linux, your user is not in the docker group. Run:
```bash
sudo usermod -aG docker $USER
newgrp docker
```

**"docker build fails: COPY requirements.txt not found"**
You are building from the wrong directory. Run `docker build` from the same directory that contains the Dockerfile:
```bash
cd backend
docker build -t capstone-app .
```

**"docker run: port 8000 already allocated"**
Your uvicorn process is already using port 8000. Either stop uvicorn first, or run Docker on a different port:
```bash
docker run -p 8001:8000 capstone-app
# Then test on port 8001:
curl http://localhost:8001/health
```

**"curl http://localhost:8000/health returns 'Connection refused'"**
Your container is binding to `localhost` inside the container, not to the host network. Your Dockerfile CMD must include `--host 0.0.0.0`. Check the starter Dockerfile — this is already set correctly. If you modified the CMD, restore it.

**"Health endpoint returns 500"**
Your app is crashing on startup. Run the container interactively to see the error:
```bash
docker run -it -p 8000:8000 \
  -e OPENROUTER_API_KEY=your-key \
  capstone-app
```
Read the error message in the terminal output.

**"Health endpoint is slow (more than 1 second)"**
Your `/health` endpoint is making an external call — probably calling OpenRouter. The health endpoint must not call any external services. Remove any LLM calls from the `/health` route.

---

## Part 4 — Rate Limiter

**"ImportError: cannot import name 'check_rate_limit'"**
The `rate_limiter.py` file is not in the same directory as your `main.py`, or you have a typo in the import. Check:
```python
# At the top of main.py
from rate_limiter import check_rate_limit
```
And confirm `rate_limiter.py` is in your `backend/` directory.

**"All requests return 429 immediately"**
The bucket initialises with 0 tokens instead of 10. Check the defaultdict lambda in `rate_limiter.py` — the `"tokens"` key must be set to `MAX_TOKENS`, not 0.

**"No requests return 429 even after 20 requests"**
The `check_rate_limit` call is not wired into the endpoint. Confirm you added it at the top of your chat handler, before any other logic:
```python
@app.post("/api/ai/chat")
async def chat(request: Request, body: ChatRequest):
    user_id = request.headers.get("X-User-ID", "anon")
    check_rate_limit(user_id)  # must be here
    # rest of handler
```

**"Rate limiter resets between requests"**
The `BUCKETS` dictionary is defined inside a function instead of at module level. Move it to module scope:
```python
# Module level — outside any function
BUCKETS: dict = defaultdict(lambda: {
    "tokens": 10,
    "last_refill": time.time()
})
```

---

*Fast Fixes · Lab 10 · CS-AI-2025 · Spring 2026 · KIU*
