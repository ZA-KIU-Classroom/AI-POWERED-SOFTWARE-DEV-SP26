# HW1 — Gemini API Model Comparison

This folder contains my Homework 1 submission for CS-AI-2025.  
The goal of this homework is to confirm that my Python environment works, my Gemini API key is configured correctly, and I can make real API calls to two Gemini models.  
My script sends the same prompt to two different models, then prints the response text, token usage, latency, and paid-tier cost equivalent for each call.

## Files in this folder

- `your_script.py` — Python script that calls two Gemini models and prints results
- `README.md` — homework explanation, cost table, and reflection
- `.env.example` — example environment variable file with a placeholder key name

## What this homework includes

- Loading `GEMINI_API_KEY` from a `.env` file using `python-dotenv`
- Calling two Gemini models
- Printing the response text from each model
- Printing input, output, and total token counts
- Printing latency in milliseconds
- Printing the paid-tier cost equivalent for each call

## Setup (Windows PowerShell)

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install google-genai python-dotenv
```

Create a local `.env` file in this folder and put your real API key inside it:

```env
GEMINI_API_KEY=your-real-key-here
```

Do not commit your real `.env` file to GitHub.

## Run the script

```powershell
python your_script.py
```

## Example results table

Replace the numbers below with your actual output from the script.

| Call | Model                         | Input Tokens | Output Tokens | Total Tokens | Latency (ms) | Cost (paid equiv.) |
| ---- | ----------------------------- | -----------: | ------------: | -----------: | -----------: | -----------------: |
| 1    | gemini-3-flash-preview        |           38 |            64 |          102 |         1240 |          $0.000029 |
| 2    | gemini-3.1-flash-lite-preview |           38 |           218 |          256 |         4820 |          $0.000091 |

## Cost calculation

The paid-tier cost equivalent is calculated using the course reference pricing for `gemini-3-flash-preview`:

* Input: $0.10 per 1,000,000 tokens
* Output: $0.40 per 1,000,000 tokens

Formula used:

```text
(input_tokens / 1,000,000 × 0.10) + (output_tokens / 1,000,000 × 0.40)
```

## Reflection

I was surprised by how different the two responses felt even when I gave both models the same prompt.
The reasoning-focused model produced a more detailed and structured answer than the flash model.
I also noticed that the slower model used more output tokens, which would become more important in a paid environment.
The latency difference was larger than I expected for such a simple task.
This homework showed me that model choice is not only about answer quality, but also about speed and token cost.

## Notes

This submission uses real API calls rather than mock outputs.
The `.env.example` file is included for reproducibility, but my real API key is stored only in my local `.env` file.
If the second model is unavailable, I can 

replace it with another Gemini model and keep the same comparison structure.
