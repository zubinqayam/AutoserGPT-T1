
from fastapi.testclient import TestClient
from app import app

def test_deepsearch_endpoint():
    c = TestClient(app)
    r = c.get("/deepsearch/test", params={"q": "autoser gpt workstation matrix algorithm"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert "summary" in data and isinstance(data["summary"], str)
