
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from modules.thinker import thinker_run
from modules.mrq import mrq_review
from modules.alga import alga_run
from modules.deepsearch import fetch_and_summarize
from modules.providers import call_model
from ratelimit import limiter

app = FastAPI(title="AutoserGPT T1", version="0.2.0")

class ThinkerReq(BaseModel):
    topic: str
    language: str = "en"
    depth: int = 2

class MrQReq(BaseModel):
    original_input: str
    draft_output: str
    min_questions: int = 10

class ALGAReq(BaseModel):
    spec_text: str

@app.get("/")
def health():
    return {"ok": True, "app": "AutoserGPT T1", "status": "live", "version": app.version}

@app.post("/thinker/test")
@limiter(limit=20, window_sec=60)
def thinker_test(req: ThinkerReq):
    result = thinker_run(topic=req.topic, language=req.language, depth=req.depth)
    return {"ok": True, "result": result}

@app.get("/deepsearch/test")
@limiter(limit=10, window_sec=60)
def deepsearch_test(q: str):
    return fetch_and_summarize(q)

@app.post("/mrq/test")
@limiter(limit=30, window_sec=60)
def mrq_test(req: MrQReq):
    qs = mrq_review(req.original_input, req.draft_output, req.min_questions)
    return {"ok": True, "questions": qs, "count": len(qs)}

@app.post("/alga/test")
@limiter(limit=30, window_sec=60)
def alga_test(req: ALGAReq):
    report = alga_run(req.spec_text)
    return {"ok": True, "report": report}

# New: ALGA score one-liner endpoint
@app.post("/alga/score")
@limiter(limit=30, window_sec=60)
def alga_score(req: ALGAReq):
    report = alga_run(req.spec_text)
    sev = report["severity"]
    line = (
        f"ALGA Error %: {report['ALGA_Error_%']}% — "
        f"(Crit:{sev['Crit']}, High:{sev['High']}, Med:{sev['Med']}, Low:{sev['Low']} / {report['total']} checks)"
    )
    return {"ok": True, "score": line}

# Streaming endpoint (Engine-A chunks + one takeaway)
@app.get("/thinker/stream")
@limiter(limit=10, window_sec=60)
def thinker_stream(topic: str, language: str = "en"):
    def generate():
        text = call_model(
            f"Engine-A (stream): Research '{topic}' in {language}. "
            f"Give 6 short bullets; keep each bullet under 20 words.",
            provider_hint="gemini"
        )
        for line in text.splitlines():
            chunk = line.strip()
            if not chunk:
                continue
            yield chunk + "\n"
        ref = call_model("Referee: Produce one actionable takeaway (<=20 words).")
        yield "\n-- Takeaway --\n" + ref + "\n"
    return StreamingResponse(generate(), media_type="text/plain")
