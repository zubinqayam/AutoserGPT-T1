
# AutoserGPT‑T1 · v0.2.0

![Google Developer](https://img.shields.io/badge/Google_Developer-blue?logo=google) ![Microsoft Certified](https://img.shields.io/badge/Microsoft_Azure_Certified-blue?logo=microsoft-azure)

**AutoserGPT‑T1** is a minimal, cost‑safe API scaffold for the AutoserGPT Workstation family. It includes endpoints for **Thinker**, **Mr.Q**, **ALGA**, and **DeepSearch**, plus a streaming demo, CI tests, Docker, and a Firebase Studio checklist.

> Default mode is **FREE**: deterministic mocks. Add keys later to enable real providers.

## Endpoints
| Route | Method | Purpose |
|---|---|---|
| `/` | GET | Health JSON with version |
| `/thinker/test` | POST | Thinker orchestration (Engine‑A = Gemini if enabled; Engine‑B = mock) |
| `/thinker/stream` | GET | Streaming chunks for Engine‑A + one takeaway |
| `/mrq/test` | POST | ≥10 probing questions (deterministic) |
| `/alga/test` | POST | ALGA JSON report |
| `/alga/score` | POST | **One‑liner**: `ALGA Error %: ... (Crit:..., High:..., Med:..., Low:... / N checks)` |
| `/deepsearch/test` | GET | Fetch & summarise (offline‑safe; mock fallback) |

## Quickstart
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```

### Optional: enable **free** real AI (Gemini)
```bash
export GEMINI_API_KEY=your_key
export GEMINI_PROVIDER=on
# optional:
export GEMINI_MODEL=gemini-1.5-flash
```

## Files
- `app.py` — API
- `modules/` — thinker, mrq, alga, deepsearch, providers
- `ratelimit.py` — sliding‑window limiter
- `tests/` — CI‑safe tests
- `runbooks/` — rollback, backups, PII override, deprecation
- `SECURITY.md` — platform controls
- `VERSION` — 0.2.0
- `CHANGELOG.md` — release notes

## Trademark & License
- **ZQ AI LOGIC™** is a proprietary trademark of **Zubin Qayam**.
- Licensed under **ZQ AI LOGIC™ Proprietary License** (see `LICENSE`).  
© 2025 Zubin Qayam. All Rights Reserved.
