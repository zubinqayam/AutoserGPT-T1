
import re
from typing import Dict, List

MANDATORY = [
    ("Encryption at rest", r"encrypt|kms|sse|vault"),
    ("DLP/PII redaction", r"\bpii\b|redact|mask|anonym"),
    ("API versioning", r"version(ing)?\b|v\d"),
    ("Network segmentation", r"vpc|subnet|firewall|zero[- ]?trust"),
    ("Code signing", r"sign(ed|ing)|signature"),
    ("Log retention", r"retention|ttl|rotate"),
    ("Load/chaos testing", r"load[- ]?test|chaos"),
]

def alga_run(spec_text: str) -> Dict:
    checks: List[Dict] = []
    hits = 0
    for name, pattern in MANDATORY:
        found = bool(re.search(pattern, spec_text, flags=re.I))
        checks.append({"control": name, "pattern": pattern, "present": found})
        if found:
            hits += 1
    total = len(MANDATORY)
    missing = total - hits
    error_pct = round(100 * (missing / total), 1) if total else 0.0
    severity = {"Crit": 0, "High": 0, "Med": 0, "Low": 0}
    for c in checks:
        if c["control"] in ["Encryption at rest", "DLP/PII redaction"] and not c["present"]:
            severity["Crit"] += 1
    for c in checks:
        if c["control"] in ["Network segmentation", "Code signing"] and not c["present"]:
            severity["High"] += 1
    for c in checks:
        if c["control"] in ["API versioning", "Log retention", "Load/chaos testing"] and not c["present"]:
            severity["Med"] += 1
    return {
        "ALGA_Error_%": error_pct,
        "severity": severity,
        "hits": hits,
        "total": total,
        "checks": checks,
    }
