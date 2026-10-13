# Vibe-coded app security cheat sheet

Use this reference to review or harden a fast-built web or mobile app before real users, sensitive data, AI spend, or paid access are exposed. It contains 30 defensive review targets in eight categories. Each item includes a standalone prompt for an AI coding assistant.

This is not a guarantee that an app is “hack-proof,” a penetration test, a certification, or an App Store approval formula. The prompts must be applied to the actual repository, architecture, deployment configuration, data, and threat model. Never paste secrets, production personal data, or private incident evidence into an AI coding tool.

## Safe prompt contract

Every prompt below is intended to be copied into an AI coding assistant. The assistant should:

- inspect the repository and identify the actual files, routes, services, providers, and deployment assumptions before editing;
- preserve existing security controls and user-visible behavior unless a safer change requires a documented behavior change;
- enforce security at the server, service, database, storage, or build boundary—not only in client-side code;
- avoid inventing credentials, users, policies, data, vendor guarantees, or compliance conclusions;
- make the smallest safe patch, add focused negative tests, run the available checks, and report files changed, assumptions, failed checks, and remaining gaps;
- never print or commit secrets, raw personal data, exploit payloads aimed at a live target, or production tokens;
- stop and ask for an owner decision when a change would delete data, rotate a live credential, change billing, weaken access, or alter a legal/security promise.

Use the status labels `verified`, `not verified`, `not applicable — reason`, `assumed`, and `needs counsel`. A passing test covers only the behavior it actually exercises.

## Category 1 — Identity and authorization

### 1. Missing server-side authentication

**Look for:** protected routes that trust the UI, client flags, hidden buttons, unsigned IDs, or an unverified session; background jobs and file endpoints that bypass the main auth middleware.

**Copy/paste prompt:**

```text
Review this repository for protected routes, server actions, API handlers, background jobs, file access, and WebSocket or RPC endpoints that can be reached without server-side authentication. Trace the identity from the request to the authorization decision. Add the smallest safe deny-by-default enforcement, preserve public routes intentionally marked public, and add allow/deny tests for anonymous and authenticated requests. Do not trust client state or invent an auth provider. Report every route you could not verify and any required configuration or owner decision.
```

### 2. Broken object-level authorization (IDOR/BOLA)

**Look for:** `/users/:id`, document IDs, storage keys, conversation IDs, exports, or download links that can be swapped to access another user's or tenant's record.

**Copy/paste prompt:**

```text
Audit every read, update, delete, download, export, and nested-resource path that accepts an object ID. Test same-user, different-user, different-tenant, deleted-object, and guessed-ID cases. Enforce ownership or approved membership in the server query and service layer, not only in the UI, and add regression tests proving cross-object access is denied without leaking whether the object exists. Do not change data or run tests against production.
```

#### Authorized manual replay test

Run this only against an app and environment that the tester owns or is explicitly authorized to assess. Use synthetic, non-sensitive records and stop after the minimum proof:

1. Create two test accounts, for example `john-test` and `nancy-test`, with distinct sentinel records.
2. Sign in as John, open one of John's records, and save the URL and the corresponding API/download request in the approved test notes. Do not save real personal data, cookies, tokens, or credentials.
3. End John's session, sign in as Nancy, and replay the same URL and request.
4. Expect a consistent authorization denial—often `401`, `403`, or a carefully designed not-found response—with no record body, metadata, file, cache hit, or sensitive error difference.
5. Repeat only within the approved scope for read, update, delete, download, export, nested-resource, GraphQL/RPC, and storage paths. Confirm Nancy cannot modify or delete John's sentinel record.
6. Clean up the test accounts and records, preserve the request/response status and build/environment as evidence, and report the smallest reproducible finding.

A successful replay demonstrates an access-control failure; it does not by itself prove that row-level security is missing. The fix may require database policy, scoped queries, service-layer authorization, storage rules, or more than one boundary.

**Copy/paste manual-test prompt:**

```text
In an explicitly authorized staging or test environment only, create two synthetic accounts with distinct non-sensitive records. Sign in as the first account, capture one record URL and its corresponding request, end that session, sign in as the second account, and replay the URL/request. Verify that read, update, delete, download, export, nested-resource, and storage variants are denied without a body, metadata, cache, or error side-channel leak. Stop after the minimum proof, clean up all test data, and report the build, route, status, and remediation boundary. Do not test an unrelated live site, use real personal data, or print cookies, tokens, or credentials.
```

### 3. Broken function-level authorization and privilege escalation

**Look for:** admin/support routes, role fields supplied by clients, hidden admin links, weak role checks, horizontal/vertical escalation, and service accounts with broad permissions.

**Copy/paste prompt:**

```text
Build an authorization matrix for every role, tenant, admin, support, automation, and service account found in this repository. Review every privileged route and mutation for server-side role and scope checks. Default to deny, separate administrative actions from customer actions, prevent client-controlled role changes, and add tests for horizontal and vertical privilege escalation. Preserve approved support workflows and report any ambiguous role policy instead of guessing.
```

### 4. Mass assignment and field tampering

**Look for:** spreading request bodies into ORM updates, accepting `role`, `ownerId`, `tenantId`, `status`, `price`, `verified`, or entitlement fields from clients, and unsafe bulk updates.

**Copy/paste prompt:**

```text
Find every create, update, patch, bulk-update, and import path that maps client input to persistent fields. Replace broad object spreading with explicit allowlists and server-owned fields. Enforce ownership, immutable fields, state transitions, and authorization on the server. Add tests proving a client cannot change roles, ownership, tenant, billing state, verification, or other protected fields. Do not silently discard a business-critical field; flag it for an owner decision.
```

### 5. Session, token, and account-recovery flaws

**Look for:** long-lived tokens, tokens in URLs or local storage without a risk decision, missing rotation/revocation, weak reset links, session fixation, insecure cookies, and account enumeration.

**Copy/paste prompt:**

```text
Trace login, logout, session refresh, password reset, email verification, MFA, magic links, OAuth callbacks, and account deletion. Harden the existing design with appropriate expiry, rotation, revocation, single-use recovery tokens, secure cookie or platform-storage settings, replay protection, and enumeration-resistant responses. Add focused tests for expired, reused, revoked, cross-user, and post-deletion credentials. Do not replace the identity system or change recovery policy without documenting the decision.
```

## Category 2 — Secrets and configuration

### 6. Exposed secrets and privileged client keys

**Look for:** API keys, access tokens, database credentials, signing keys, service-role keys, `.env` files, source maps, mobile bundles, screenshots, logs, and copied secrets in Git history.

**Copy/paste prompt:**

```text
Scan the tracked files, configuration, build output if available, client bundles, and scripts for secrets or privileged keys. Classify public identifiers separately from credentials, remove secrets from source and client artifacts, replace them with protected runtime configuration or a secret manager reference, and add a safe secret-scanning check. Do not print discovered values or rotate a live credential automatically; report the redacted location and the authorized rotation steps required.
```

### 7. Unsafe runtime configuration, CORS, and security headers

**Look for:** wildcard origins with credentials, environment mix-ups, debug flags in production, unsafe redirects, permissive framing, missing CSP/referrer/MIME/clickjacking headers, and insecure WebView or deep-link settings.

**Copy/paste prompt:**

```text
Review environment loading, origin allowlists, redirects, CORS, cookies, CSP, framing, referrer policy, MIME sniffing, transport settings, WebViews, deep links, and production flags. Tighten configuration to the smallest documented set of origins and capabilities, preserve intentional integrations, and add header/configuration tests for allowed and denied cases. Do not use a wildcard or disable a browser control as a shortcut; list any deployment value that must be supplied by the owner.
```

### 8. Debug endpoints and verbose error disclosure

**Look for:** stack traces, SQL/provider errors, source maps, health/debug routes, admin consoles, test accounts, verbose logs, and error messages that reveal tokens, schema, filesystem paths, or user existence.

**Copy/paste prompt:**

```text
Inspect production error handling, debug routes, health checks, source-map exposure, logs, and client error surfaces. Remove or protect nonessential diagnostics, return stable non-sensitive error responses, preserve correlation IDs, and redact credentials, personal data, queries, filesystem paths, and provider responses. Add tests for production and development behavior without hiding useful operator diagnostics from authorized channels.
```

## Category 3 — Input, injection, and browser attacks

### 9. SQL, NoSQL, and ORM injection

**Look for:** string-built queries, dynamic filters, raw SQL, unsafe sort/field selection, operator injection, and query parameters passed without type or size bounds.

**Copy/paste prompt:**

```text
Trace every user-controlled value into SQL, NoSQL, ORM, search, reporting, and ordering queries. Replace string concatenation or unsafe operator construction with parameterized APIs and allowlisted fields, then validate types, sizes, pagination, and business constraints at the server boundary. Add negative tests for quotes, operators, wildcards, unexpected fields, and large inputs. Do not weaken authorization while changing query code.
```

### 10. Command, template, expression, and code injection

**Look for:** shell calls, `eval`, dynamic template compilation, unsafe expression engines, deserialization, plugin execution, and user-controlled filenames or arguments.

**Copy/paste prompt:**

```text
Find all paths from untrusted input to shell commands, process execution, template compilation, expression evaluation, deserialization, plugins, or dynamic imports. Remove the dynamic execution where possible; otherwise use a fixed operation allowlist, safe parameter APIs, strict resource limits, isolation, and least privilege. Add tests proving hostile values remain data. Do not “sanitize” a dangerous interpreter and call it fixed without explaining the remaining boundary.
```

### 11. Cross-site scripting and unsafe output rendering

**Look for:** raw HTML, unsafe DOM sinks, markdown/rendering plugins, untrusted URLs, `dangerouslySetInnerHTML`-style APIs, rich-text previews, and insufficient output encoding.

**Copy/paste prompt:**

```text
Trace untrusted data into HTML, DOM, markdown, URL, email, PDF, WebView, and template output contexts. Use context-appropriate escaping or a narrowly configured sanitizer, remove unsafe rendering where not required, validate URL schemes, and add tests for stored, reflected, DOM, rich-text, and attribute-context payloads in a non-production environment. Keep CSP as defense in depth, not the sole fix.
```

### 12. Cross-site request forgery and unsafe state changes

**Look for:** cookie-authenticated mutations without CSRF protection, state changes through GET, weak SameSite assumptions, cross-origin forms, and missing origin checks.

**Copy/paste prompt:**

```text
Review all cookie-authenticated state-changing routes, including account, billing, deletion, admin, and webhook-adjacent actions. Prevent state changes over unsafe methods, add the framework's correct CSRF/origin defense, preserve secure SameSite cookie behavior, and add tests for same-origin, cross-origin, missing-token, replay, and API-token cases. Do not add a custom crypto scheme or exempt a route without documenting why it has a different trust model.
```

### 13. SSRF, unsafe redirects, and unbounded outbound requests

**Look for:** user-provided URLs, image fetchers, webhooks, previewers, importers, redirects, DNS rebinding, cloud metadata access, and arbitrary internal-network egress.

**Copy/paste prompt:**

```text
Audit every outbound HTTP, DNS, redirect, preview, webhook, and import path that can be influenced by a user. Apply an explicit destination policy, scheme and host validation, redirect limits, DNS/IP protections, timeout and response-size bounds, egress restrictions, and safe error handling. For redirects, allowlist destinations and prevent credential leakage. Add non-production tests for private addresses, rebinding-shaped inputs, unsupported schemes, long chains, and oversized responses.
```

## Category 4 — Files and user-generated content

### 14. Unrestricted or unsafe file uploads

**Look for:** extension-only checks, unlimited size/duration, executable paths, public-by-default objects, archive bombs, missing malware scanning, and processing before authorization.

**Copy/paste prompt:**

```text
Review every upload, import, attachment, avatar, media, and AI-file path. Enforce authenticated ownership, explicit type/size/count/duration limits, content inspection, safe generated names, isolated non-executable storage, malware or provider scanning where appropriate, bounded processing, and access-controlled serving. Add tests for mismatched MIME/extension, oversized files, archives, executable content, unauthorized downloads, and deletion. Do not upload real user data during testing.
```

### 15. Path traversal and local-file exposure

**Look for:** filenames or paths concatenated into filesystem operations, archive extraction, static-file routes, template includes, export paths, and object keys that accept `../` or encoded variants.

**Copy/paste prompt:**

```text
Trace user-controlled filenames, object keys, archive entries, and path parameters into filesystem or storage operations. Replace path concatenation with opaque IDs or safe joins rooted in an approved directory, canonicalize before authorization, reject traversal and symlink escapes, and keep storage outside executable/static paths. Add tests for encoded traversal, absolute paths, symlinks, archive entries, and cross-tenant files.
```

### 16. Active content and unsafe media processing

**Look for:** SVG/HTML uploads, embedded scripts, document macros, image/PDF converters, metadata leaks, content sniffing, and files served inline with an unsafe content type.

**Copy/paste prompt:**

```text
Inventory file types that can contain scripts, links, macros, active content, or sensitive metadata and every converter or previewer that touches them. Remove active content or serve downloads with safe disposition and type headers, isolate parsers, bound resources, and strip metadata where the approved product behavior allows it. Add tests for SVG/HTML/document previews, content-type confusion, malicious metadata, parser errors, and cross-user access.
```

### 17. UGC abuse, moderation, and reporting gaps

**Look for:** public posts, comments, messages, feedback boards, or AI outputs without reporting, blocking, moderation ownership, rate limits, deletion, privacy controls, or copyright/takedown handling.

**Copy/paste prompt:**

```text
Map every user-generated-content surface and its visibility, storage, search, sharing, moderation, and deletion paths. Add or verify content rules, report and block controls, abuse rate limits, moderator authorization, audit-safe actions, private-by-default handling for sensitive content, and a deletion/takedown workflow. Do not invent legal conclusions; flag jurisdiction, child-safety, copyright, and platform-policy decisions for the owner or counsel.
```

## Category 5 — Data privacy and storage

### 18. Excessive collection and PII leakage

**Look for:** unnecessary form fields, precise location, contacts, identifiers, prompts, analytics events, logs, screenshots, and vendor transfers unrelated to the feature.

**Copy/paste prompt:**

```text
Create a field-level data-flow inventory for this feature from collection through logs, analytics, support, backups, and vendors. Remove fields and telemetry not necessary for the stated purpose, make optional processing explicit, redact identifiers from diagnostics, and update the relevant policy or vendor map only after behavior is confirmed. Do not delete or change required business data without an owner decision; report retention and jurisdiction questions.
```

### 19. Weak password and cryptographic handling

**Look for:** plaintext or reversible password storage, homemade crypto, hard-coded keys, weak randomness, insecure TLS exceptions, predictable reset tokens, and misuse of encryption without key management.

**Copy/paste prompt:**

```text
Review password, token, key, encryption, randomness, and transport handling against the framework's supported primitives and the application's threat model. Replace plaintext or homemade cryptography with a maintained password KDF and vetted library, protect keys separately, use secure randomness and expiry, and remove TLS verification bypasses. Add tests for storage format, token entropy/expiry, rotation, and failure behavior. Do not invent algorithms or print credentials.
```

### 20. Overbroad API responses, logs, and telemetry

**Look for:** returning entire database rows, GraphQL overexposure, internal IDs, tokens, billing data, prompts, stack traces, analytics payloads, and support exports.

**Copy/paste prompt:**

```text
Compare each API, GraphQL resolver, export, log, trace, analytics event, crash report, and support payload with the minimum fields the caller needs. Replace broad serialization with explicit response schemas and redaction, enforce field-level authorization, remove secrets and sensitive values from URLs, and add tests for unauthorized fields and log scrubbing. Preserve a documented operational identifier where needed without exposing personal data.
```

### 21. Public storage, backup, retention, and deletion failures

**Look for:** public buckets, guessable URLs, unencrypted backups, stale replicas, vendor copies, missing retention jobs, deletion that leaves caches/logs, and policies that promise more than the system does.

**Copy/paste prompt:**

```text
Trace sensitive data across primary storage, object storage, caches, queues, replicas, backups, search indexes, logs, analytics, and vendors. Make access deny-by-default, scope keys to the owner or tenant, protect backups, define retention, and implement the approved deletion or anonymization workflow with status and audit evidence. Add tests for unauthorized retrieval, expired access, deletion propagation, and lawful retention exceptions. Do not claim deletion is complete where the architecture cannot verify it.
```

## Category 6 — Abuse, payments, and webhooks

### 22. Missing rate limits, brute-force controls, and bot protection

**Look for:** unlimited login, signup, reset, AI, upload, search, messaging, coupon, export, or deletion attempts; limits applied only in the browser; one shared limit for unrelated costs.

**Copy/paste prompt:**

```text
Inventory public and authenticated endpoints and design endpoint-specific limits for credential attacks, enumeration, spam, AI spend, uploads, exports, and expensive queries. Enforce limits server-side with appropriate identity/IP/tenant keys, bounded bursts, safe errors, accessible recovery, `Retry-After` where useful, abuse alerts, and tests for concurrency and reset behavior. Do not choose arbitrary thresholds without recording the rationale and owner.
```

### 23. Resource exhaustion and AI-cost abuse

**Look for:** unbounded tokens, image/video duration, recursive jobs, pagination, concurrency, queue depth, retries, timeouts, model selection, or vendor spend.

**Copy/paste prompt:**

```text
Find every path that consumes CPU, memory, storage, queue capacity, model tokens, paid API calls, or worker time. Add server-side bounds, quotas, timeouts, concurrency limits, cancellation, retry caps, circuit breakers, tenant budgets, and a safe degraded response. Add tests for oversized and repeated requests, queue saturation, vendor failure, and cost spikes. Do not silently change paid entitlements or user limits; flag product decisions.
```

### 24. Client-trusted payments and entitlements

**Look for:** client-controlled `isPaid`, credits, plan, price, role, receipt, success query parameter, or unlock flag; access granted before payment is verified.

**Copy/paste prompt:**

```text
Trace checkout, receipt, subscription, refund, chargeback, and entitlement state from the client through the server and payment provider. Make the server authoritative for product IDs, prices, payment status, plan limits, credits, seats, and expiration; verify provider state before granting access and reconcile revocation or refund. Add tests for tampered client values, pending/failed/duplicate payments, retries, refunds, and account deletion. Follow the existing mobile app-store payment rules where applicable.
```

### 25. Unsigned, replayable, or non-idempotent webhooks

**Look for:** webhook endpoints with no signature verification, secrets in client code, trust in event order, duplicate grants, replayable events, and missing failure/retry handling.

**Copy/paste prompt:**

```text
Review every inbound webhook and callback. Verify the provider's current signature scheme over the exact request bytes, validate timestamp and event identity, reject replays, authenticate the intended account, process idempotently, handle out-of-order and duplicate events, and enqueue slow work safely. Add redacted logs and tests for invalid signatures, old timestamps, duplicates, tampering, delayed payment, refund, cancellation, and provider retries. Do not accept a browser redirect as webhook proof.
```

## Category 7 — Dependencies and delivery

### 26. Vulnerable or unnecessary dependencies

**Look for:** unpinned packages, abandoned libraries, transitive vulnerabilities, install scripts, unused SDKs, copied code, and upgrades made without tests or provenance review.

**Copy/paste prompt:**

```text
Inventory direct and transitive dependencies, build tools, SDKs, containers, and install scripts. Run the repository's supported audit tools, remove unused packages, review reachable findings and licenses, pin or otherwise control versions, and propose the smallest safe upgrades with regression tests. Do not blindly upgrade the whole stack or suppress a finding; record false-positive reasoning and remaining exposure.
```

### 27. Insecure CI/CD and build artifacts

**Look for:** overprivileged workflow tokens, untrusted pull-request code with secrets, mutable actions/images, artifact tampering, deploys from unreviewed branches, and secrets printed in logs.

**Copy/paste prompt:**

```text
Audit CI, build, release, deployment, preview, and dependency-update workflows. Apply least-privilege permissions, isolate untrusted code from secrets and production deploys, pin trusted actions/images where practical, protect environments and branches, mask logs, verify artifacts, and add approval or rollback controls proportionate to risk. Do not change production credentials or deploy settings without explicit authorization; report the exact owner action needed.
```

### 28. Unsafe third-party SDKs, OAuth scopes, and external integrations

**Look for:** unused analytics/ad/crash/payment SDKs, broad OAuth scopes, undocumented data destinations, scripts before consent, vendor proxy endpoints, and integrations that bypass authorization or deletion.

**Copy/paste prompt:**

```text
Build an inventory of every SDK, script, OAuth app, API, webhook, embedded service, and vendor destination. Record purpose, fields, identifiers, permissions, region, retention, subprocessors, consent timing, deletion support, security controls, and rollback path. Remove unused integrations, narrow scopes and egress, gate optional tracking where required, and add tests that the vendor receives only approved data. Do not infer consent or vendor compliance from a package name.
```

## Category 8 — Operations and recovery

### 29. Missing monitoring, alerting, and incident response

**Look for:** no alerts for auth abuse, authorization failures, data export/deletion failures, payment/webhook errors, AI spend, dependency risk, or unusual access; telemetry that leaks secrets; no owner or runbook.

**Copy/paste prompt:**

```text
Design a privacy-safe security and reliability signal map for this repository. Add or verify alerts for authentication abuse, authorization denials, error spikes, queue/resource exhaustion, payment/webhook failures, deletion failures, unusual AI spend, and deployment or dependency events. Scrub tokens and personal data, assign owners, link runbooks and rollback actions, and test at least one alert in a non-production environment. Do not claim monitoring prevents incidents or proves uptime.
```

### 30. Untested backups, recovery, rollback, and security regression gates

**Look for:** backups that cannot be restored, no recovery-point/recovery-time decision, no rollback or feature flag, no security regression tests, unpatched releases, and changes shipped without evidence.

**Copy/paste prompt:**

```text
Review release, backup, restore, rollback, patching, and security-regression practices for this repository and deployment. Add an evidence-based gate for authentication, authorization, input validation, secrets, uploads, payment/webhooks, deletion, and dependency checks; document backup protection, restore verification, recovery objectives, rollback ownership, and patch deadlines. Run only safe non-production tests, report what could not be verified, and do not claim disaster recovery until an actual restore or approved exercise proves it.
```

## App-store and legal follow-through

Security hardening is only one release gate. For iOS or Android, read [the mobile app and app-store release checklist](mobile-app-release-checklist.md) for privacy declarations, AI data flows, account deletion, store billing, UGC moderation, trademark/claim review, accessibility, and evidence. The supplied transcript ends before its Apple-approval section; do not invent the missing advice or promise approval.

For the legal and privacy crosswalk, also read [the public-web compliance checklist](web-compliance-checklist.md) and [the production security and monetization baseline](production-security-and-monetization.md).

## Reference sources

- OWASP Application Security Verification Standard: <https://owasp.org/projects/asvs>
- OWASP Top 10: <https://owasp.org/projects/top-ten>
- NIST Secure Software Development Framework: <https://csrc.nist.gov/pubs/sp/800/218/final>
- NIST Cybersecurity Framework: <https://www.nist.gov/cyberframework>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
