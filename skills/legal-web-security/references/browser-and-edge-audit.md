# Authorized browser and edge audit

Use this reference for a safe first-pass inspection of a web or browser-based app that was built quickly with an AI coding tool. It complements code review and server-side tests; browser DevTools cannot prove that an app is secure.

Run it only against an application and environment the tester owns or is explicitly authorized to assess. Use synthetic, non-sensitive accounts and data. Do not copy session cookies, access tokens, personal data, payment data, or private incident evidence into notes, chat, tickets, or an AI tool. Do not stress-test, flood, scan unrelated hosts, or replay requests against production without written scope and an approved test plan.

## Transcript-to-control map

| Observation | Primary control reference | Safe interpretation |
| --- | --- | --- |
| User text runs as code in another browser | [30-hole item 11](vibe-coded-app-security-cheatsheet.md#11-cross-site-scripting-and-unsafe-output-rendering) | Use context-specific output encoding; sanitize only approved rich text; do not treat a generic sanitizer or CSP as the whole fix. |
| Uploaded file executes or exposes the server | [30-hole items 14–16](vibe-coded-app-security-cheatsheet.md#category-4--files-and-user-generated-content) | Validate content and size, isolate storage, limit processing, and serve safely; extension checks alone are insufficient. |
| Fake payment success or webhook | [30-hole item 25](vibe-coded-app-security-cheatsheet.md#25-unsigned-replayable-or-non-idempotent-webhooks) and [the production payment baseline](production-security-and-monetization.md#payment-and-merchant-of-record-review) | Verify the provider signature and event state server-side, handle replay/order/idempotency, and do not grant access from a browser redirect. |
| API key or privileged token in the front end | [30-hole item 6](vibe-coded-app-security-cheatsheet.md#6-exposed-secrets-and-privileged-client-keys) | Anything shipped to a browser can be inspected. Public identifiers are not privileged credentials. |
| Unlimited endpoint abuse | [30-hole item 22](vibe-coded-app-security-cheatsheet.md#22-missing-rate-limits-brute-force-controls-and-bot-protection) | Use endpoint-specific server-side limits, quotas, and alerts; do not pick arbitrary thresholds or rely on a UI limit. |
| DDoS or edge-provider claim | [30-hole items 23 and 29](vibe-coded-app-security-cheatsheet.md#23-resource-exhaustion-and-ai-cost-abuse) | CDN/WAF/edge services may reduce some traffic and origin exposure, but protection depends on plan, configuration, architecture, provider limits, and tested failover. No vendor name is a guarantee. |
| Database role/RLS issue | [30-hole items 2–4](vibe-coded-app-security-cheatsheet.md#category-1--identity-and-authorization) | Test server-side resource and field authorization, database/storage policy, jobs, exports, and caches together. A browser result does not identify one missing database feature. |
| DevTools inspection | This reference | Treat it as evidence collection for an authorized test, not as permission to access another person's account or data. |

## 1. Prepare a safe test

Record the written scope, environment, build/commit, domains, test accounts, allowed routes, time window, data-retention plan, and stop conditions. Create two synthetic accounts with distinct records if object authorization is in scope. Use a harmless marker such as `SECURITY_TEST_001`; do not use a real name, email, card, prompt, or document.

Before opening DevTools:

- confirm the browser profile is dedicated to the test and has no personal sessions or extensions that may capture data;
- use staging or an approved test tenant wherever possible;
- disable or avoid third-party recording tools unless they are in scope and scrubbed;
- redact identifiers in screenshots and notes;
- stop when a response contains another person's data, a credential, or a production secret; preserve only the minimum authorized evidence and escalate.

## 2. Network panel

Inspect normal, login, logout, account-switch, CRUD, upload, download, export, AI, checkout, and deletion flows.

Check:

- request URLs, query strings, referrers, headers, bodies, and responses contain no passwords, access/reset tokens, session cookies, card data, or unnecessary personal data;
- APIs return only the fields the screen needs; inspect for over-fetching, internal IDs, roles, billing state, prompts, or other users' records;
- protected requests fail safely after logout, session expiry, role change, deletion, or tenant switch;
- resource URLs cannot be replayed by the second synthetic account; test the corresponding API/download request, not only the visible page;
- response headers and cache behavior do not make private data public or reusable across users;
- CORS, redirects, content types, and error responses match the intended trust boundary;
- client-side “success” or `?success=true` does not grant payment entitlement before server verification;
- webhook delivery is not confused with browser traffic: inspect the server endpoint and use a provider sandbox fixture for signature/state tests.

Do not save full HAR files by default. If a HAR is needed, use synthetic data, scrub cookies/auth headers/bodies, limit the route/time scope, protect the file, and delete it after the approved review.

## 3. Application and storage panels

Inspect cookies, local storage, session storage, IndexedDB, service-worker caches, WebSQL if present, and browser permissions.

Check:

- session cookies have appropriate `Secure`, `HttpOnly`, `SameSite`, domain, path, expiry, and partitioning decisions;
- long-lived access or refresh tokens are not stored in an unnecessarily exposed browser surface;
- logout, password reset, account deletion, and role changes remove or invalidate cached credentials and private data;
- service-worker and HTTP caches do not serve one user's response to another user or after logout;
- client configuration contains only intentionally public values; no database master key, service credential, signing key, payment secret, or model-provider secret is present;
- browser permissions, embedded frames, and third-party storage are limited to the documented purpose;
- consent state and optional SDK initialization match the approved privacy design.

Never paste a token or cookie value into a report. Record the storage location, cookie flags, key name, redacted value shape, and remediation owner.

## 4. Sources, bundles, and public build output

Inspect source maps, loaded JavaScript bundles, public environment variables, debug routes, error overlays, package metadata, and source references.

Check:

- no privileged secret is embedded in the bundle, source map, public asset, or HTML;
- debug logging, test accounts, admin routes, feature flags, stack traces, and development endpoints are not enabled unintentionally;
- public config and API base URLs do not create an unintended origin or environment crossing;
- third-party scripts and SDKs match the inventory, consent timing, permissions, and data destinations;
- build artifacts come from the reviewed commit and deployment environment.

Source-map availability is a risk decision, not automatically a vulnerability. The important question is whether it exposes secrets, sensitive source, or an attacker-useful path in the intended deployment.

## 5. Safe feature probes

### XSS

Submit only a harmless synthetic marker containing characters that require encoding, such as `<`, `>`, `&`, quotes, and a URL-like string. Verify it displays as text in comments, usernames, search results, notifications, markdown, rich text, emails, previews, and admin screens. Do not use an exploit payload against a live or unrelated target. Trace the output context in code and apply the corresponding encoding or approved rich-text sanitizer.

### File uploads

In an authorized test environment, use inert small files and controlled mismatch cases to verify allowlists, content inspection, size/count limits, generated names, non-executable storage, safe content type/disposition, authorization, scanning/quarantine, and deletion. Do not upload malware, a server-side executable, a real document, or an archive bomb. Test the download/preview path and the processor boundary without attempting takeover.

### Payment webhooks

Use the provider's sandbox or local signed fixtures. Verify invalid signatures, altered bodies, old/replayed events, wrong-account events, duplicates, pending payment, refund, cancellation, and out-of-order delivery are rejected or handled idempotently. Never forge a production payment or use a browser success page as proof of payment.

### Rate limits and edge protection

Use configured low-volume boundary tests, not traffic floods. Verify the server enforces limits after client-side controls are bypassed, returns safe responses, emits alerts, and preserves an accessible recovery path. Inspect CDN/WAF/edge configuration, origin access, caching, provider plan, quotas, and failover with the owner. Do not conduct a DDoS simulation without a written scope, provider approval, and an isolated test plan.

## 6. Evidence and remediation

| Area | Evidence to record | Status/owner |
| --- | --- | --- |
| Network | Redacted route/method/status, response-field review, logout/account-switch denial |  |
| Storage | Cookie flags, token-storage decision, cache/service-worker behavior |  |
| Bundle/config | Secret scan result, public-config review, debug/source-map decision |  |
| XSS | Synthetic marker context test, output location, encoding/sanitizer path |  |
| Uploads | Inert file/type/size/access tests, storage and serving configuration |  |
| Webhooks | Sandbox signature/replay/idempotency/pending/refund test evidence |  |
| Limits/edge | Endpoint limits, low-volume boundary test, alerts, origin/plan/config review |  |

For each finding, record the affected route/component, realistic consequence, severity/confidence, minimum safe fix, owner, test, and residual gap. Remove the test data and artifacts according to the approved retention plan.

## Copy/paste authorized audit prompt

```text
Review this app in an explicitly authorized staging/test environment using browser DevTools and the repository. Use synthetic non-sensitive accounts and data only. Inspect Network, Application/Storage, Sources/build output, and safe low-volume feature probes for: client-exposed privileged keys; tokens or personal/payment data in URLs, responses, logs, storage, or caches; over-fetching; front-end-only authentication/authorization; cookie/session flags; XSS output contexts; upload validation/isolation; payment success versus server-verified webhook state; endpoint rate limits; and edge/WAF/origin configuration. Add or propose the smallest server-side fixes and focused negative tests. Do not stress-test, forge production payments, upload malware, probe unrelated hosts, copy credentials/tokens into notes, change production, or claim that a provider or DevTools review proves security. Return redacted evidence, files/configuration, test results, severity, owners, and remaining gaps.
```

## Related references

- [Vibe-coded app security cheat sheet](vibe-coded-app-security-cheatsheet.md)
- [Production security and monetization baseline](production-security-and-monetization.md)
- [Secure-launch scorecard](secure-launch-scorecard.md)
- [Launch preflight and store-rejection workflow](launch-preflight-and-store-rejection.md)
- OWASP ASVS: <https://owasp.org/projects/asvs>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
