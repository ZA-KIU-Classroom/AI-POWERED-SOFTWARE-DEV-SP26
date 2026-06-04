# QUICKSTART · Do This Before You Walk In

Five minutes of preparation makes Lab 12 productive instead of a scramble. Run this checklist the night before or on the bus.

## 1. Your app is deployed and reachable

```bash
# Replace with your real Railway URL. Both must return quickly.
curl -i https://your-app.up.railway.app/health
curl -i -X POST https://your-app.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

If `/health` is slow or `/api/chat` errors, fix it first. A cold start is normal on the first hit, so call it twice and time the second.

## 2. Locust is installed

```bash
pip install locust
locust --version
```

## 3. Your fallback chain and logging from Lab 11 are in place

```bash
# Your .env should define all three model strings.
grep -E "PRIMARY_MODEL|SECONDARY_MODEL|OSS_FALLBACK" .env

# Every /api/chat response should include which model answered.
curl -s -X POST https://your-app.up.railway.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "hi"}' | python -m json.tool | grep model_used
```

## 4. Your evaluation assets exist

```bash
ls eval/golden_set.json eval/model-comparison.json
```

You need at least 5 questions in `eval/golden_set.json`.

## 5. Your presentation draft exists

Bring a draft of the 8-slide Demo Day deck, even if rough. See `guides/presentation-checklist.md` for the required structure. You will work on it during the session.

## 6. Bring these to the room

- Laptop with the app open in a tab, warmed up
- A backup screen recording of your demo if you have one
- Your draft deck, exported to PDF as a fallback
- One teammate ready to drive the demo while another narrates

## If something is missing

Do not panic. The first few minutes of the lab are for warm-up and fixes. Flag the instructor early so it can be sorted before you start the main work.
