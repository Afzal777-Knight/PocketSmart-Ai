# PocketSmart AI

FastAPI + Jinja2 + SQLite + Gemini budget recommendation application.

## Setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `GEMINI_API_KEY` if you want live Gemini AI.

Run:

```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and http://127.0.0.1:8000/docs.

Test:

```bash
pytest -q
```

The catalog is intentionally simulated. It does not pretend to scrape or access Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO live.
