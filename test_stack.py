
from fastapi.testclient import TestClient
from app import app

def test_health():
    c = TestClient(app)
    r = c.get("/")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_thinker():
    c = TestClient(app)
    r = c.post("/thinker/test", json={"topic": "matrix algorithm", "language": "en", "depth": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True
    assert "engine_a" in body["result"] and "engine_b" in body["result"]

def test_mrq():
    c = TestClient(app)
    r = c.post("/mrq/test", json={"original_input": "spec", "draft_output": "answer", "min_questions": 10})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["count"] >= 10

def test_alga():
    c = TestClient(app)
    text = "We use KMS for encrypt. VPC and firewall. API v1. Logs rotate for 30 days. code signing"
    r = c.post("/alga/test", json={"spec_text": text})
    assert r.status_code == 200
    report = r.json()["report"]
    assert "ALGA_Error_%" in report
    assert report["total"] >= 5
