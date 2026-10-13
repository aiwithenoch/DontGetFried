# Independently Verified, Coverage-Led Audit Workflow

Use this reference only when the user explicitly asks for a security audit, a full or comprehensive pre-launch review, a legal/security audit, a security report, a coverage record, or repeatable audit artifacts. A normal bug fix, narrowly scoped review, or one-control implementation should use the smaller workflow in `SKILL.md` and the relevant focused reference.

This workflow adapts the useful audit mechanics of Cloudflare's MIT-licensed [`security-audit-skill`](https://github.com/cloudflare/security-audit-skill) (reviewed at commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`): deterministic coverage, source-grounded candidate records, separate verdicts, independent verification, machine-readable output, and additive reruns. It is an original adaptation for context-first legal and web-security work. Do not copy Cloudflare-specific attack prose, branding, or implementation files into a target application. Preserve the [source license context](https://github.com/cloudflare/security-audit-skill/blob/main/LICENSE) when redistributing this reference.

## 1. Choose the audit mode deliberately

Use the smallest mode that answers the request:

- `guidance`: normal skill behavior; inspect the relevant context, make the requested change or review, and leave a concise evidence-backed result. Do not create a broad ledger merely because the word “security” appears.
- `quick`: explicit, bounded audit of a named surface or launch gate. One verifier may combine candidate and final-record verification, but it still must be independent of the hunter that proposed the candidate.
- `standard`: repository-wide or product-surface audit with separate hunting and final-record verification passes.
- `deep`: standard mode plus adjacent dependency, deployment, vendor, privacy, accessibility, and jurisdiction routes that the context snapshot shows are material.

If the user has not authorized an audit or report, do not silently perform a broad crawl, probe a deployment, create a penetration-test claim, or write audit artifacts into the application repository. If the target cannot be inspected, produce an evidence-gap record rather than a generic “secure” report.

## 2. Establish the context and execution boundary first

Before seeding coverage, read the context-first operating model and any applicable web, mobile, production, Ghana/Africa, or vendor reference. Record:

- target repository/ref, stack, entrypoints, routes, APIs, jobs, storage, database policies, deployment and distribution targets;
- actors, assets, tenant boundaries, trust boundaries, data flows, third parties, AI providers, payment rails, analytics, cookies, emails, uploads, logs, backups, and deletion paths;
- actual business, user, employee, vendor, hosting, and target-country facts; use a country matrix rather than an “Africa” label;
- what is `observed`, `provided`, `assumed`, `unknown`, `needs counsel`, or `not verified`;
- the approved source/local/staging execution boundary and the exact owner authorization for any runtime check.

Do not contact production, unrelated systems, external/shared services, real customer accounts, or live payment/AI endpoints. Prefer repository source, static configuration, local fixtures, local emulators, and synthetic identities. If a deployment fact is decisive and cannot be observed safely, keep the record as `needs_validation` and state the owner-observed check needed. Never place secrets, tokens, raw personal data, payment data, or unredacted incident evidence in audit artifacts.

## 3. Use an isolated, reproducible artifact directory

Create an audit output directory only when the user requests artifacts or a full audit. Use the caller's requested path; otherwise use a disposable work/output location outside the target application. Do not overwrite a prior run. A run may contain:

```text
<audit-output>/
  architecture.md
  coverage-ledger.json
  findings.json
  REPORT.md
  FINDINGS-DETAIL.md          # required when confirmed medium/high/critical records exist
  NEEDS-VALIDATION.md         # required when unresolved records exist
```

`architecture.md` is a context snapshot, not a claim that every listed control is present. It must identify the version/ref, surfaces, actors, boundaries, data/vendor paths, jurisdiction matrix, and explicit exclusions. Keep evidence redacted and repository-relative. If a file is generated from runtime output, label it `not verified` unless the runtime was explicitly authorized and the observation is retained safely.

Run the bundled validator before reporting:

```sh
python3 skills/legal-web-security/scripts/validate_audit_records.py <audit-output>
```

The validator checks structure, stable IDs, safe paths, verdict separation, and coverage/findings consistency. A passing validator proves only artifact integrity; it does not prove security, legal compliance, accessibility, or store approval.

## 4. Seed a deterministic coverage ledger

The ledger is the coverage claim. A paragraph saying “auth was reviewed” is not coverage evidence. Create one unit for each material tuple:

```text
surface | boundary | subsystem | attack_class
```

Use lowercase, stable, repository-independent slugs and join them with `|` for `coverage_id`, for example `web|browser-api|auth|authorization`. Do not create duplicate semantic tuples under different IDs. Sort units lexicographically by `coverage_id`.

Choose attack classes from the actual product, including only applicable units. Typical classes are:

- identity, session, recovery, authorization, tenant isolation, admin/support access;
- input/output injection, XSS, CSRF, SSRF, unsafe deserialization, file upload/download, path traversal;
- rate limits, resource exhaustion, queues/jobs, bot abuse, scraping, denial of service;
- secrets, logs, error responses, headers, TLS, dependencies, build/release, cloud/edge configuration;
- payments, webhooks, entitlements, refunds, tax/vendor boundaries;
- privacy notice, consent, cookies, SDKs, minimization, retention, deletion, exports, children, AI disclosures;
- legal artifacts, claims, reviews, pricing/fees, business identity, unsubscribe, accessibility, font/image licensing.

Each unit records at least:

```json
{
  "coverage_id": "web|browser-api|auth|authorization",
  "surface": "web",
  "boundary": "browser-api",
  "subsystem": "auth",
  "attack_class": "authorization",
  "status": "planned",
  "prior_status": "none",
  "owner": null,
  "reviewed_paths": [],
  "checks": [],
  "result_fingerprints": [],
  "unresolved": []
}
```

Use these status meanings:

| Status | Required meaning | What it cannot mean |
| --- | --- | --- |
| `planned` | Unit exists but no review has started | not “safe” |
| `in_progress` | An identified reviewer owns the current attempt | not covered |
| `covered` | Source/local evidence reviewed the unit and no unresolved candidate remains; final disposition fingerprints may be retained | not a clean bill of health |
| `candidate` | A stable finding fingerprint still needs validation or an unresolved disposition | not a confirmed vulnerability |
| `blocked` | A material check could not be completed and the blocker is recorded | not “not applicable” |
| `deferred` | Scope owner intentionally deferred it with a reason | not silently omitted |
| `out_of_scope` | Explicitly excluded with a reason | not a coverage result |
| `not_applicable` | The product context proves the unit does not apply | not a guess |

For each check, retain the reviewer ID, method (`source`, `local`, `runtime`, or `provided`), repository-relative reviewed paths, exact local checks or test names, result fingerprints, and unresolved items. A unit's `reviewed_paths` must equal the union of its checks. Do not use a scratch path, symlink, external URL, or raw runtime dump as retained evidence.

## 5. Hunt by coverage wave, not by intuition

Work through the ledger in deterministic priority order:

1. exposed entrypoints and lower-trust inputs;
2. authentication, authorization, tenant and resource boundaries;
3. sensitive data, payment, AI, upload, webhook, deletion, and admin flows;
4. privacy/consent/legal claims that describe those flows;
5. availability, dependency, deployment, observability, and accessibility controls;
6. deferred or blocked units that can be resolved within the authorized boundary.

For every candidate, prove as much of this chain as the evidence supports:

```text
lower-trust principal → native input/action → missing or bypassed control
→ crossed trust/data boundary → affected principal/resource → concrete result
```

A generic “could be vulnerable” statement is not a candidate. Follow the path into adjacent code when the result depends on middleware, policies, schemas, vendor configuration, queue consumers, or deployment settings. Do not infer provider behavior from the provider name or from a frontend SDK import.

Deduplicate candidates by a stable fingerprint derived from the source-visible root cause and affected boundary. A different symptom with the same root cause is one candidate; a different root cause gets a new fingerprint. Keep the fingerprint unchanged when the candidate moves between verdicts.

## 6. Keep verdicts and legal routing separate

Every final record has exactly one verdict:

- `confirmed`: an independent reviewer reproduced or otherwise established the complete source/local result within the authorized boundary. It may carry severity, but the severity must reflect demonstrated impact and realistic likelihood—not a statutory penalty, social-media claim, or worst-case imagination.
- `needs_validation`: source evidence supports a concrete candidate, but a decisive runtime, deployment, vendor, business, jurisdiction, or counsel fact is unavailable. It has no severity. It must name the blocker and an exact local or owner-observed resolution plan.
- `rejected`: an independent reviewer disproved the claimed root cause, path, prerequisite, or result. Retain the record so a repeat run does not rediscover the same unsupported claim without changed evidence.

Do not use `needs_validation` as a parking lot for an unresearched idea. Do not add `severity`, `execution`, `remediation`, or a confirmed `root_cause` to a `needs_validation` or `rejected` record. Do not convert a policy mismatch into a legal violation without an applicable source and counsel/owner decision.

Every record must include:

- stable `fingerprint`, title, description, affected surface, repository-relative `trace`, and evidence;
- `context` with data categories, jurisdiction(s) or `unknown`, and `legal_status` of `not_assessed`, `route_only`, `needs_counsel`, or `verified_source`;
- legal/source references as URLs or repository paths, with the source type and effective/status caveat when relevant;
- a trace beginning at the lower-trust entrypoint and ending at the sink/boundary effect when the trace has more than one item;
- no claims stronger than the evidence. A missing runtime configuration is `not verified`, not “absent.”

For a `confirmed` record, include `root_cause`, intended behavior, conditions, target-native bounded execution, observed result, smallest effective remediation, severity, confidence, and regression verification. For `needs_validation`, include `claimed_root_cause`, blockers, and at least one precise `validation_plan.local`, `validation_plan.deployment`, or `validation_plan.owner`. For `rejected`, include the claimed root cause, trace/evidence, and the reason for rejection only.

## 7. Validate with a fresh reviewer

The person or agent that hunted a candidate must not be the only person deciding its final verdict. Give a fresh reviewer the candidate, linked ledger checks, cited source, architecture facts needed to interpret it, and the execution boundary. Do not give the reviewer another reviewer's conclusion as an instruction.

The fresh reviewer must:

1. re-read every cited source location and check safe repository-relative paths and positive line numbers;
2. reconstruct the strongest authentication, authorization, validation, normalization, lifecycle, framework, vendor, and containment controls on the path;
3. reproduce the minimum local result where safe, using synthetic identities/resources and the target's native interface;
4. decide whether the legal route is a source-backed question, `needs counsel`, `not assessed`, or not applicable;
5. preserve the candidate fingerprint or explicitly identify a different root cause;
6. return one schema-shaped decision, not prose surrounding JSON.

For `confirmed`, the reviewer must verify the affected principal/resource, actual observed result, remediation invariant, confidence, and severity separation. For `needs_validation`, the reviewer must confirm that the blocker is genuinely outside source/local observation and that the proposed owner check is safe, bounded, and applicable. If the source or local evidence refutes the claim, use `rejected`.

For `standard` and `deep`, run a second fresh pass over every retained `confirmed` and `needs_validation` record after writing `findings.json`. If that pass materially changes the root cause, trace, observed result, impact, severity, or verdict, remove the disputed record from the final file, update the ledger to `candidate`, and obtain another independent decision before restoring it. A malformed or prose-wrapped reviewer response is not evidence; retry with a fresh reviewer within the budget or leave the candidate unresolved.

## 8. Write target-neutral reports only after records are final

Sort `findings.json` by fingerprint and run the validator. Derive prose from the final records and ledger; prose cannot upgrade a verdict or severity. `REPORT.md` must state:

- run profile, target ref, scope, source/local/runtime boundary, prior-run use, and incomplete/deferred/out-of-scope units;
- confirmed findings in a separate table with severity, boundary, and observed result;
- a separate `NEEDS VALIDATION` section with blocker and safe resolution plan, without severity;
- rejected records only as coverage history when useful, never as findings;
- positive patterns, hardening notes, coverage counts, and remaining gaps;
- the exact statement that the audit is not a legal opinion, compliance certification, penetration-test authorization, or guarantee of security/store approval.

`FINDINGS-DETAIL.md` is for confirmed medium/high/critical records and must include the trace, lower-trust principal, native reproduction, conditions, actual result, impact, source fix, and regression test. `NEEDS-VALIDATION.md` is for unresolved records and must not turn an owner-observed check into live attack instructions.

Never claim “all vulnerabilities found,” “secure,” “compliant,” “App Store approved,” or “hack-proof” from a completed ledger or a passing validator. A clean result means only that the recorded scope and evidence produced no confirmed record in that run.

## 9. Make reruns additive and honest

At the beginning of every rerun, read prior `architecture.md`, `coverage-ledger.json`, and `findings.json` if present. Preserve old records; do not overwrite them with a clean rerun. Carry a prior `confirmed` record only when its source, conditions, and relevant configuration are unchanged and a fresh reviewer rechecks it. Mark changed-source records `prior_confirmed_changed_source` and revalidate them. Keep prior `needs_validation`, `blocked`, `deferred`, and `out_of_scope` units visible. A prior `rejected` record suppresses only the exact unchanged claim, not the whole coverage unit.

Use a new run ID, append new evidence/checks, and keep coverage and finding fingerprints stable. If budget, missing authorization, or missing runtime access prevents a required verifier or critic, set the run to `incomplete` and list every unresolved fingerprint and unit. Do not hide incomplete coverage behind a green-looking report.

## 10. Safe operation rules

- Use read-only source inspection and bounded local fixtures by default.
- Use runtime or browser checks only against an explicitly authorized local/staging target, with synthetic accounts, low volume, and a stop condition.
- Never exploit a real user's account, enumerate records, upload executable content, send unsolicited mail, test live payment/AI calls, stress a service, alter production, wipe a database, or bypass a control “to see what happens.”
- Keep scratch output separate from retained evidence. Promote only predeclared, redacted, regular files; reject symlinks, special files, archives, changing files, oversized files, and paths escaping the output root.
- Redact secrets, tokens, personal data, payment data, precise locations, and private incident evidence before retention.
- Route statutory interpretation, filing/licensing, child/health/biometric data, cross-border transfer, marketing, tax, payment, and contract decisions to the applicable country matrix and counsel/owner. The audit workflow organizes evidence; it does not create legal advice.
