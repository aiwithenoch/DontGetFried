---
name: legal-web-security
description: Analyze a user's actual web or connected mobile application, repository, runtime, data flows, dependencies, and deployment context before creating fact-matched legal, privacy, compliance, or security work; use templates only as structures and surface counsel and security-review boundaries.
---

# Legal & Web Security

Use this skill for web-product work where legal obligations and technical controls affect each other: privacy notices, cookie/tracking flows, authentication, payments, data processing, vendor integrations, user-generated content, security features, incident preparation, or a review of an existing web application.

The goal is a traceable, context-specific engineering result. Connect each important legal or contractual assumption to the user's actual implementation, data flow, vendor, document, test, or open question. Do not turn uncertainty into a confident legal conclusion or generic policy text.

## Context-first operating contract

This is the skill's default mode, not an optional audit flavor. Before selecting a template, writing a policy, proposing a security fix, or making a release claim, read [the context-first operating model](references/context-first-operating-model.md) and inspect the actual target.

- Analyze the real repository first: instructions, changelog, manifests, lockfiles, entrypoints, routes, server/API handlers, auth/session code, authorization and database policies, schemas/migrations, storage, jobs, webhooks, emails, deletion, vendors/SDKs, deployment, tests, and public claims.
- If an explicitly authorized staging app, API, browser session, or test environment is available, walk the relevant user journey and compare runtime behavior with the code. Use synthetic data and low-volume checks only. If it is not available, label runtime behavior `not verified`; do not pretend the repository proves it.
- Build an evidence ledger with `observed`, `provided`, `assumed`, `unknown`, `needs counsel`, and `not verified` statuses before generating output.
- Select only the references that match the observed product surface. Treat the legal templates as structures and drafting starting points, never as facts about the user's app.
- Every generated paragraph, finding, patch, test, and prompt must connect to an actual file, route, schema, SDK, vendor, config, user journey, runtime observation, or visible open question. Generic output is a failure mode to remove before handoff.
- If the target cannot be inspected, produce an evidence-gap report or clearly marked non-production outline—not a publishable privacy policy, terms, cookie notice, or claim that the app is secure or compliant.

## Ghana-first and Africa-aware jurisdiction mode

When Ghana, Africa, ECOWAS, African users, mobile money, Ghanaian business operations, or a Ghana/Africa launch is mentioned, read [the Ghana-first and Africa-aware compliance router](references/ghana-africa-compliance-router.md) before drafting or changing an artifact. It makes Ghana Act 843/Act 772/Act 1038, DPC/CSA/NCA/BoG/GRA/ORC routing, child-safety and transfer questions, and Ghana-relevant security risks first-class checks.

Never treat “Africa” as a jurisdiction or claim pan-African compliance. Build a country matrix for every actual target, data-subject location, entity, processor, hosting region, payment rail, and sector. Separate statute, regulator guidance, policy framework, consultation, draft bill, platform rule, vendor statement, and engineering recommendation. If a Ghana-specific fact or country law is unknown, keep it visible as `unknown`, `not verified`, or `needs counsel`; do not fill it with a U.S., EU, or generic African assumption.

## Non-negotiable boundaries

- This skill is an engineering and issue-spotting aid, not a lawyer, law firm, compliance certification, or substitute for licensed counsel. Never state that a product, policy, contract, or implementation is legally compliant unless the user supplies an authoritative determination and the statement is accurately scoped.
- Separate `provided`, `verified`, `assumed`, and `open` facts. Do not invent jurisdictions, legal bases, retention periods, consent requirements, data categories, vendor behavior, or security assurances.
- Treat the templates in this repository as drafting starting points. They are not a current-law database and do not automatically fit a user's facts. Preserve visible placeholders until the user supplies the value and flag material changes for counsel.
- Do not request, print, commit, or place secrets, credentials, raw personal data, production tokens, or incident evidence in source files, logs, prompts, or the changelog. Use redacted examples and secret-manager references.
- Do not weaken a security control, bypass an approval, send a notice, submit a filing, change production, or push to an external system unless that action is explicitly in scope and authorized.
- Do not claim that OWASP Top 10, ASVS, NIST, or any other framework by itself proves safety, compliance, or absence of vulnerabilities. Name the exact version and the evidence actually checked.

## Start with context, then ask only for missing facts

Before changing code or drafting a legal artifact, follow the context-first model. Inspect the target before asking a generic questionnaire. Then establish the smallest remaining fact set:

1. Product surface, repository, stack, deployment model, distribution targets (web, iOS, Android, App Store, Google Play), and the specific user journey or endpoint in scope.
2. Countries/states where the business, users, employees, and service providers are located or targeted. Treat jurisdiction as a counsel-confirmed input, not an inference from a domain name.
3. Data categories, including whether the flow involves children, health, biometric, precise location, financial/payment, credentials, employment, or other sensitive information.
4. Purpose, collection point, access roles, sharing/subprocessors, transfers, retention, deletion, backups, and user rights workflows.
5. Authentication, authorization, tenancy, admin/support access, payments, uploads, integrations, and user-generated content.
6. Required artifacts or commitments: privacy policy, cookie policy/notice, terms of service/use, refund or cancellation policy, DPA, BAA, NDA, MSA, security addendum, customer promise, or internal control.
7. Launch deadline, acceptable residual risk, existing tests/evidence, and who must approve legal or security decisions.

If a fact is missing, continue only with a clearly labeled assumption for low-risk scaffolding and list the exact evidence or owner decision needed. Pause consequential behavior—such as collecting sensitive data, sharing it with a vendor, making a significant automated decision, publishing a legal artifact, or representing a security promise—until the relevant fact is confirmed.

## Public-web launch baseline

For a public website, checkout, marketing flow, email program, or user-facing form, read [the web-compliance checklist](references/web-compliance-checklist.md). It turns the user's requested baseline into verifiable work items:

- publish fact-matched privacy, terms of service/use, refund/cancellation, and cookie-policy/notice content where applicable;
- make cookie choices and form consents specific, accessible, revocable, and consistent with the actual data flows;
- collect only necessary data, audit third-party SDKs and vendors, provide a deletion-request path, and apply age/children safeguards when relevant;
- remove dark patterns, hidden or late mandatory fees, fake reviews, and unsupported product or security claims;
- provide business identity/contact details, accessible text alternatives, sufficient contrast, logical keyboard operation, licensed fonts/images, and unsubscribe controls for commercial email.

Mark each item `verified`, `not verified`, `not applicable — reason`, or `needs counsel`. Do not treat a missing application as permission to write fictional implementation evidence.

## Mobile app and store-release baseline

When the product ships through Apple or Google Play, read [the mobile app and app-store release checklist](references/mobile-app-release-checklist.md). It adds platform-specific issue spotting for App Privacy Details, Google Play Data safety, AI data flows, account deletion, digital purchases, user-generated content, DMCA process, trademark clearance, feedback boards, store-review evidence, and mobile security controls.

Do not convert social-media advice into a universal legal rule. In particular, do not promise that an AI disclosure, arbitration clause, DMCA agent, anonymization shortcut, billing integration, or monitoring product guarantees immunity or store approval. Separate platform policy, applicable law, product choice, and counsel decisions; record the exact source and build evidence for each store answer.

## Production security and monetization baseline

When the request involves real users, rate limits, managed authentication, database tenancy, secrets, monitoring, AI spend, checkout, subscriptions, or a payment/merchant-of-record vendor, read [the production security and monetization baseline](references/production-security-and-monetization.md). It requires endpoint-specific abuse controls, server-side authorization, provider configuration review, secret isolation, privacy-safe observability, payment-state verification, webhook hardening, entitlement reconciliation, and vendor/tax/contract escalation.

Treat examples such as Clerk, Supabase, Firebase Auth, Sentry, or Polar as candidate dependencies, not proof of security, tax coverage, store eligibility, or legal compliance. Verify the deployed configuration, current vendor terms and coverage, data processing, failure modes, and the user's actual jurisdiction and product category.

## Vibe-coded app security cheat sheet

When the request is an all-in-one security pass for a fast-built app, read [the defensive security cheat sheet](references/vibe-coded-app-security-cheatsheet.md). It provides 30 review targets across eight categories and standalone prompts for an AI coding assistant. Use the prompts as controlled review instructions: inspect the real repository first, make minimal server-side fixes, add negative tests, preserve secrets and data, and report what remains unverified.

Never promise that an app is 100% hack-proof or that a checklist guarantees App Store approval. Route Apple/Google requirements to the mobile checklist and use the exact architecture, provider configuration, deployment, and data-flow evidence available.

## Launch preflight and store rejection

When the request is a go-live gate, includes authentication/rate limiting/roles/server validation, mentions destructive database operations, or reports an Apple review rejection, read [the launch preflight and store-rejection workflow](references/launch-preflight-and-store-rejection.md). Never execute or recommend a one-line production database wipe. For a store rejection, require the actual Resolution Center finding, guideline reference, build, reproduction steps, and evidence before selecting a fix or appeal.

When the user asks for a quick secure-launch score or a fixed number of checks, read [the secure-launch scorecard](references/secure-launch-scorecard.md). Treat its ten items as evidence-backed triage, not a magic threshold or a claim that the app is secure.

When the request calls for browser DevTools, front-end bundle/storage inspection, XSS/upload/payment-webhook checks, or CDN/WAF/DDoS review, read [the authorized browser and edge audit](references/browser-and-edge-audit.md). Use only owned or explicitly authorized test environments, synthetic data, redacted evidence, and low-volume probes.

When the request is a pre-production release gate for paperwork, cookie or analytics consent, session replay, authentication versus authorization, database policies, or RLS, read [the production paperwork, consent, and database authorization gate](references/production-release-gate.md). Treat vendor defaults, fixed penalty claims, and RLS assurances as facts to verify—not universal rules. Require a facts-to-document crosswalk, consent-state evidence, server-side authorization tests, and counsel/security-owner escalation for unresolved decisions.

When the request involves Ghana/Africa jurisdiction, local consumer disclosures/refunds, Ghana data-protection registration, local incident/marketing/payment rules, children, cross-border vendors, or a multi-country African launch, read [the Ghana-first and Africa-aware compliance router](references/ghana-africa-compliance-router.md). It is a country-routing and evidence reference, not a legal conclusion.

## Route the work

Choose the smallest mode that fits the request:

- **Build or modify:** translate the intake into controls, implement secure defaults, update the affected user-facing disclosure or contract artifact, and add verification evidence.
- **Review or audit:** model assets, actors, trust boundaries, abuse cases, and data flows; report source-backed findings with severity, exploitability, affected behavior, and remediation. Do not call an issue a legal violation or a security certification gap without the required authority and evidence.
- **Draft or update an artifact:** read [the template map](references/legal-template-map.md), select a candidate template, preserve `<mark>` customization fields, state assumptions, and identify clauses that need counsel or business-owner decisions.
- **Incident or urgent risk:** preserve evidence safely, contain only within the authorized scope, avoid destructive cleanup, record uncertainty, and escalate legal, privacy, security, and communications decisions to the responsible humans.

## Core workflow

### 1. Build a requirement map

Create a compact matrix before implementation when more than one requirement is involved:

| Requirement or promise | Source and version | Code/config/document location | Evidence or test | Status/owner |
| --- | --- | --- | --- | --- |

Use source labels such as `user-provided`, `repository template`, `contract`, `counsel`, `OWASP ASVS vX.Y.Z`, or `NIST SP 800-218`. Keep legal interpretation, product choice, and technical implementation as separate rows when they are not the same decision.

### 2. Map the legal artifact to real behavior

For every policy or contract statement, check the implementation rather than copying prose blindly:

- What data is actually collected, inferred, stored, disclosed, transferred, or deleted?
- Which UI, API, job, vendor, cookie, SDK, or log creates that behavior?
- What user choice, notice, access/deletion path, retention rule, or contractual restriction is promised?
- What evidence shows the promise is true, and what would make it false?

If the document and the product disagree, flag the mismatch. Do not silently make the product collect less or the document promise more without recording the decision.

### 3. Threat-model the web change

At minimum, identify:

- assets and sensitive data;
- users, administrators, support staff, vendors, and attackers;
- trust boundaries and data flows;
- authentication, authorization, tenant-isolation, and recovery assumptions;
- abuse cases such as account takeover, privilege escalation, injection, data exfiltration, scraping, fraud, spam, unsafe uploads, and denial of service;
- detection, response, deletion, backup, and evidence-retention needs.

Read [the secure-web baseline](references/secure-web-baseline.md) for the control families and evidence expectations. Use the narrowest scope that answers the user's question, but follow a risk into adjacent code when the changed behavior depends on it.

### 4. Implement secure, privacy-aware defaults

Prefer controls enforced at the server or service boundary, not only in browser code or policy text. Typical expectations include server-side authorization on every protected operation, deny-by-default access, tenant scoping, parameterized data access, context-appropriate output encoding, CSRF protection where applicable, safe file handling, strict input validation, bounded resource use, secure session/cookie settings, secret isolation, redacted logs, dependency review, and tested error handling. For public-facing work, verify that the consent banner, forms, deletion path, email preferences, price disclosures, and accessibility behavior are implemented—not merely linked from a policy.

Minimize collection and retention. Avoid putting personal or sensitive values in URLs, analytics events, exception messages, debug logs, screenshots, or test fixtures. Make tracking and consent behavior match the actual SDK calls and regional rules supplied by the user or counsel; do not assume that a banner alone resolves the legal analysis.

### 5. Verify and report honestly

Run the relevant tests, static checks, dependency checks, and manual probes that are available in the repository. Record exact commands and results. For each finding or unresolved risk, include:

- affected file, route, component, or user flow;
- source-backed explanation and realistic attack or failure path;
- severity and confidence, with the reason;
- remediation or decision needed;
- verification performed and remaining coverage gaps.

Use `verified`, `not verified`, `assumed`, and `needs counsel` labels. A passing test proves only the behavior it covers.

## Required handoff shape

Return a concise record containing:

1. scope and objective;
2. facts, assumptions, and jurisdiction/data gaps;
3. legal or contractual artifacts considered, with repository paths;
4. security risks, controls, and residual risk;
5. files changed and verification results;
6. open questions and explicit counsel/security-owner escalations;
7. a statement of what was not established (for example, no legal opinion, no certification, or incomplete production evidence).

For implementation work, leave the context snapshot, evidence ledger, requirement map, and unresolved questions close to the code or in the project handoff so a later reviewer can reproduce the reasoning. Keep the repository's lowercase `changelog.md` append-only and record material decisions, failed checks, and next steps there.

## References

- Read [legal-template-map.md](references/legal-template-map.md) when selecting or updating a contract, notice, or policy template.
- Read [context-first-operating-model.md](references/context-first-operating-model.md) before every legal, privacy, compliance, or security artifact, review, fix, or release decision.
- Read [web-compliance-checklist.md](references/web-compliance-checklist.md) for the public-web release baseline.
- Read [mobile-app-release-checklist.md](references/mobile-app-release-checklist.md) for iOS, Android, AI, app-store, UGC, payment, deletion, and mobile-security release checks.
- Read [production-security-and-monetization.md](references/production-security-and-monetization.md) for rate limits, identity providers, tenancy, secrets, monitoring, payments, Polar/vendor review, webhooks, and entitlement evidence.
- Read [ghana-africa-compliance-router.md](references/ghana-africa-compliance-router.md) when Ghana, Africa, ECOWAS, African users/vendors, mobile money, local SMS/USSD, Ghana entity/payment/tax questions, or multi-country African compliance is in scope.
- Read [vibe-coded-app-security-cheatsheet.md](references/vibe-coded-app-security-cheatsheet.md) for 30 defensive security targets and copy/paste remediation prompts across eight categories.
- Read [launch-preflight-and-store-rejection.md](references/launch-preflight-and-store-rejection.md) for the four launch security gates, destructive-operation safeguards, and evidence-based Apple rejection handling.
- Read [secure-launch-scorecard.md](references/secure-launch-scorecard.md) for the ten-control secure-launch scorecard and audit prompt.
- Read [browser-and-edge-audit.md](references/browser-and-edge-audit.md) for authorized DevTools, bundle/storage, XSS, uploads, webhooks, rate-limit, and edge-protection checks.
- Read [production-release-gate.md](references/production-release-gate.md) for paperwork, consent-aware analytics/session replay, authentication versus authorization, database/RLS, evidence, and combined pre-production prompts.
- Read [refund-policy-outline.md](references/refund-policy-outline.md) when a paid product, subscription, order, or cancellation flow needs a refund artifact and no approved policy exists.
- Read [secure-web-baseline.md](references/secure-web-baseline.md) for security-control families, testing evidence, and framework versioning.
