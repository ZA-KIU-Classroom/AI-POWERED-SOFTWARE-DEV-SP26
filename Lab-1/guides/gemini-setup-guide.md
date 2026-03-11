# Gemini Free Tier Setup Guide

**Understanding Google AI Studio, your API key, and the free tier limits.**

---

## What Is Google AI Studio?

Google AI Studio is Google's browser-based IDE for prototyping with Gemini models. It includes a chat playground, a prompt testing interface, and API key management — all for free. In this course, you use Google AI Studio primarily as the source of your API key. The actual work happens in your Python code.

URL: [aistudio.google.com](https://aistudio.google.com)

---

## Creating Your Account

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **"Sign in"** in the top right
3. Use your Google account (any Gmail address works — a university email is fine but not required)
4. On first login, you will be asked to accept Google's generative AI terms of service. Read them (at least the key points) and accept
5. You are now in the Google AI Studio dashboard

The dashboard shows you a prompt playground on the left and your model options on the right. Feel free to test the chat interface here — it is a useful way to prototype prompts before moving them into your code.

---

## Getting Your API Key

1. In the left sidebar, find and click **"Get API key"** (it may also appear as "API keys" depending on the current UI)
2. Click the **"Create API key"** button
3. You will be prompted to associate the key with a Google Cloud project. Select **"Create API key in new project"** — Google will create a project for you automatically
4. Your key is generated. It begins with `AIza` and is 39–42 characters long
5. Click the copy icon next to the key to copy it to your clipboard
6. Paste it into your `.env` file immediately:
   ```
   GEMINI_API_KEY=AIzaSyYourKeyHere
   ```

**Can you view the key again later?** Yes. Return to Google AI Studio → Get API key, and your existing keys are listed. You can also regenerate a new key if yours is compromised.

---

## The Models Available on Free Tier

As of March 2026, the following models are accessible on the free tier via Google AI Studio:

| Model | Best For | Context Window | Speed |
|-------|----------|----------------|-------|
| `gemini-3-flash-preview` | General tasks, fast responses, high volume | 1M tokens | Very fast |
| `gemini-3.1-flash-lite-preview` | Complex reasoning, step-by-step problems | 1M tokens | Slower (reasoning) |
| `gemini-3-flash-preview-8b` | Ultra-fast, lightweight tasks | 1M tokens | Fastest |

**For Lab 1, use `gemini-3-flash-preview`.** It is fast, capable, and sits comfortably within the free tier limits even with the volume of calls you will make during the lab session.

The `gemini-3.1-flash-lite-preview` model is worth experimenting with for Exercise 2 — it is Google's reasoning model that shows extended chain-of-thought thinking before answering. It is analogous to OpenAI's o1 family. It uses more tokens and is slower, but the reasoning traces are educational.

**Note on the frontier:** The course's frontier models (Gemini 3.1, GPT-5.2, Claude Opus 4.6) require paid API access. You will access them through OpenRouter organizational credits starting in Lab 2. The free tier gives you capable models that are excellent for learning the fundamentals.

---

## Free Tier Limits in Detail

Understanding these limits prevents frustration during the lab session.

### Rate Limits

| Metric | Limit |
|--------|-------|
| Requests per minute (RPM) | 15 |
| Requests per day | 1,500 |
| Tokens per minute (TPM) | 1,000,000 |

The limit that matters most for lab work is **15 requests per minute**. If you write a loop that sends 20 requests quickly, the 16th will fail with a `429 Resource Exhausted` error. The fix is simple: add `time.sleep(4)` between calls in any loop you write.

### What "free" means

Free tier usage does not require a credit card. Google makes the Gemini API free for development and low-volume use in exchange for the right to use that data to improve their models. If you are processing personal data or sensitive information (you should not be for coursework), read Google's data usage policy.

When you move to paid tier (which the course does through OpenRouter for higher-volume work), your data is not used for training by default.

---

## Staying Within Free Tier Limits During Lab

### Strategy 1: Add sleep between looped calls

```python
import time

prompts = ["prompt one", "prompt two", "prompt three", "prompt four"]
for prompt in prompts:
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt
    )
    print(response.text)
    time.sleep(4)  # 4 seconds ensures we stay under 15 RPM
```

### Strategy 2: Check your usage in Google AI Studio

Google AI Studio shows your request count in the API key management section. Check it periodically during the lab if you are running many experiments.

### Strategy 3: Use the prompt playground for testing

Before running a prompt in your Python code (which costs a request), test it in the Google AI Studio playground. Playground usage does not count against your API key's rate limits — it uses Google's UI quota instead.

---

## Troubleshooting API Errors

| Error | Meaning | Fix |
|-------|---------|-----|
| `401 Unauthorized` | API key is invalid or missing | Check your `.env` file and that `load_dotenv()` is called |
| `403 Forbidden` | API key is revoked or restricted | Generate a new key in Google AI Studio |
| `429 Resource Exhausted` | Rate limit hit | Wait 60 seconds and retry, or add `time.sleep()` to your code |
| `400 Bad Request` | Your request is malformed | Check the request structure against the starter code |
| `500 Internal Server Error` | Temporary Google-side issue | Wait 30 seconds and retry — these are rare and transient |

---

## Rotating or Revoking a Key

If you accidentally commit your API key to Git:

1. Go to Google AI Studio → API keys
2. Click the three dots next to the compromised key
3. Select **"Delete key"** — this immediately revokes it
4. Create a new key
5. Update your `.env` file
6. Never commit the `.env` file

On GitHub, you can also push a fix that removes the key from code — but even after removal, the key is visible in the Git history. Revocation is the only reliable protection.

---

## Moving Beyond Free Tier (Lab 2 Onwards)

Starting in Lab 2, you will use **OpenRouter** — a service that routes to 400+ models including Gemini 3.1, Claude Opus 4.6, and GPT-5.2. The organizational account has been provisioned for the course, and each team will receive a credit allocation.

The switch from `google-genai` to OpenRouter requires changing two lines of code. You will learn this in Lab 2. For now, master the free tier.

---

*Gemini Setup Guide for CS-AI-2025 Lab 1, Spring 2026.*
