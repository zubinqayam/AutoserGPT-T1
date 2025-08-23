
# SECURITY — Platform Controls (AutoserGPT‑T1 v0.2.0)

- **Encryption at rest:** Provider encryption + CMEK/KMS; key rotation 365d; key IDs documented.
- **DLP/PII redaction:** Outbound artifacts pass PII redaction (pattern+ML); manual override logged; immutable audit.
- **API versioning:** `/v1/*`, 90‑day deprecations; `x-api-version` accepted; comms at T‑30/15/7 via email + changelog + header.
- **Network segmentation:** Private VPC; SG allow 80/443 only; egress allowlist; per‑service IAM roles.
- **Code signing:** All artifacts signed (cosign); deploy gate verifies signature/public key.
- **Logs & backups:** Logs 30d hot + 180d archive; WORM audit trail; daily backups; quarterly restore drill.
- **Performance & resilience:** SLO 99.5% uptime; p95 < 800ms; k6 monthly; chaos quarterly; release blocks if SLO violated.
- **Rate limits & cost controls:** 20 req/min/IP (burst 60), 429 w/ `Retry-After`; token & spend ceilings; paid providers off by default.

## Owners
- API Steward — name/email
- Security Lead — name/email
- SRE Lead — name/email
