# Secure-launch scorecard

Use this scorecard as a release-preflight evidence sheet for a web or mobile app. It turns ten common security checks into verifiable controls. It is not a penetration test, certification, or proof that an app is safe.

Score each item:

- `verified` — the control is present, tested on the intended build/environment, and evidence is attached;
- `not verified` — missing, unknown, or only asserted by a vendor/UI setting;
- `not applicable — reason` — the product truly does not use the flow;
- `needs counsel/security owner` — a legal, risk, data, payment, or architecture decision remains open.

Do not use a magic threshold such as “seven out of ten means secure.” A score helps prioritize work. One unverified high-impact control can matter more than several low-risk passes, and all ten checks leave other attack paths possible.

## Ten checks

### 1. HTTPS and transport security

Verify that production traffic uses valid TLS, HTTP redirects safely to HTTPS, sensitive cookies require secure transport, mixed content is absent, and transport configuration is monitored. For mobile, verify the platform's network-security policy, certificate validation, deep links, and embedded WebViews. Consider HSTS after a controlled rollout and domain inventory.

Evidence: external header/TLS check, deployment configuration, cookie inspection, mixed-content scan, mobile network-security test, owner/date.

### 2. Passwords are hashed, never plaintext

Verify that passwords are processed with a maintained password KDF and unique salts, never stored or logged in plaintext, never reversibly encrypted as a substitute for hashing, and never exposed in support, analytics, crash, backup, or test data. Verify parameters, upgrade path, reset behavior, and access controls around password records.

Evidence: redacted schema/config review, KDF test, secret/log scan, recovery test, dependency/version record. Do not print hashes or credentials.

### 3. Bot and abuse protection

Verify server-side limits and abuse controls for signup, login, password recovery, MFA, public forms, AI/costly operations, uploads, messaging, exports, and coupon or checkout flows where applicable. Use risk-based controls, accessible alternatives, privacy-safe telemetry, and enumeration-resistant responses. A CAPTCHA alone is not a complete abuse strategy.

Evidence: endpoint inventory, rate-limit/quotas, bot controls, concurrency tests, alert, accessibility check, tuning owner.

### 4. Sessions expire and can be revoked

Verify access-token/session expiry, refresh rotation, logout/revocation, password-change and deletion invalidation, secure cookie or platform storage settings, audience/issuer validation, and protection from fixation and replay. Choose lifetimes based on risk and user experience; do not promise that expiry stops every stolen-token attack.

Evidence: session matrix, cookie/token inspection, expired/revoked/reused-token tests, provider configuration, incident revocation procedure.

### 5. CSRF and cross-origin state changes are controlled

For cookie-authenticated browser actions, verify the framework's CSRF/token/origin defense on every state-changing route, safe methods for mutations, and intentional SameSite/CORS settings. For bearer-token or mobile APIs, verify the actual trust model and origin/deep-link protections instead of adding an irrelevant browser token.

Evidence: route inventory, same-origin/cross-origin tests, cookie/CORS configuration, failed-token test, documented exceptions.

### 6. Password reset is short-lived and single-use

Verify reset links/tokens are high-entropy, expire, work once, are bound to the intended account and purpose, are not logged or placed in analytics/referrers, and invalidate old sessions or credentials as the approved design requires. Avoid account enumeration and require proportional identity proof for high-risk recovery.

Evidence: expiry/reuse/cross-account tests, token storage review, referrer/log scrub, session invalidation test, recovery owner.

### 7. Database credentials are least-privilege

Verify client-visible keys are intentionally limited identifiers, not master/service credentials; privileged keys stay server-side; RLS, scoped queries, storage policies, and service roles are tested; migrations and jobs have only required access; and credentials can be rotated. A key name such as `anon`, `public`, or `service` is not proof of its permissions.

Evidence: redacted permission matrix, client-bundle inspection, database/storage policy tests, service-role path review, rotation record. Never commit a key to this repository.

### 8. Logs do not contain credentials or payment data

Verify logs, traces, analytics, crash reports, support exports, URLs, headers, request bodies, and error messages are scrubbed of passwords, access/reset tokens, session cookies, API keys, prompts, identity documents, and card data. Keep only the minimum operational context, protect access, and test the scrubbing pipeline. Avoid relying on “private logs” as permission to collect unnecessary data.

Evidence: redaction rules, synthetic secret/card-marker test, retention/access policy, vendor data map, sample output with values removed.

### 9. Billing, spend, and abuse alerts are active

Verify alerts for unusual payment volume, failed-payment spikes, refunds/chargebacks, webhook failures, AI/provider spend, quota exhaustion, credential abuse, and high-cost endpoint activity. Route alerts to an owner with a runbook, rate-limit/kill-switch/rollback capability, and privacy-safe context. Billing alerts detect selected signals; they do not detect every attack.

Evidence: alert rules, threshold rationale, test event, notification owner, runbook, escalation and containment path.

### 10. Backups are automated and restorable

Verify backups are scheduled, encrypted, access-controlled, isolated from the primary account/region where appropriate, retained according to the approved plan, and tested by restoring into a safe environment. Record recovery-point and recovery-time objectives, rollback ownership, deletion/retention interactions, and what vendor data is or is not included. “Backups enabled” without a restore test is not recovery evidence.

Evidence: schedule, backup health, access review, restore exercise, RPO/RTO decision, retention/deletion review, owner/date.

## Copy/paste audit prompt

```text
Run a secure-launch scorecard on this repository and deployment configuration. Verify, with evidence, these ten controls: HTTPS and transport security; password hashing; signup/public-form bot and abuse protection; session expiry and revocation; CSRF or the correct cross-origin defense; single-use expiring password reset; least-privilege database and storage credentials; log/trace/analytics scrubbing; billing, AI-spend, payment, webhook, and abuse alerts; and automated restorable backups. Inspect the real implementation rather than trusting UI settings or vendor names. For every item, report files/configuration, test performed, result, severity, owner, and remaining gap. Make only minimal safe changes in an authorized non-production environment; do not print secrets, use real personal/payment data, rotate live credentials, delete data, or claim that a score proves the app is secure.
```

## Follow-through

- Use [the launch preflight and store-rejection workflow](launch-preflight-and-store-rejection.md) for the four minimum gates, destructive-operation safety, and Apple rejection evidence.
- Use [the vibe-coded app security cheat sheet](vibe-coded-app-security-cheatsheet.md) for the broader 30-hole review and per-finding remediation prompts.
- Use [the production security and monetization baseline](production-security-and-monetization.md) for rate limits, authorization, secrets, monitoring, payments, webhooks, and vendor review.
- Use [the mobile app and app-store release checklist](mobile-app-release-checklist.md) for Apple/Google privacy, deletion, billing, UGC, AI, accessibility, and store evidence.

## Reference sources

- OWASP Application Security Verification Standard: <https://owasp.org/projects/asvs>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
- NIST Secure Software Development Framework: <https://csrc.nist.gov/pubs/sp/800/218/final>
