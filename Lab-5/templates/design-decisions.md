# Design Decisions — Lab 5

**Team Name:**
**Team Members:**
**Date:** Friday 10 April 2026
**Time to complete:** 25 minutes

> This document is a team effort. Fill it in together. It goes into your repo at `docs/design-decisions-lab5.md`. The instructor reviews it as part of your capstone progress record.

---

## Section 1: Design Review Feedback Acknowledgement

For each piece of feedback you received on your Design Review, record it below and state your decision. Be honest. "We disagree and here is why" is a valid answer. "We forgot" is not.

Copy the feedback item exactly as written, then write your decision.

### Feedback Item 1

**Feedback received:**

```
[paste or summarise the feedback here]
```

**Our decision:**

- [ ] We are making this change: _______________
- [ ] We are not making this change because: _______________
- [ ] We need more information to decide — we will address it by: _______________

**Impact on our design:**

```
[one or two sentences on how this changes or does not change what we are building]
```

---

### Feedback Item 2

**Feedback received:**

```
[paste or summarise the feedback here]
```

**Our decision:**

- [ ] We are making this change: _______________
- [ ] We are not making this change because: _______________
- [ ] We need more information to decide — we will address it by: _______________

**Impact on our design:**

```
[one or two sentences]
```

---

### Feedback Item 3

**Feedback received:**

```
[paste or summarise the feedback here]
```

**Our decision:**

- [ ] We are making this change: _______________
- [ ] We are not making this change because: _______________
- [ ] We need more information to decide — we will address it by: _______________

**Impact on our design:**

```
[one or two sentences]
```

---

*(Add more sections if you received more than three feedback items. Do not leave any feedback unaddressed.)*

---

## Section 2: What We Are Keeping

List the three to five core decisions from your original Design Review that you are not changing. For each, state why you are confident in it.

| Decision | Reason we are keeping it |
|---|---|
| | |
| | |
| | |
| | |
| | |

---

## Section 3: Today's Prototype Milestone

This is the most important part of this document. Be specific. Vague goals produce no working code.

**The one feature we are building today:**

```
[Example: "A FastAPI POST route at /api/summarise that accepts a URL, 
fetches the page content, and returns a 3-sentence AI-generated summary 
with the model name and token count logged to the terminal."]

[Write your actual milestone here]
```

**How we will know it is working:**

```
[Describe the exact thing you will do to verify success.
Example: "We will send a curl request with a real BBC article URL 
and see a 3-sentence summary in the response body 
and token counts printed in the terminal."]
```

**What we are explicitly NOT building today:**

```
[Write down the features you are deferring. 
This keeps scope from expanding during the sprint.
Example: "We are not building the frontend UI, user authentication, 
or the database layer today."]
```

---

## Section 4: Technical Decisions for Today

Answer each question briefly. These decisions should be made before you write the first line of code.

**Which model are you using for the sprint?**

```
[Start with google/gemini-2.0-flash-001 unless you have a specific reason not to.
It is fast, cheap, and reliable via OpenRouter.]
```

**Which stack scaffold are you using?**

- [ ] FastAPI (Python) — using `examples/fastapi-scaffold/`
- [ ] Next.js (TypeScript) — using `examples/nextjs-scaffold/`
- [ ] Custom stack — see `guides/custom-stack-guide.md`

**What is the input your endpoint will accept?**

```
[Example: "A JSON body with a 'text' field containing the content to summarise."]
```

**What is the output your endpoint will return?**

```
[Example: "A JSON object with 'summary' (string), 'model' (string), 
'input_tokens' (int), 'output_tokens' (int), 'latency_ms' (int)."]
```

**Where will the cost log live?**

- [ ] Printed to terminal (capture with `tee logs/cost-log.txt`)
- [ ] Written to `logs/cost-log.md` as a markdown table
- [ ] Written to `logs/cost-log.csv`

---

## Section 5: Dependency Declaration

List every external service, API, and library your prototype will depend on today. This surfaces integration risks before you hit them mid-sprint.

| Dependency | Purpose | Fallback if unavailable |
|---|---|---|
| OpenRouter API | AI model calls | Google AI Studio direct |
| | | |
| | | |
| | | |

---

*Complete this document as a team in Part 1 of Lab 5. Save it to `docs/design-decisions-lab5.md` in your team repo before starting the sprint.*
