# Production security and monetization baseline

Use this reference when a web or mobile product is moving from a prototype to real users, paid access, AI usage, or meaningful revenue. It is a threat-model and vendor-review aid, not a certification, legal opinion, or promise that a named provider is safe by default.

The supplied transcript is a source of review topics. It is not authority for fixed rate limits, “production-grade” claims, tax outcomes, or a specific payment architecture. Record the actual stack, user volume, abuse risk, data, jurisdictions, platform, payment category, and evidence.

## Claim triage

| Advice in the transcript | Required correction before implementation |
| --- | --- |
| “Add rate limiting before it becomes a problem.” | Rate limiting is a baseline control, but limits must match the endpoint, identity model, cost, abuse case, accessibility needs, and legitimate burst behavior. Add quotas, monitoring, graceful errors, and an owner for tuning. |
| “Clerk, Supabase, or Firebase Auth is production-grade out of the box.” | A managed identity service can reduce custom-auth code, but production risk remains in configuration: redirect allowlists, session lifetime, MFA/recovery, email verification, roles, tenant mapping, webhook validation, deletion, provider outages, logs, and vendor terms. Verify the deployed configuration. |
| “RLS or scope permissions lock down the database.” | Use database policy and server-side authorization together where appropriate. Test every read, write, relation, admin path, service-role path, background job, export, and direct-object identifier for cross-tenant access. A policy file alone is not evidence. |
| “Put secrets in a server-side environment variable file.” | Keep secrets out of source control and client bundles; use an approved secret manager or protected runtime configuration, least privilege, rotation, access logging, and redaction. A local `.env` file is not automatically a production secret-management system. |
| “Sentry means users will not be impacted.” | Monitoring detects some failures; it does not prevent them or prove availability. Configure PII/token scrubbing, sampling, retention, alert routing, release health, rollback, on-call ownership, and a test alert. |
| “Polar handles payment, billing, CRM, and global tax so there is no sales tax to worry about.” | Polar markets a Merchant of Record service and states that it handles specified international sales-tax obligations for supported sales. Confirm the current agreement, country/product coverage, transaction classification, fees, customer relationship, refunds/disputes, data processing, and the business's remaining tax, accounting, income, registration, reporting, and contractual duties with qualified advisers. |

## 1. Abuse-resilient endpoint controls

Inventory public and authenticated endpoints, then assign controls based on the threat model:

- login, password reset, MFA, email verification, signup, invitation, and OAuth callback;
- AI prompts, file analysis, image/video generation, search, exports, reports, and other expensive or asynchronous work;
- payment checkout, coupon validation, entitlement changes, refund requests, webhooks, and account deletion;
- uploads, feedback, comments, messaging, notification sends, contact forms, and passwordless links;
- admin, support, data export, vendor proxy, and internal health or debug routes.

For each endpoint, record the limit key(s), window/algorithm, burst allowance, cost budget, response, identity/IP/device treatment, trusted-service exception, retry behavior, alert, and owner. Consider separate limits for anonymous traffic, authenticated users, tenants, API keys, device/session, IP range, and high-cost operations. Avoid relying on IP alone where carrier NAT or shared networks can harm legitimate users.

Implement and test:

- server-side enforcement at every relevant route, job, and provider boundary;
- bounded request body, file, page, batch, timeout, concurrency, and token sizes;
- quotas for AI/model spend and external API calls, with a safe failure mode;
- account-enumeration-resistant responses and recovery throttles;
- exponential backoff and `Retry-After` behavior where appropriate;
- idempotency keys for retried writes, checkout creation, entitlement changes, and webhook processing;
- abuse and bot detection proportionate to risk, with an accessible fallback and privacy review;
- monitoring for spikes, credential stuffing, scraping, spend anomalies, queue growth, and denial-of-service symptoms;
- tests for the allowed, limited, reset, concurrent, proxy, authenticated, and failure cases.

Do not publish exact thresholds as security promises unless they are intentional, tested, and maintained. Do not turn a rate-limit response into a data leak or a permanent denial for a legitimate user.

## 2. Identity and authentication provider review

A managed provider such as Clerk, Supabase Auth, or Firebase Authentication may be an appropriate design choice. Treat it as a dependency, not a security conclusion. Verify:

- issuer, audience, redirect URI, allowed origins, deep links, OAuth scopes, cookie/token storage, and session expiry;
- email verification, MFA/passkeys where risk warrants, recovery, device/session management, logout, token revocation, and account deletion;
- server-side token verification and role/tenant mapping; never trust a client-supplied user ID or role;
- service-role/admin keys, provider webhooks, signing-key rotation, clock skew, replay handling, and failure behavior;
- brute-force, credential-stuffing, bot, enumeration, invitation, and abuse controls;
- provider data locations, subprocessors, retention, training/reuse, DPA/contract, deletion support, incident notices, export, rate limits, price changes, and exit plan;
- observability that excludes passwords, access tokens, recovery links, raw identity documents, and unnecessary personal data.

Test a matrix of unauthenticated, authenticated-own-resource, authenticated-other-resource, tenant-admin, support, service-role, deleted-user, expired-session, and provider-outage cases. Protect the authorization decision at the service boundary even if the UI hides the route.

## 3. Database, tenancy, and authorization

Define the authorization invariant in plain language before writing a policy, for example: “A user can read or change only records belonging to an active tenant membership, except for explicitly reviewed support actions.” Then verify it in every access path.

- Use RLS, scoped queries, service-layer checks, or equivalent controls where appropriate; use defense in depth for sensitive data.
- Deny by default and test cross-tenant IDs, alternate HTTP methods, nested resources, bulk operations, search, exports, files, events, and caches.
- Keep privileged service roles server-side; do not expose them in browser/mobile bundles or untrusted jobs.
- Prevent mass assignment and field tampering with allowlists and server-side ownership checks.
- Separate customer, support, admin, automation, migration, and analytics permissions.
- Record access decisions and administrative actions with privacy-safe audit evidence.
- Re-test policies after schema, SDK, migration, storage, ORM, or role changes.

An RLS policy, ORM filter, or UI condition is not enough if another route, SQL function, storage bucket, background job, export, or provider can bypass it.

## 4. Secrets and runtime configuration

Classify credentials and keep them out of Git history, client bundles, mobile binaries, URLs, logs, crash reports, screenshots, support tickets, and changelogs. Use an approved secret manager or protected runtime configuration with:

- separate development, staging, and production values;
- least-privilege scopes, short-lived credentials where possible, and explicit ownership;
- rotation and revocation procedures tested without an outage;
- CI/CD masking and protected environments;
- access logs, reviewable grants, and break-glass handling;
- secret scanning on commits, dependencies, build artifacts, and release packages;
- an incident path for purge, rotation, session invalidation, vendor notification, and evidence preservation.

Public client keys may identify a client or project, but they do not authorize protected operations. Assume anything shipped to a browser or mobile binary can be inspected.

## 5. Monitoring, alerting, and recovery

Use Sentry or another observability service only after checking what data it receives. Configure:

- release and environment tags without secrets or raw personal content;
- scrubbing for authorization headers, cookies, tokens, prompts, uploads, emails, payment data, and sensitive query values;
- retention, access roles, vendor subprocessors, regional storage, deletion, and export behavior;
- alerts for auth abuse, authorization failures, error-rate spikes, queue/backlog growth, payment/webhook failures, deletion failures, unusual AI spend, and dependency/security events;
- actionable routing, on-call ownership, runbooks, rollback or feature-flag controls, and a test alert;
- dashboards that separate a detected signal from a claim about uptime, safety, or user impact.

Test that alerts fire, contain enough context to act, do not expose secrets, and recover when the vendor or notification channel is unavailable. Monitoring is an operational control; it does not replace preventive authorization, validation, rate limits, backups, or incident response.

## 6. Payment and merchant-of-record review

Before selecting Polar or another vendor, classify the sale and map the flow:

1. Is the product a web purchase, an iOS/Android in-app digital entitlement, a physical good/service, a marketplace/P2P service, a donation, or another category?
2. Which entity is the seller, merchant of record, contracting party, invoice issuer, and support contact in each region?
3. Who owns pricing, taxes, refunds, chargebacks, fraud, subscriptions, renewals, customer data, and entitlement decisions?
4. Which terms, privacy notice, DPA, refund policy, tax documents, invoices, receipts, and store disclosures apply?
5. What happens if the vendor, webhook, payment processor, identity provider, or app store is delayed, wrong, unavailable, or terminated?

### Polar-specific verification points

Polar's official [Merchant of Record page](https://polar.sh/features/merchant-of-record) says Polar acts as reseller for supported sales and handles stated international sales-tax obligations. Treat those statements as vendor claims to verify against the signed agreement and current coverage, not as a universal “no tax duties” result.

Polar's [checkout API documentation](https://polar.sh/docs/api-reference/checkouts/create-session) exposes discount, net, tax, and total amounts and may return a checkout that is not yet paid. Show the actual total and tax treatment to the customer, and do not grant access merely because the browser reached a success URL.

Polar's [order webhook documentation](https://polar.sh/docs/api-reference/webhooks/order.created) warns that an order may still be pending, and the [subscription documentation](https://polar.sh/docs/api-reference/webhooks/subscription.created) says a newly created subscription may not yet be active. Verify webhook authenticity, bind the event to the intended user/product, process it idempotently, and grant or revoke entitlements from server-side payment state.

Polar documents webhook endpoint secrets and event configuration in its [webhook endpoint API](https://polar.sh/docs/api-reference/webhooks/endpoints/get), and documents refund/revocation behavior in its [refund API](https://polar.sh/docs/api-reference/refunds/create). Store webhook secrets server-side, verify signatures according to the current integration documentation, reject replays, log a redacted event ID, and test refunds, disputes, cancellation, past-due, revocation, and vendor retries.

### Monetization release checks

- show total mandatory price, currency, trial conversion, renewal cadence, taxes/fees where applicable, cancellation, refund, and support information before commitment;
- do not hide mandatory charges or make cancellation materially harder than purchase;
- verify paid status server-side before granting access, credits, seats, downloads, or AI quota;
- make entitlements idempotent and recoverable after duplicate, delayed, out-of-order, or missing events;
- reconcile vendor orders, internal access, refunds, chargebacks, cancellations, and deletion requests;
- minimize payment/customer data and update the privacy policy, SDK/vendor inventory, retention map, and deletion process;
- preserve receipts and accounting evidence without putting payment secrets or unnecessary personal data in logs;
- test sandbox and production-like cases for success, pending, failure, duplicate, renewal, upgrade, downgrade, refund, dispute, cancellation, vendor outage, and account deletion;
- document vendor fees, settlement currency, payout timing, supported countries/products, tax/invoice behavior, data processing, support responsibility, portability, and exit plan.

For mobile digital purchases, follow the platform-specific payment analysis in [the mobile app and app-store release checklist](mobile-app-release-checklist.md). A web payment vendor or integration library does not by itself create an app-store exception.

## Evidence packet

| Area | Evidence |
| --- | --- |
| Rate limiting | Endpoint inventory, limit rationale, quota config, abuse tests, alerts, accessibility review |
| Authentication | Provider config, server verification, auth matrix, recovery/MFA/session tests, vendor review |
| Authorization/tenancy | RLS/scoped-policy source, cross-tenant negative tests, privileged-path review, audit events |
| Secrets | Secret inventory, manager/runtime config, scan output, rotation/revocation test, bundle inspection |
| Monitoring | Scrubbing config, retention/roles, alert test, runbook, rollback/owner |
| Monetization | Product classification, vendor contract/coverage, checkout totals, webhook verification, entitlement reconciliation, refund/dispute tests |
| Privacy/legal | Policy/version crosswalk, vendor data map, consent/retention/deletion behavior, counsel decisions |

Mark gaps `not verified` or `needs counsel`; do not replace missing evidence with a vendor logo, a dashboard screenshot, or a statement that the app is “production-grade.”

## Reference sources

- OWASP ASVS: <https://owasp.org/projects/asvs>
- NIST SSDF: <https://csrc.nist.gov/pubs/sp/800/218/final>
- Polar Merchant of Record: <https://polar.sh/features/merchant-of-record>
- Polar checkout API: <https://polar.sh/docs/api-reference/checkouts/create-session>
- Polar order webhooks: <https://polar.sh/docs/api-reference/webhooks/order.created>
- Polar subscription webhooks: <https://polar.sh/docs/api-reference/webhooks/subscription.created>
- Polar webhook endpoints: <https://polar.sh/docs/api-reference/webhooks/endpoints/get>
- Polar refunds: <https://polar.sh/docs/api-reference/refunds/create>
