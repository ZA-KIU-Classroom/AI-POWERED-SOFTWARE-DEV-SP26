# HW1 Grading Rubric

**Assignment:** Homework 1 — Individual  
**Course:** CS-AI-2025 — Building AI-Powered Applications | Spring 2026  
**Total Points:** 5.0  
**Due:** Before Lab 2 — Friday 13 March 2026 (Group A: 09:00 | Group B: 11:00)

---

## Summary Rubric

| Component | Max Points | What is checked |
|---|---|---|
| Working script | 1.5 | Runs from a fresh clone with only a `.env` file added |
| Two models called | 1.0 | Both model strings present in code, both responses printed |
| Token and cost table | 1.0 | Table present with real numbers, cost formula correct |
| Reflection | 1.0 | 5 sentences, specific and personal — not generic |
| Repo structure + README | 0.5 | `/hw01` folder, README explains the work, no real key committed |
| **Total** | **5.0** | |

**Automatic deductions:**
- **-1.0** if the real API key is committed anywhere in the repository
- **-0.5** if the script crashes on a fresh clone (import errors, hardcoded paths, etc.)

---

## Detailed Component Descriptions

### Component 1: Working Script (1.5 points)

The submitted script(s) must run successfully on a fresh clone of the repository. The grader will:

1. Clone the repo
2. Create a `.env` file with a valid `GEMINI_API_KEY`
3. Install dependencies (`uv add google-genai python-dotenv` or `pip install google-genai python-dotenv`)
4. Run the script

| Score | Criteria |
|---|---|
| **1.5** | Script runs without errors, produces visible output showing both model responses, token counts, and latency for each call |
| **1.0** | Script runs with minor issues (one model fails, or output is partial but substantial work is clearly complete) |
| **0.5** | Script attempts to run but crashes partway through, or only one model is attempted |
| **0.0** | Script does not run at all, or no script is submitted |

---

### Component 2: Two Models Called (1.0 points)

The assignment requires calling at least two different Gemini model strings. The intent is that you observe real differences between a standard model and a reasoning model.

| Score | Criteria |
|---|---|
| **1.0** | Two distinct model strings appear in the code (e.g., `gemini-3-flash-preview` and `gemini-3.1-flash-lite-preview`). Both responses are printed to the terminal or saved to a file. |
| **0.5** | Only one model is called, but token counts and cost are tracked for that call. |
| **0.0** | No model calls made, or hardcoded fake responses. |

Acceptable second model alternatives if `gemini-3.1-flash-lite-preview` is unavailable: `gemini-3-flash-preview` or `gemini-3-flash-preview`.

---

### Component 3: Token and Cost Table (1.0 points)

A markdown table with one row per API call showing: model, input tokens, output tokens, total tokens, latency in ms, and the paid-tier cost equivalent.

| Score | Criteria |
|---|---|
| **1.0** | Table present with real numbers from actual API calls. Cost formula is correct: `(input_tokens / 1_000_000) * input_price + (output_tokens / 1_000_000) * output_price`. Values are plausible. |
| **0.5** | Table present but incomplete (missing columns, or values look copy-pasted from the spec rather than from actual calls). |
| **0.25** | Table present but clearly contains estimated or fabricated numbers. |
| **0.0** | No table submitted. |

---

### Component 4: Reflection (1.0 points)

Five sentences answering: what surprised you about the responses?

| Score | Criteria |
|---|---|
| **1.0** | Exactly or approximately 5 sentences. Specific — names a particular model, response, or observation. Honest — acknowledges something unexpected, not just "it was interesting". Sounds like the student's own voice and experience. |
| **0.5** | Reflection present but generic (could apply to any student's experience), or fewer than 3 substantive sentences. |
| **0.0** | No reflection, or clearly AI-generated text with no personal observation. |

---

### Component 5: Repository Structure and README (0.5 points)

| Score | Criteria |
|---|---|
| **0.5** | `/hw01` folder exists. `README.md` explains what was built. `.env.example` present with placeholder value. Real API key not committed anywhere. |
| **0.25** | README present but minimal, or `.env.example` missing. |
| **0.0** | No README, or real API key committed to the repo. |

---

## Automatic Deductions

**-1.0: API key committed to repository**  
This is Security Rule 1 from the lecture. If a real `GEMINI_API_KEY` value appears in any committed file (`.env`, `.py` file, README, anywhere), the full 1.0 point is deducted regardless of other scores. The key should also be revoked immediately.

**-0.5: Script fails on fresh clone**  
If the grader cannot run the script by following the README instructions, 0.5 points are deducted. This includes: missing `requirements.txt` or `pyproject.toml`, hardcoded absolute paths, imports of packages not in the dependency list.

---

## Common Mistakes

1. **API key in the code.** The most common and most serious mistake. Use `os.getenv("GEMINI_API_KEY")` with `load_dotenv()`, never a string literal.

2. **Usage data is None.** Free-tier models sometimes return `None` for `response.usage_metadata`. Always check before accessing it: `if response.usage_metadata:`.

3. **Both model calls use the same model string.** Read the requirement — two *different* model strings. The comparison between a standard and reasoning model is the educational point.

4. **Reflection is one generic sentence.** "The model gave a good response and I learned about tokens." This earns 0.0. Name something specific that actually surprised you.

5. **No `.env.example`.** You must show the key name without the key value so a grader can reproduce your setup. A file containing `GEMINI_API_KEY=your-key-here` is the minimum.

---

*Grading Rubric — HW1 — CS-AI-2025 Spring 2026*
