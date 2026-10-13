# Secure web baseline

Use this as a risk-based checklist, not as a certification rubric. Tailor it to the application's architecture and threat model. Record the exact framework versions and requirements used in a review.

## Threat-model minimum

Document the assets, actors, trust boundaries, data flows, abuse cases, and security objectives that matter to the requested change. Include the browser, API, background jobs, storage, identity provider, third-party SDKs, administrators/support staff, and deployment/CI system when they can affect the path. Mark unknown boundaries as gaps rather than assuming they are trusted.

## Control families

| Family | Secure-default questions | Useful evidence |
| --- | --- | --- |
| Input and output | Are inputs validated for type, size, encoding, and business rules? Are database, shell, template, HTML, URL, and command contexts protected with the right parameterization or encoding? | Unit/integration tests for hostile values; code review; negative cases |
| Identity and sessions | Are authentication, password recovery, MFA, session rotation, cookie flags, expiration, and logout behavior appropriate to risk? Are credentials and tokens kept out of URLs and logs? | Auth-flow tests; cookie/header inspection; provider configuration |
| Authorization and tenancy | Is every protected operation authorized server-side for the acting identity, resource, role, and tenant? Are object IDs and admin paths resistant to guessing or confused-deputy behavior? | Matrix tests for allow/deny cases; route/service evidence |
| Browser and cross-origin | Are CSP, framing, referrer, MIME, CORS, CSRF, and cross-site cookie decisions intentional for the app? Are dangerous sinks and third-party scripts reviewed? | Response-header checks; browser tests; dependency inventory |
| Data lifecycle | Is collection minimized? Are sensitive fields encrypted in transit and at rest where appropriate, access-limited, retained, deleted, and excluded from telemetry and backups where promised? | Data-flow map; retention/deletion tests; access logs with redaction |
| Server and network | Are SSRF, path traversal, unsafe redirects, uploads, deserialization, resource exhaustion, and error disclosure addressed? Are outbound destinations and parser limits constrained? | Boundary tests; sandboxing/config review; safe failure checks |
| Secrets and operations | Are secrets injected at runtime, rotated, scoped, and absent from Git and logs? Are alerts, audit events, backups, recovery, and incident ownership defined? | Secret scan; deployment config; runbook; restore/alert test |
| Dependencies and supply chain | Are dependencies pinned or controlled, provenance/updates reviewed, build artifacts protected, and CI permissions minimal? | Lockfile review; dependency scan; CI permission/config review |
| Abuse and resilience | Are rate limits, quotas, idempotency, anti-automation, moderation, and fraud controls appropriate without creating a privacy or accessibility problem? | Abuse-case tests; limits and alert evidence |

## Minimum implementation posture

- Enforce authorization at the server/service boundary and default to deny.
- Use parameterized queries and context-specific output encoding; do not treat generic sanitization as a universal fix.
- Validate and bound uploads, parsing, pagination, batch size, recursion, timeouts, and outbound requests.
- Use secure session and cookie settings, transport security, CSRF defenses where applicable, and explicit CORS allowlists.
- Keep secrets in an approved secret store or runtime environment; never hard-code them or echo them in errors.
- Redact personal, credential, token, payment, and health data from logs, traces, analytics, screenshots, and test fixtures.
- Make deletion and retention behavior testable across primary storage, caches, queues, replicas, backups, and vendor APIs where the product promises it.
- Review third-party scripts, SDKs, webhooks, OAuth scopes, subprocessors, and CI/build permissions as part of the attack surface.
- Prefer reversible, observable changes. For production or incident work, define rollback, evidence preservation, and owner approval before mutation.

## Framework use

- **OWASP ASVS:** use the official project as a requirements and verification catalog for web-application controls. Pin the exact release/tag in the requirement map; version-qualify requirement IDs because identifiers can change.
- **OWASP Top 10:** use the current official release for awareness and prioritization, not as a complete test plan or proof of security.
- **NIST SP 800-218 (SSDF):** use it to organize secure-development practices, provenance, vulnerability handling, and recurrence prevention.
- **NIST CSF 2.0:** use it for risk-governance language and organizational outcomes; tailor it to the product instead of claiming framework compliance from a checklist.

Authoritative starting points:

- OWASP ASVS: <https://owasp.org/projects/asvs>
- OWASP Top 10: <https://owasp.org/projects/top-ten>
- NIST SP 800-218 SSDF: <https://csrc.nist.gov/pubs/sp/800/218/final>
- NIST CSF 2.0: <https://www.nist.gov/cyberframework>

## Finding format

For a review, report each material issue with:

```text
ID: stable local identifier
Severity: critical | high | medium | low | informational
Confidence: high | medium | low
Location: file, route, component, or configuration
Evidence: exact behavior or source-backed observation
Attack/failure path: realistic consequence and preconditions
Legal/contract relevance: requirement, promise, or open question (never an unsupported legal conclusion)
Fix: smallest safe remediation and any design decision
Verification: test/check run and result
Residual risk: what remains unverified or accepted
```

Do not suppress a finding merely because a policy says the behavior is allowed. Do not label a policy gap as a vulnerability without connecting it to a real security or contractual risk.
