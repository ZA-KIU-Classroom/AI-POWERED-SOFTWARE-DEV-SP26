# Example Prompt Log (Completed Reference)

**This is a completed example to show you the expected quality and depth of your own prompt log.**  
*Do not copy this. It is here so you know what a good log looks like.*

---

**Student Name:** [Anonymised — previous semester example]  
**Student ID:** [Anonymised]  
**Lab / Assignment:** HW1 — Individual  
**Date:** Lab 1 session, Spring 2026  
**Model Used:** `gemini-3-flash-preview`

---

## Session Overview

| Field | Value |
|-------|-------|
| Session purpose | Explore prompt patterns for a topic I plan to use in my capstone — medical symptom triage |
| Task / domain | Healthcare information, symptom assessment |
| Total calls made | 6 |
| Total input tokens | 847 |
| Total output tokens | 1,214 |
| Total estimated cost | $0.00 (free tier) |
| Total time (minutes) | 38 |

---

## Call Log

### Call #1

| Field | Value |
|-------|-------|
| Timestamp | `2026-03-06 09:22:15` |
| Pattern used | `[x] Zero-shot` |
| Model | `gemini-3-flash-preview` |

**System Prompt** *(leave blank if not used)*

```
[none]
```

**User Prompt**

```
What should a person do if they have a sore throat and mild fever?
```

**Model Response**

```
If you have a sore throat and mild fever, here are some recommended steps:

1. Rest and stay hydrated — drink plenty of fluids like water, herbal tea,
   or warm broth. Avoid caffeine and alcohol.

2. Over-the-counter relief — acetaminophen (paracetamol) or ibuprofen can
   reduce fever and ease throat pain. Follow package instructions.

3. Soothe the throat — gargle with warm salt water (1/4 tsp salt per 8 oz
   water), try throat lozenges, or use a humidifier.

4. Monitor symptoms — most sore throats caused by viruses resolve within
   7–10 days. See a doctor if:
   - Fever rises above 38.9°C (102°F)
   - Symptoms worsen after 3–4 days
   - You have difficulty breathing or swallowing
   - A white or yellow coating appears on your tonsils

5. Rest your voice — avoid straining your throat unnecessarily.

Note: If you suspect strep throat (which requires antibiotics), a rapid
strep test from your doctor or pharmacy is a reliable diagnostic tool.
```

**Metrics**

| Metric | Value |
|--------|-------|
| Input tokens | 21 |
| Output tokens | 211 |
| Total tokens | 232 |
| Latency (ms) | 1,340 |
| Estimated cost (USD) | $0.00 (free tier) |

**Evaluation**

| Question | Your Answer |
|----------|------------|
| Did the output match what you intended? | `[x] Partially` |
| Quality score (1–5) | 3 |
| What worked well? | The response is accurate and covers the key points. Good numbered structure. |
| What would you change? | It is way too long for a triage app — I need concise, structured output. The user of my app does not want a wall of text, they want a quick assessment. Need to constrain format. |

---

### Call #2

| Field | Value |
|-------|-------|
| Timestamp | `2026-03-06 09:27:41` |
| Pattern used | `[x] System prompt` |
| Model | `gemini-3-flash-preview` |

**System Prompt**

```
You are a medical triage assistant helping patients determine urgency level.

For every symptom description:
1. Output a TRIAGE LEVEL: ROUTINE, URGENT, or EMERGENCY
2. Output a ONE-LINE REASON for that level
3. Output exactly THREE next steps in bullet points
4. End with a DISCLAIMER in italics

Keep your entire response under 100 words. Never diagnose. Never prescribe.
If in doubt, escalate the triage level.
```

**User Prompt**

```
What should a person do if they have a sore throat and mild fever?
```

**Model Response**

```
TRIAGE LEVEL: ROUTINE

REASON: Sore throat with mild fever is most likely viral and self-limiting.

Next steps:
• Rest, hydrate, and take OTC pain relievers as directed
• Gargle warm salt water 2–3 times daily for symptom relief
• Monitor for warning signs (fever above 39°C, difficulty swallowing, worsening after day 4)

*This is general information only. Consult a healthcare professional for personal medical advice.*
```

**Metrics**

| Metric | Value |
|--------|-------|
| Input tokens | 143 |
| Output tokens | 88 |
| Total tokens | 231 |
| Latency (ms) | 980 |
| Estimated cost (USD) | $0.00 (free tier) |

**Evaluation**

| Question | Your Answer |
|----------|------------|
| Did the output match what you intended? | `[x] Yes` |
| Quality score (1–5) | 5 |
| What worked well? | The system prompt completely transformed the output. Exact format I specified, concise, structured, includes triage level, shorter than Call #1 despite more input tokens, actually faster. |
| What would you change? | The triage level would work better as a colour code (GREEN/AMBER/RED) for a visual UI. Will test this in Call #3. |

---

### Call #3

| Field | Value |
|-------|-------|
| Timestamp | `2026-03-06 09:33:02` |
| Pattern used | `[x] System prompt` (iterated) |
| Model | `gemini-3-flash-preview` |

**System Prompt**

```
You are a medical triage assistant. Output ONLY valid JSON with this exact schema:
{
  "triage": "GREEN" | "AMBER" | "RED",
  "summary": string (max 15 words),
  "steps": [string, string, string],
  "disclaimer": string (max 15 words),
  "seek_care_within": "hours" | "days" | "weeks" | "if_worsens"
}
Never include any text outside the JSON object.
```

**User Prompt**

```
Sore throat and mild fever for 2 days.
```

**Model Response**

```json
{
  "triage": "GREEN",
  "summary": "Likely viral infection, self-limiting, monitor for warning signs.",
  "steps": [
    "Rest and drink fluids; take paracetamol for pain and fever",
    "Gargle warm salt water twice daily to soothe throat",
    "Watch for fever above 39°C or difficulty swallowing"
  ],
  "disclaimer": "Not medical advice; consult a doctor for personal guidance.",
  "seek_care_within": "if_worsens"
}
```

**Metrics**

| Metric | Value |
|--------|-------|
| Input tokens | 131 |
| Output tokens | 101 |
| Total tokens | 232 |
| Latency (ms) | 1,105 |
| Estimated cost (USD) | $0.00 (free tier) |

**Evaluation**

| Question | Your Answer |
|----------|------------|
| Did the output match what you intended? | `[x] Yes` |
| Quality score (1–5) | 5 |
| What worked well? | The JSON output is exactly parseable. I can feed this directly into a front end. The "seek_care_within" field was my own addition and it added real value to the triage decision. |
| What would you change? | I need to test whether it actually outputs valid JSON every time — a single malformed response in production could crash the app. Need error handling and validation in the code. |

---

## Session Summary

**Pattern Comparison**

| Pattern | Calls Used | Average Quality (1–5) | Notes |
|---------|-----------|----------------------|-------|
| Zero-shot | 1 | 3 | Accurate but wrong format, too long |
| Few-shot | 0 | — | Did not test yet, will do in HW1 |
| Chain-of-thought | 0 | — | Planned for complex triage edge cases |
| System prompt | 2 | 5 | Completely transformed output quality |

**Best call of the session:** Call #3

**Why it was best:**
```
Call #3 combined the format constraint from Call #2 with a JSON output requirement,
making the response directly parseable by code. It also added the "seek_care_within"
field which I came up with while iterating — that field would be very useful in a
real triage app. The response was shorter and faster than Call #2 despite carrying
the same information.
```

**Most interesting failure of the session:** Call #1 (zero-shot)

**Why it failed and what you learned:**
```
The zero-shot call was not wrong — it was accurate medical information — but it was
completely wrong for my use case. It produced the kind of output a general AI assistant
would produce, not the kind of output a purpose-built triage tool needs. This is the
core insight of today's lab: the same model with different prompts is effectively a
different product. The system prompt in Call #2 transformed the same model into
something I could actually ship.
```

**If you repeated this session, what would you do differently?**
```
I would test the JSON output format with 10 different symptom inputs to check how
consistent the model is. In a real application, one malformed JSON response crashes
the user's experience. I would also test what happens when I give it a deliberately
ambiguous or edge-case symptom to see whether it escalates conservatively (as I told it to).
```

---

*Example prompt log for CS-AI-2025 Lab 1, Spring 2026.*  
*This example is anonymised from a previous semester. Used with permission.*
