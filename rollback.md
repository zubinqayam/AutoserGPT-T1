
# Rollback Runbook

1. Announce: "Rollback in progress" (Slack/Email).
2. Pin to last known good tag:
   - `git checkout <TAG>`; `docker pull <IMAGE@DIGEST>`
3. Deploy pinned image to all services.
4. Database: if needed, restore last snapshot; run idempotent migrations.
5. Verify smoke tests; lift traffic gradually (25% → 50% → 100%).
6. Post‑mortem doc within 48h.

**Owner:** SRE Lead
