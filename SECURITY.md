# SECURITY.md

## Overview
This repository implements a minimal but hardened security posture suitable for the AutoserGPT Workstation MVP.

## Secrets & Keys
- Store all API keys in GitHub Actions Secrets (never in code).
- Local signing keys (GPG or keyless Sigstore) must be stored in an encrypted vault.
- **Rotation cadence:** 90 days for API keys and signing keys.
- Enforce **TOTP MFA** for all accounts.

## Artifact Integrity & Authenticity
- Build artifacts are **checksummed (SHA-256)** and **cryptographically signed** via **Sigstore (cosign)** or **GPG**.
- Public verification info (fulcio/certificate chain or GPG public key) must be committed or referenced here.

### Verify (GPG example)
```bash
gpg --keyserver keyserver.ubuntu.com --recv-keys <PUBKEY_ID>
gpg --verify release/signature.asc release/thinker_report_<RUN>.pdf
sha256sum -c release/checksums.sha256
```

### Sign (GPG example)
```bash
gpg --armor --output release/signature.asc --detach-sign release/thinker_report_<RUN>.pdf
sha256sum release/* > release/checksums.sha256
```

### Verify (Sigstore / cosign example)
```bash
cosign verify-blob --certificate release/cosign.cert   --signature release/cosign.sig --bundle release/cosign.bundle   --certificate-oidc-issuer https://token.actions.githubusercontent.com   --certificate-identity 'https://github.com/<ORG>/<REPO>/.github/workflows/ci.yml@refs/heads/main'   --insecure-ignore-tlog=true   --yes   <BLOB_PATH>
```

### Sign (Sigstore / cosign example — keyless in CI)
```bash
cosign sign-blob --yes --output-certificate release/cosign.cert   --output-signature release/cosign.sig   --bundle release/cosign.bundle <BLOB_PATH>
```

## SBOM & Vulnerabilities
- Generate a **CycloneDX SBOM** on every build and perform vulnerability scanning with **osv-scanner**.
- CI **fails on High/Critical** vulnerabilities.
- SBOM and vuln report are published with each release.

## DLP & Privacy
- Regex detectors + allow/deny lexicons.
- **5% human QA sampling** before export; store QA decisions and a **redaction preview** artifact.
- Retain QA artifacts for 30 days (dev) / 90 days (prod).

## Trigger Guardrails & RBAC
- Require **API key + nonce**; **rate-limit 10/min per IP** and **daily cap per user**.
- Roles: **Owner / Operator / Viewer**; all runs produce an **audit log** entry.

## Incident Response
- See `ops/incident_response.md`. RPO ≤ 24h / RTO ≤ 8h.
- Quarterly **restore drill**; outcomes recorded in ALGA Layer3.

## Time Sync
- Runners and build hosts must use NTP; CI logs clock skew prior to signing.

## Review Policy
- **Two-person review** (Owner + Operator) required before a release passes the gate.
