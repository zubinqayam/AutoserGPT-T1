
# Firebase Studio Test Plan — AutoserGPT‑T1 (v0.2.0)

## Import
1. Firebase Studio → Import Project
2. Repo URL: your GitHub URL
3. Workspace name: `autoser-t1`
4. (Optional) Mobile SDK Support → only if testing Android/Flutter
5. Import

## Setup
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Mock mode (free):** do nothing else.  
**Gemini (real output):**
```bash
export GEMINI_API_KEY=your_key
export GEMINI_PROVIDER=on
```

## Tests
```bash
pytest -q
```

## Run
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Endpoints
- GET `/` — health
- POST `/thinker/test` — {topic, language, depth}
- POST `/mrq/test` — {original_input, draft_output, min_questions}
- POST `/alga/test` — {spec_text}
- POST `/alga/score` — one-liner
- GET `/deepsearch/test?q=...` — web summary (offline-safe)
- GET `/thinker/stream?topic=...&language=en` — streaming demo
