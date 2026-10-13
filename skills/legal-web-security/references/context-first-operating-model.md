# Context-first operating model

This is the default execution contract for every use of the `legal-web-security` skill. Analyze the actual application before selecting a template, drafting a policy, proposing a security fix, or making a release claim. Do not generate generic terms, privacy text, cookie language, or security advice merely because the user named an artifact.

The output must be grounded in evidence from the target repository and, when explicitly authorized, the target's staging/runtime/API behavior. If the target cannot be inspected, produce an evidence-gap report and a clearly marked non-production outline only when useful; do not present a generic document as ready to publish.

This model is an engineering workflow, not legal advice, a security certification, or permission to access a live system. Follow the skill's boundaries, the repository's `AGENTS.md`, the user's scope, and the applicable tool permissions.

## Operating contract

For every request:

1. Identify the actual target, requested outcome, allowed changes, and authorized inspection surface.
2. Inspect the target's real code, configuration, dependencies, data flows, user journeys, and deployment assumptions before relying on any template or checklist.
3. Build an evidence ledger that separates observed facts from user-provided facts, assumptions, unknowns, and counsel decisions.
4. Select only the repository references that match the observed product surface. Use templates as structures, never as facts.
5. Create or modify only what the evidence supports. Tie every policy statement, security finding, and proposed fix to a route, component, schema, vendor, configuration, document, test, or explicit open question.
6. Verify the resulting behavior and the document-to-product match. Report what was not inspected, not tested, or not established.

“Based on context” means the result should be capable of being disproved by the target evidence. A paragraph that could be pasted unchanged into an unrelated app is a review signal: either replace it with observed product facts or label it as an unresolved placeholder.

## Phase 0 — scope and authorization

Before inspection, record:

- repository/worktree and branch, project type, target app or service, and requested files or user journey;
- whether the request is analysis, drafting, implementation, testing, deployment preparation, or an external publication;
- whether an app URL, API, browser session, test account, logs, vendor console, or deployment configuration is actually available;
- which environment is authorized: local, test, staging, or production; default to local or staging;
- allowed mutations, data restrictions, time or cost limits, and legal/security/business owners;
- external systems that are explicitly in scope and those that are not.

Do not infer authorization from a URL, a public repository, a browser tab, a public API key, or the fact that a user wants an audit. Do not ask for production passwords, private tokens, real customer records, or payment data. If runtime access is needed but not authorized, continue with repository analysis and list the exact runtime evidence gap.

## Phase 1 — repository and runtime discovery

Inspect in this order, adapting to the stack:

1. Read applicable `AGENTS.md` instructions, the project README, the lowercase `changelog.md`, and any explicit project design or deployment notes.
2. Establish the repository shape from manifests and lockfiles: language, framework, client/server split, package manager, build scripts, test commands, database/provider, hosting, mobile targets, and generated-code boundaries.
3. If a `.codegraph/` directory exists and CodeGraph is available, query it before broad grep or file crawling. Ask for the relevant symbols, routes, data paths, and call paths. If it does not exist, use `rg --files` and targeted search; do not initialize a graph unless the project owner requests it.
4. Locate application entrypoints, routes, server actions/API handlers, middleware, authentication/session code, authorization/policy code, database schema/migrations, storage rules, queues/jobs, webhooks, admin/support paths, exports, deletion flows, emails, and error/reporting paths.
5. Inventory dependencies and third-party SDKs from manifests, lockfiles, imports, build plugins, tag managers, native modules, server integrations, and deployment configuration. Trace what data each integration can receive and where it sends it.
6. Follow the requested user journey end to end: UI or client input → request/API → server decision → database/storage/vendor → response, job, email, log, analytics, cache, backup, and deletion path. Read adjacent code when the promise depends on it.
7. Inspect environment examples and configuration without exposing secret values. Record variable names and whether a value is client-visible, server-only, build-time, runtime, or unknown.
8. If explicit authorized staging/API access exists, use synthetic accounts and low-volume requests to confirm the repository findings. Walk through relevant flows and inspect redacted responses, cookies, storage, network destinations, and safe error behavior. Do not stress, fuzz, bypass, or alter a live system.

Do not read the entire repository indiscriminately. Start from the requested flow and follow its dependencies. Expand only when a control, disclosure, or risk crosses a boundary.

## Phase 2 — evidence ledger and context map

Create a working ledger before drafting or editing:

| Fact or question | Evidence | Status | Why it changes the work | Owner/next check |
| --- | --- | --- | --- | --- |
| Actual data collected | file, route, schema, event, or observed request | verified / provided / assumed / unknown | changes policy, minimization, consent, retention |  |
| User and tenant model | auth middleware, roles, RLS/storage policy, tests |  | changes authorization and terms |  |
| Vendor or SDK behavior | manifest/config/docs/request trace |  | changes disclosure, DPA, consent, risk |  |
| Payment and pricing behavior | checkout, webhook, entitlement, receipt, refund code |  | changes terms/refund/fee claims |  |
| Deletion and retention | route/job/vendor API/backup policy |  | changes rights language and release evidence |  |
| Jurisdiction and audience | user-provided fact or counsel source |  | changes legal analysis |  |

Use these labels consistently:

- `observed` — supported by inspected code, configuration, test output, or authorized runtime evidence;
- `provided` — supplied by the user or an authoritative project owner but not independently checked;
- `assumed` — a temporary low-risk working assumption, never a published fact;
- `unknown` — not enough evidence to decide;
- `needs counsel` — a legal interpretation, jurisdiction, contract, consumer-rights, or policy decision that requires the responsible professional;
- `not verified` — a claim or control was expected but the available evidence did not prove it.

Do not turn `assumed`, `unknown`, or `not verified` into confident prose. A missing route, schema, vendor setting, test, or business detail is a finding or open question, not permission to invent one.

## Phase 3 — choose context-specific work

Select references after the context map, not before it:

- use the web checklist only when the app actually has public forms, cookies, marketing, email, checkout, or user-facing accessibility behavior;
- use the mobile checklist only when the target ships through Apple or Google Play or has mobile-specific data flows;
- use the production release gate when the observed app has paperwork, optional tracking/replay, authz/RLS, or release evidence to verify;
- use the security cheat sheet or launch preflight for the actual attack surface found, not as a substitute for inspection;
- use the template map only after actual data, services, users, payments, content, and jurisdictions are recorded.

If several references apply, load the smallest set that covers the observed paths. Do not overwhelm a narrow bug fix with every checklist, and do not treat a checklist item as present merely because its heading exists.

## Policy and legal-artifact generation rules

When the user asks for a privacy policy, terms, cookie notice, refund policy, DPA, or similar artifact:

1. Build a product-specific fact table first.
2. Trace statements to actual behavior: data fields, forms, routes, storage, SDKs, vendors, cookies, emails, payments, AI calls, uploads, user content, retention, deletion, and support access.
3. Use the relevant repository template only for structure and clause candidates. Preserve `<mark>` fields and replace them only with confirmed facts.
4. Identify jurisdiction, controller/processor, children, sensitive data, transfer, consumer-rights, arbitration, warranty, tax, refund, and business-contact decisions that are missing or need counsel.
5. Remove statements for features the app does not have. Do not claim “we do not sell,” “we delete,” “we never share,” “we are compliant,” or a particular retention period unless the evidence supports the exact wording.
6. Reconcile the final draft against the implementation and produce a mismatch list. A document is not ready for publication if it describes a generic app, contains material placeholders, or conflicts with observed behavior.

Minimum product-specific checks for a privacy or cookie artifact include actual data categories and sources, collection points, purposes, identifiers, SDK/vendor destinations, cookies/storage, AI processing, sharing and regions, retention/deletion, rights route, security description, contact details, and consent/withdrawal behavior. “We may collect information” is not an inventory.

## Security analysis and implementation rules

When the user asks to secure, audit, or fix the app:

- cite the actual file, route, component, query, policy, dependency, environment setting, or runtime request;
- trace the full path from untrusted input or identity to the decision, storage, vendor, response, log, and recovery behavior;
- distinguish authentication, authorization, validation, tenancy, database policy, storage access, and provider configuration;
- make the smallest safe server-side change that fits the current architecture; do not replace providers or introduce a generic framework because it sounds safer;
- add a focused negative test for the observed failure, using synthetic data and non-production execution;
- preserve existing legitimate public behavior and report ambiguous business rules instead of guessing;
- never call an app secure, compliant, hack-proof, or store-approved from a checklist or vendor name alone.

## Context-specific output contract

Unless the user asks for a different format, return or leave behind:

1. a short context snapshot of what was actually inspected;
2. the evidence ledger or a link to it;
3. the product-specific artifacts, findings, fixes, tests, or prompts selected from that context;
4. document-to-code mismatches and security/privacy gaps with exact locations;
5. facts still missing, labeled assumptions, counsel decisions, and runtime paths not verified;
6. commands/tests run and their results;
7. explicit statement of what the work did not establish.

If the repository or app is inaccessible, say exactly what was unavailable and stop short of producing publishable legal text or claiming a completed security review. Offer the smallest next evidence request—such as a repository path, redacted manifest, staging URL, approved test account, schema, or vendor inventory—without requesting secrets or unrelated personal data.

## Final anti-generic check

Before handoff, ask:

- Could this policy, finding, prompt, or fix be pasted into a different app unchanged?
- Does every material statement have an observed source, a provided fact, or an explicit placeholder/owner?
- Did the work inspect the route, data flow, vendor, role, and deployment boundary that makes the statement true?
- Are unknown jurisdiction, retention, deletion, children, vendor, payment, AI, and business-contact facts visible rather than guessed?
- Do tests cover the changed behavior and the negative case, and are all runtime limitations stated?

If the answer exposes generic or unsupported output, revise it before handoff.
