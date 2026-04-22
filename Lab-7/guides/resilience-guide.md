# Resilience Guide

Lab 7 requires every external AI call to handle slow responses and transient failure.

A production system fails in boring ways first:
- slow network
- provider hiccup
- empty model response
- rate limit
- timeout
- partial outage

Your code must absorb these failures without hiding them.

---

## 1. Timeouts

A timeout defines how long you are willing to wait for a call before treating it as failed.

### Why it matters

Without a timeout:
- requests hang
- the UI stalls
- retries never begin
- the user has no clear failure boundary

### Rule for Lab 7

Every LLM call must go through a timeout wrapper.

### Python pattern

```python
import asyncio

async def call_with_timeout(coro, timeout_s: float):
    return await asyncio.wait_for(coro, timeout=timeout_s)
```

### TypeScript pattern

```ts
export async function withTimeout<T>(promise: Promise<T>, timeoutMs: number): Promise<T> {
  return await Promise.race([
    promise,
    new Promise<T>((_, reject) =>
      setTimeout(() => reject(new Error("timeout")), timeoutMs)
    ),
  ]);
}
```

---

## 2. Retries with Exponential Backoff

Not every failure should retry.

Good retry candidates:
- temporary provider errors
- 429 rate limits
- transient 5xx responses
- network interruptions

Bad retry candidates:
- invalid schema
- bad auth key
- prompt too long
- forbidden action

### Rule for Lab 7

Use:
- bounded attempts
- exponential backoff
- small random jitter
- logging for each attempt

### Python pattern

```python
import asyncio
import random

async def retry_with_backoff(fn, max_attempts: int = 4, base_delay_s: float = 0.5):
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await fn(attempt)
        except Exception as exc:
            last_error = exc

            if attempt == max_attempts:
                raise

            delay = base_delay_s * (2 ** (attempt - 1))
            jitter = random.uniform(0, 0.1)
            await asyncio.sleep(delay + jitter)

    raise last_error
```

### TypeScript pattern

```ts
export async function retryWithBackoff<T>(
  fn: (attempt: number) => Promise<T>,
  maxAttempts = 4,
  baseDelayMs = 500,
): Promise<T> {
  let lastError: unknown;

  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      return await fn(attempt);
    } catch (error) {
      lastError = error;

      if (attempt === maxAttempts) {
        throw error;
      }

      const delay = baseDelayMs * Math.pow(2, attempt - 1);
      const jitter = Math.floor(Math.random() * 100);
      await new Promise(resolve => setTimeout(resolve, delay + jitter));
    }
  }

  throw lastError;
}
```

---

## 3. Circuit Breakers

A circuit breaker prevents endless calls to a failing dependency.

### Three states

- **Closed**: normal operation
- **Open**: fail fast, do not keep calling the dependency
- **Half-open**: allow one probe request after a cooldown

### When to use it

You do not need a full implementation in Lab 7.  
You do need to understand when you would add one:

- same provider fails repeatedly
- retries are draining credits
- system should degrade gracefully instead of cascading

---

## 4. What to Log

Your episode log must include enough detail for later analysis.

Minimum Lab 7 fields:

- `event_type`
- `model`
- `success`
- `retry_count`
- `timeout_ms`
- `latency_ms`
- `error_type`
- `session_id`
- `approval_required`
- `approved`

Use `templates/episode-log-extension.md`.

---

## 5. Graceful Degradation

When the best path fails, the system should still do something reasonable.

Examples:
- return a partial answer
- skip an optional specialist
- ask the user to retry
- fall back to a simpler route
- stop before the risky action and request human confirmation

A clean downgrade is better than a cascade.

---

## 6. Lab 7 Minimum Standard

Before you tag your repo, confirm:

- [ ] every LLM call uses a timeout wrapper
- [ ] retries are bounded
- [ ] attempts are logged
- [ ] final failure is surfaced cleanly
- [ ] risky actions do not proceed silently after degraded behaviour

---

*Guide for Lab 7 resilience work.*
