# Incident Response Plan (IRP)

## Purpose
Define roles, severity levels, communication, evidence preservation, and recovery steps for the AutoserGPT MVP.

## Roles (RACI)
- Owner (Zubin Qayam) — Accountable, final decisions, external comms.
- Operator — Leads technical triage, coordinates CI/CD and restore.
- Viewer — Observer, executes pre-approved tasks, documents steps.

## Severity & SLAs
- **SEV-1 (Outage / Data Exposure)**: Immediate response, status update within 1h, RTO ≤ 8h, RPO ≤ 24h.
- **SEV-2 (Degradation / Security Gap)**: Response within 4h, remediation within 72h.
- **SEV-3 (Minor / Cosmetic)**: Response within 1 business day, fix in next cycle.

## Evidence Preservation
- Freeze relevant logs and artifacts; export copies to `_archive/` with SHA-256 and signature.
- Record chain-of-custody: who handled, when, and where evidence was stored.

## Communication
- Internal: Notion IR page, GitHub issue labeled `incident`, email to stakeholders.
- External (if required): formal notice after triage with minimal sensitive details.

## Backup & Restore
- Nightly OneDrive versioned snapshot; Weekly export to `_archive/` (checksummed); Monthly offline copy.
- **Quarterly restore drill**: run on a fresh VM/container, document RTO/RPO, and lessons learned to ALGA Layer3.

## Red-Team & DLP Stress Tests
- Quarterly prompt pack to probe redaction/authz; log findings and create Locks for never-repeat.

## Post-Incident Review
- Root cause, contributing factors, and **action items**.
- Update Locks (never-repeat registry) and revise this IRP when needed.
