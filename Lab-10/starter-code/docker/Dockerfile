# Dockerfile
# Place this file in your backend/ directory.
# Build: docker build -t capstone-app .
# Run:   docker run -p 8000:8000 --env-file ../.env capstone-app

# ── Base image ────────────────────────────────────────────────────────────────
# python:3.11-slim is 70% smaller than the full image.
# Pin the minor version so your image does not silently change between builds.
FROM python:3.11-slim

# ── System dependencies ───────────────────────────────────────────────────────
# curl is required for the HEALTHCHECK command below.
# Clean up the apt cache in the same layer to keep the image small.
RUN apt-get update && apt-get install -y \
    curl \
  && rm -rf /var/lib/apt/lists/*

# ── Working directory ─────────────────────────────────────────────────────────
WORKDIR /app

# ── Dependencies ──────────────────────────────────────────────────────────────
# Copy requirements.txt before the application code.
# Docker caches each layer. If your code changes but requirements.txt does not,
# Docker reuses the cached pip install layer — much faster rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application code ──────────────────────────────────────────────────────────
COPY . .

# ── Port ─────────────────────────────────────────────────────────────────────
EXPOSE 8000

# ── Health check ─────────────────────────────────────────────────────────────
# Railway and docker-compose use this to know when your app is ready.
# Interval: check every 30 seconds.
# Timeout: fail the check if it takes more than 10 seconds.
# Retries: restart the container after 3 consecutive failures.
# The /health endpoint must respond in under 10 seconds with a 2xx status.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# ── Security: non-root user ───────────────────────────────────────────────────
# Never run your application as root inside a container.
# If a prompt injection exploits your app, a non-root process has far less
# ability to affect the host system.
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# ── Start command ─────────────────────────────────────────────────────────────
# --host 0.0.0.0 makes the app reachable from outside the container.
# Without this, uvicorn binds to localhost inside the container only.
# --workers 1 is correct for a single-container deployment with async FastAPI.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
