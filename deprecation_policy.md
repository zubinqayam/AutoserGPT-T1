
# API Deprecation Policy

- Public APIs versioned as `/v{n}/...`.
- 90‑day deprecation window with notices at T‑30/15/7 days:
  - Email to subscribers
  - Changelog entry
  - Response header: `Deprecation: true; sunset="<date>"`
- Releases blocked if communication steps are missing.

**Owner:** API Steward
