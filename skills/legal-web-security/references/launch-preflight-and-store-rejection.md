# Launch preflight and App Store rejection workflow

Use this reference immediately before a web or mobile app goes live, or when a store submission has been rejected. It is a defensive engineering workflow, not a security certification, legal opinion, or guarantee of approval.

The four minimum checks are authentication, rate limiting, authorization/role enforcement, and server-side input validation. They are necessary but not sufficient: secrets, sessions, uploads, dependencies, payments, privacy, deletion, monitoring, backups, and incident response still need review.

For a broader ten-control score, use the [secure-launch scorecard](secure-launch-scorecard.md). Do not convert its result into a universal pass/fail threshold.

## Destructive database safety

Never execute or recommend a one-line production database wipe. A destructive command can remove customer records, audit evidence, entitlements, backups, or the ability to recover. Do not place a destructive wipe in an application route, startup script, migration that runs automatically, CI job, AI-builder prompt, or copy/paste snippet.

Before any authorized destructive operation:

1. identify the exact environment, account, host, database, tenant scope, and data owner;
2. stop and require explicit authorization from the responsible owner;
3. take an encrypted, access-controlled backup and prove that a restore works in an isolated environment;
4. prefer a reversible, scoped migration or soft-delete plan with a dry run and affected-record count;
5. add an environment guard that refuses production unless an approved break-glass path is used;
6. use transactions, bounded batches, timeouts, locks, and a tested rollback where the datastore supports them;
7. record the change, approver, backup, result, and residual risk without recording secrets or raw personal data;
8. verify application behavior, access revocation, retention/deletion promises, search indexes, caches, queues, replicas, and vendor copies afterward.

**Copy/paste prompt:**

```text
Audit this repository for destructive database, storage, migration, seed, cleanup, reset, and deployment operations. Do not execute any destructive command and do not print a command that would wipe production. Add safe environment guards, dry-run and scoped-operation support, backup/restore evidence requirements, bounded batches, authorization checks, and tests that prove production is refused by default. Preserve existing data and report any operation that still requires explicit owner approval.
```

## Four launch security gates

For each gate, record `verified`, `not verified`, `not applicable — reason`, `assumed`, or `needs counsel`, with the build, route, test, reviewer, and date.

### 1. Authentication

Authentication proves the request is associated with an identity; it does not by itself prove that the identity may access a resource. Review APIs, server actions, background jobs, file routes, WebSockets/RPC, exports, and recovery paths—not only visible screens.

Verify:

- every protected operation enforces identity at the server/service boundary;
- public routes are intentionally listed and do not expose protected data;
- sessions/tokens have appropriate expiry, rotation, revocation, storage, and logout behavior;
- password reset, email verification, MFA, OAuth, magic links, and deletion invalidate or scope credentials correctly;
- provider/admin/service keys are not shipped to clients or accepted as user identity;
- anonymous and authenticated negative tests exist for every protected route.

**Copy/paste prompt:**

```text
Perform an authentication preflight on this repository. Inventory every route, server action, job, file endpoint, WebSocket/RPC method, export, and recovery flow; classify it as intentionally public or protected; then trace the server-side identity check. Add the smallest deny-by-default fix for unprotected operations, preserve the existing identity provider, and add anonymous/authenticated/expired/revoked-session tests. Do not invent users, credentials, or provider behavior, and report every route that remains unverified.
```

### 2. Rate limiting and abuse controls

Rate limiting must be applied to the actual abuse and cost boundary, not just the login screen. Consider login, signup, recovery, MFA, AI, uploads, search, exports, messaging, passwordless links, checkout, coupons, deletion, and webhooks.

Verify:

- limits are enforced server-side and cannot be bypassed by changing the client or route;
- keys and thresholds reflect the endpoint's risk and cost: identity, tenant, IP, device/session, API key, or a combination;
- limits include burst handling, concurrency, queue/AI budgets, timeouts, retry behavior, and a safe accessible recovery path;
- responses do not disclose account existence or sensitive state;
- monitoring detects credential stuffing, scraping, spam, spend spikes, and distributed abuse;
- allow/deny/concurrent/reset cases have tests and an owner for tuning.

**Copy/paste prompt:**

```text
Perform a rate-limit and abuse-control preflight on this repository. Inventory public and authenticated endpoints, identify brute-force, spam, scraping, denial-of-service, and cost-abuse paths, and add endpoint-specific server-side limits with safe errors, bounded bursts, retry behavior, quotas, and alerts. Cover login, recovery, AI, uploads, exports, messaging, checkout, and deletion where present. Add non-production tests for allowed, limited, concurrent, reset, and distributed-client cases. Do not choose arbitrary thresholds or block legitimate users without documenting the rationale and owner.
```

### 3. Authorization and role-based security

Authorization decides what an authenticated identity can do. Use resource ownership, tenant membership, role, action, and state—not just a `userId` from the request or a hidden UI button.

Verify:

- every read, write, delete, download, export, search, and nested-resource operation checks the acting identity and resource scope;
- roles and permissions are allowlisted and enforced server-side;
- client input cannot change owner, tenant, role, plan, verification, status, or entitlement fields;
- admin, support, automation, service-role, and background-job access is separately scoped and audited;
- cross-user, cross-tenant, horizontal, vertical, guessed-ID, and deleted-user tests fail closed;
- database RLS or equivalent policy is tested together with service-layer authorization, storage, caches, and exports.

For the concrete two-account URL/request replay, use the [authorized manual replay test in the security cheat sheet](vibe-coded-app-security-cheatsheet.md#authorized-manual-replay-test). Run it only with synthetic data in an owned or explicitly authorized environment; a failed replay shows an access-control defect but does not by itself identify the missing implementation technology.

**Copy/paste prompt:**

```text
Perform an authorization and role-security preflight on this repository. Build a matrix of identities, tenants, roles, resources, actions, and states; trace every read/write/delete/download/export path to the server-side decision; and test same-user, other-user, other-tenant, admin, support, service-role, guessed-ID, and deleted-account cases. Enforce deny-by-default ownership and role checks, explicit field allowlists, and safe database/storage scoping. Do not trust UI visibility or client-supplied roles, and report ambiguous business rules instead of guessing.
```

### 4. Server-side validation

Client-side validation improves usability but cannot protect an API. Validate type, shape, length, encoding, ranges, allowed values, file content, state transitions, and business rules again at the server boundary.

Verify:

- all request bodies, query parameters, headers, path IDs, files, imports, webhooks, and background messages are validated;
- database, shell, template, HTML, URL, file, and model contexts use the correct parameterization or encoding;
- unknown fields are rejected or ignored intentionally, and protected fields cannot be mass-assigned;
- resource and cost bounds prevent oversized payloads, recursive work, expensive queries, and unbounded AI calls;
- invalid input returns safe, accessible errors without echoing secrets or personal data;
- validation tests cover malformed, hostile, boundary, duplicate, replayed, and cross-tenant input.

**Copy/paste prompt:**

```text
Perform a server-side validation preflight on this repository. Trace every client, webhook, import, file, background-job, and provider value into persistence, queries, commands, templates, HTML, URLs, files, and AI/model calls. Add explicit schemas, type/size/range/encoding/business-rule checks, unknown-field handling, parameterization, context-specific output encoding, and resource bounds at the server boundary. Add negative tests for malformed, oversized, hostile, duplicate, replayed, and cross-tenant input. Do not rely on browser validation or a generic sanitizer.
```

## Apple App Store rejection workflow

“Apple rejected my app” is not enough information to choose a fix. Do not guess the reason, delete data, hide a feature, falsify metadata, bypass a payment rule, or submit a different behavior merely to pass review.

### 1. Preserve the actual finding

Capture the App Store Connect/App Review Resolution Center message, guideline number and quoted issue, affected build/version, metadata or region, review steps, test account state, screenshots, and the date. Redact credentials and personal data. If the message is ambiguous, ask Apple for clarification rather than inferring a legal or security defect.

### 2. Classify the issue against evidence

Map the cited finding to the actual build and configuration. Common areas include:

- privacy policy, App Privacy Details, data collection, tracking, AI/vendor disclosure, or consent;
- account creation and in-app/web account deletion;
- digital purchases, subscriptions, restore/cancel/refund behavior, or external payment claims;
- user-generated content filtering, reporting, blocking, moderation, or contact information;
- crashes, broken links, incomplete functionality, login/test-account failure, or inaccessible flows;
- misleading metadata, unsupported claims, trademark/brand issues, or missing business/support details;
- security, safety, age/child, regulated-use, or high-impact feature concerns.

Use the current [Apple App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) and the relevant official Apple documentation. Use [the mobile app and app-store release checklist](mobile-app-release-checklist.md) to cross-check privacy, deletion, billing, UGC, AI, accessibility, and evidence. Do not treat a social-media post or a vendor's “approval” claim as an Apple rule.

### 3. Fix the real behavior

For each cited issue, create a row with the guideline/source, observed behavior, code/config/metadata location, fix, owner, test, build number, and status. Make the smallest honest fix. Keep the privacy policy, store declarations, app behavior, server behavior, SDK inventory, and test notes synchronized.

Do not:

- obfuscate or null data merely to make account deletion appear complete;
- hide an AI provider, analytics SDK, tracking call, subscription, mandatory fee, or UGC feature from review;
- route a covered digital purchase through an unapproved web workaround;
- remove report/block/moderation controls or accessibility behavior to reduce visible scope;
- claim encryption, privacy, safety, compliance, human review, or performance that the implementation cannot prove.

### 4. Re-test from the reviewer path

Use a clean device or simulator, supported OS, correct region, fresh account, test account, and production-like backend. Verify the exact steps in the rejection, cold start, offline/poor network behavior, login/recovery, privacy choices, deletion, purchases and restoration, UGC reports, accessibility, error handling, and any reviewer notes. Attach a short reproducible test script and safe demo credentials through the store's approved channel—not in the repository or chat.

### 5. Reply or appeal factually

Respond point-by-point with the guideline reference, what changed, where it can be tested, build/version, demo account instructions, screenshots or recordings where appropriate, and any remaining limitation. If the disagreement concerns legal interpretation, regulated data, contracts, consumer rights, or a material business claim, escalate to qualified counsel or the responsible policy owner. There is no checklist that guarantees approval.

## Release evidence matrix

| Gate | Minimum evidence | Status/owner |
| --- | --- | --- |
| Authentication | Protected-route inventory, identity-provider config, anonymous/expired/revoked tests |  |
| Rate limiting | Endpoint limits, abuse cases, quota/alert evidence, accessible recovery test |  |
| Authorization | Role/tenant matrix, cross-user and cross-tenant negative tests, RLS/storage review |  |
| Server validation | Input schema map, hostile/boundary tests, output/query/file checks |  |
| Destructive operations | Environment guard, backup/restore proof, dry-run/rollback evidence, approver |  |
| Apple rejection | Resolution Center citation, reproduction steps, changed build, point-by-point response |  |
| Store/legal alignment | Policy/declaration crosswalk, deletion/payment/UGC/privacy evidence, counsel decisions |  |

## Reference sources

- Apple App Review Guidelines: <https://developer.apple.com/app-store/review/guidelines/>
- Apple App Privacy Details: <https://developer.apple.com/app-store/app-privacy-details/>
- Apple account deletion: <https://developer.apple.com/support/offering-account-deletion-in-your-app/>
- Apple In-App Purchase configuration: <https://developer.apple.com/help/app-review/before-submitting-for-review/configure-in-app-purchases/>
- OWASP ASVS: <https://owasp.org/projects/asvs>
- OWASP Cheat Sheet Series: <https://cheatsheetseries.owasp.org/>
- NIST SSDF: <https://csrc.nist.gov/pubs/sp/800/218/final>
