
import re
from fastapi.testclient import TestClient
from app import app

def test_alga_score() -> None:
    client = TestClient(app)
    query = (
        "We use KMS encrypt and DLP masking. API v1; VPC+firewall; cosign signatures; logs retention; chaos tests."
    )
    res = client.post("/alga/score", json={"spec_text": query})
    assert res.status_code == 200
    s = res.json()["score"]
    assert re.search(r"ALGA Error %: \d+\.\d% — \(Crit:\d+, High:\d+, Med:\d+, Low:\d+ / \d+ checks\)", s)
