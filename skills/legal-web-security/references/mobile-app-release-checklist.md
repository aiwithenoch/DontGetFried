# Mobile app and app-store release checklist

Use this checklist when a web product also ships as an iOS app, Android app, or cross-platform mobile app. It is an engineering release gate and issue-spotting aid, not a legal opinion, store-approval guarantee, or substitute for counsel. Platform rules, laws, and payment exceptions change; re-check the linked official sources at release time.

The supplied social-media transcript is treated as a list of leads, not as authority. Do not copy its fines, deadlines, approval guarantees, or one-line fixes into product requirements without verifying the facts, jurisdiction, product category, and current platform rule.

## How to use this checklist

For each applicable row, record:

- `verified` — the control or disclosure was checked against the shipped build and evidence is attached;
- `not verified` — work or evidence is missing;
- `not applicable — reason` — the feature or platform condition does not exist;
- `needs counsel` — legal interpretation, jurisdiction, contract, regulated data, or material risk remains unresolved.

Record the build number, platform, region, reviewer, date, source version or URL, and evidence location. A policy, App Store privacy detail, Google Play Data Safety answer, or security claim is defective if it does not match the shipped behavior.

## Claim triage: reject unsafe shortcuts

| Transcript claim pattern | Safe treatment |
| --- | --- |
| “Undisclosed AI always triggers a fixed FTC fine per violation per day, and one sentence fixes it.” | Do not encode a universal fine or disclosure cure. Inventory the AI feature, advertising claims, data flow, provider, retention, training/reuse, and applicable law. Give users accurate notice at the relevant point and escalate material AI claims or sensitive-data processing. |
| “Without arbitration, one user can organize a class action; one line saves millions.” | Arbitration, class waivers, consumer rights, enforceability, notice, and jurisdiction are counsel decisions. Do not promise that a clause prevents a lawsuit or eliminates liability. |
| “Apple and Google have one privacy nutrition label that lists everything.” | Treat Apple App Privacy Details and Google Play Data Safety as separate platform declarations. Report the app and third-party partner behavior accurately, keep the privacy policy current, and re-check each store's current rules. |
| “A DMCA registration costs a fixed amount and prevents all copyright liability.” | A designated agent and notice-and-takedown process can be relevant to U.S. safe-harbor eligibility, but registration is not blanket immunity and requirements are fact-dependent. Obtain current Copyright Office and counsel guidance. |
| “The copyright ceiling is automatically a fixed amount per upload.” | Statutory damages depend on the claim, work, conduct, and court; do not put a guaranteed amount in product copy or terms. Build rights, notice, takedown, counter-notice, and repeat-infringer processes. |
| “Obfuscate or null fields instead of deleting an account so the store accepts it.” | Never make cosmetic changes solely to pass review. Implement the approved deletion or anonymization design, document lawful retention, remove access, propagate deletion to vendors and backups where applicable, and test the real result. |
| “Every AI app must show the same AI-consent screen.” | There is no single universal screen. Decide what notice, consent, permission, contract, or opt-out is required from the actual data, provider, audience, jurisdiction, and platform flow. |
| “Apple has its own Stripe; RevenueCat bypasses the rules.” | Determine whether the transaction is a digital good, feature, subscription, physical good, person-to-person service, or an applicable exception. Follow the current Apple and Google payment rules. RevenueCat is an integration, not a policy exemption. |
| “Sentry makes an app bug-free.” | No tool proves an absence of bugs. Use tests, crash and performance monitoring, privacy-safe telemetry, triage, rollback, and a documented residual-risk decision. |
| “A Google search is enough to clear an app name.” | Search the relevant official trademark databases, common-law uses, app stores, domains, and markets; preserve the search record and obtain clearance advice where risk is material. |

## 1. Establish the mobile release facts

Before implementation or store submission, record:

- target platforms, OS versions, package/bundle identifiers, distribution regions, and release channels;
- whether users can create accounts, make purchases, upload content, message others, or use location, camera, microphone, contacts, health, biometric, financial, or precise-device data;
- whether the app calls an AI model, what is sent, where it is processed, whether prompts/uploads are retained or used for training, and which provider or subprocessors receive it;
- every SDK, pixel, crash reporter, analytics tool, ad network, payment provider, embedded browser, push provider, and server-side integration;
- age audience, child-directed features, age gates, parental-consent design, and regional restrictions;
- support URL, privacy-policy URL, terms URL, deletion URL, refund/cancellation path, business identity, and store-account owner;
- paid entitlements, subscriptions, credits, trials, renewals, taxes, fees, cancellation, refund, and restoration behavior;
- current store declarations, policy versions, review notes, test accounts, demo data, and the human owner for each answer.

Create a data-flow and SDK inventory before filling store forms. “The app does not collect it” is not a safe assumption when a third-party SDK, log pipeline, crash report, payment provider, or AI service receives it.

## 2. Store privacy declarations and policy alignment

### Apple

- Publish a privacy-policy URL in the store metadata and make the policy reachable inside the app.
- Complete App Privacy Details for data collected by the app and third-party partners, including data collected by SDKs. Include the purpose, linkage, and tracking answers that match the actual build.
- Keep App Privacy Details, the in-app policy, consent choices, SDK configuration, and backend behavior synchronized after every material release.
- Provide a support/contact path and an accessible privacy-settings path where users can review or change available choices.

### Google Play

- Complete the Data safety form for each app and keep it accurate across versions, regions, and third-party SDK behavior, including when the app collects no data.
- Provide a valid privacy policy and the required disclosures and consent controls for the data the app handles.
- If users can create accounts, provide the required in-app deletion path and the web deletion path, then verify that the actual deletion behavior matches the disclosure.

### Cross-platform evidence

Keep a release packet containing:

1. field-level data inventory and retention map;
2. SDK/version/destination/permission inventory;
3. privacy-policy and terms versions;
4. Apple App Privacy Details and Google Data safety answers;
5. consent and deletion tests on clean devices;
6. screenshots or recordings of the relevant flows;
7. owner approval and unresolved questions.

## 3. AI features and automated-processing disclosures

For each AI feature, map:

- input fields, uploads, prompts, metadata, identifiers, and output;
- model/provider, region, subprocessors, encryption, retention, deletion, training/reuse, and human access;
- whether the input can contain personal, confidential, health, financial, child, or regulated information;
- whether the output affects eligibility, safety, employment, housing, credit, education, health, legal advice, or another high-impact decision;
- user-facing claims, limitations, review path, correction path, and abuse reporting.

Implement disclosures and choices that match this map. Do not describe an external model as local, private, encrypted, human-reviewed, or non-training unless the contract and implementation support the statement. Do not market an AI feature as replacing a professional without evidence and counsel review. Add a human escalation or safety path for high-impact or safety-sensitive use cases when the product owner and counsel approve the design.

Test that optional AI processing is not initialized before the applicable choice, that consent or opt-out changes affect subsequent calls, and that prompts, outputs, debug logs, analytics, and crash reports do not leak unnecessary user data.

## 4. Account creation and deletion

When an account can be created:

- provide an obvious in-app deletion route on iOS;
- provide the in-app route and a working web deletion path for Google Play where required;
- explain what is deleted, what may be retained by law or for a documented security/accounting need, the expected timing, and how subscriptions or pending transactions are handled;
- revoke sessions, tokens, device links, shared access, notifications, and recovery methods as part of deletion;
- propagate approved deletion or anonymization to processors, analytics, support tools, caches, queues, replicas, and backups according to the retention design;
- issue a confirmation or status reference without exposing personal data in the URL or notification;
- test a fresh account, an account with purchases, an account with user content, and a failed/partial vendor deletion.

Anonymization is acceptable only when the resulting data is actually no longer attributable under the approved design. Replacing values with placeholders, keeping identifiers in logs, or retaining a re-identification key is not automatically deletion. Do not retain data merely to preserve a database shape unless the retention basis, notice, access controls, and counsel decision are documented.

## 5. Purchases, subscriptions, fees, and refunds

Classify every payment before implementation:

- digital feature, subscription, credit, consumable, or other in-app entitlement;
- physical good or service consumed outside the app;
- person-to-person service, marketplace transaction, donation, or other category;
- web purchase restored or referenced in the app;
- country, storefront, business model, and current platform exception.

Then verify the current Apple and Google rules for that exact classification. Do not ship a “Stripe instead of store billing” workaround based on a social-media claim. A billing integration can simplify receipts or entitlements but does not decide eligibility for an exception.

Before commitment, show the total mandatory price, currency, recurring amount and frequency, trial conversion, renewal timing, taxes/fees where required, cancellation route, restoration behavior, and refund/cancellation terms. Ensure the app, checkout, store metadata, receipt, terms, refund policy, and support scripts tell the same story. Never hide a required fee until the final screen or make cancellation materially harder than purchase.

## 6. User-generated content, copyright, and moderation

If users can upload, publish, share, or submit text, photos, video, audio, designs, or feedback:

- define the user's rights and the service's limited license in terms, with counsel review;
- provide content rules, reporting, moderation, removal, appeal, and support contact paths;
- filter or review where appropriate, respond to reports, block abusive users, rate-limit uploads, and protect reporters;
- restrict file type, size, duration, storage, processing, and executable content; scan and isolate uploads before serving them;
- prevent public indexing, metadata leakage, and accidental exposure of private uploads;
- preserve a lawful notice/takedown and counter-notice process where applicable, including repeat-infringer handling and records;
- test copyright complaints, abusive content, account deletion, and vendor/storage deletion end to end.

For a service seeking U.S. DMCA safe-harbor treatment, confirm whether the service-provider category fits, designate an agent through the U.S. Copyright Office process, publish the required contact information, maintain current registration, and implement the applicable notice-and-takedown requirements. This is not a blanket defense against infringement and does not replace counsel review.

## 7. App name, trademarks, and launch claims

Before committing to an app name, logo, slogan, or feature name:

1. search the USPTO trademark database and the relevant official databases for target markets;
2. search common-law uses, app stores, domains, social accounts, and close variants;
3. preserve the date, query scope, results, and unresolved conflicts;
4. obtain clearance advice for a confusingly similar, high-value, regulated, or international mark.

Audit every material store, landing-page, testimonial, security, privacy, performance, AI, “free,” “unlimited,” and “no data” claim. Assign an evidence owner and expiry/review date. Remove fabricated or undisclosed incentivized reviews, unsupported testimonials, false scarcity, and claims that the evidence cannot reproduce.

## 8. Public feedback boards

A feedback board can be useful product research, but it is also a public user-content surface. Before enabling it:

- disclose whether submissions are public, searchable, licensed, moderated, or used for product decisions;
- minimize fields and prevent names, email addresses, access tokens, secrets, health data, or private customer details from being posted;
- provide report, edit, delete, export, and support paths; authenticate actions proportionally; rate-limit spam and scraping;
- moderate abuse, copyrighted material, personal data, and confidential information;
- avoid implying that upvotes promise delivery, ownership, compensation, or a particular roadmap outcome;
- include feedback-board data in the privacy, retention, deletion, UGC, and vendor inventory.

## 9. Proactive application-security baseline

Treat the following as implementation checks, not slogans:

- keep API keys, signing keys, database secrets, provider tokens, and admin credentials out of the app bundle, source, logs, screenshots, and public repository;
- distinguish intentionally public client identifiers from privileged secrets; enforce authorization on the server even when a client key is public;
- enable database row-level security or equivalent tenant isolation and test deny-by-default access;
- enforce server-side authentication, object/record authorization, and field-level authorization; prevent IDOR, mass assignment, and field tampering;
- encrypt sensitive data in transit and at rest where the design requires it; use platform secure storage for mobile tokens and credentials;
- use secure, scoped sessions and cookies on web surfaces; rotate/revoke tokens and do not put secrets in URLs;
- hash passwords with a current password KDF and safe parameters; rate-limit login, recovery, signup, upload, and expensive AI operations; add abuse/bot controls proportionate to risk;
- parameterize queries; validate type, length, encoding, and business rules server-side; encode untrusted content for its output context;
- restrict and scan uploads, store outside executable paths, generate safe names, strip or handle metadata, and serve with safe content types;
- return only required fields; redact logs, traces, analytics, crash reports, and support exports; scrub AI prompts and user content where possible;
- send security headers, use HTTPS with secure transport configuration, and test deep links, redirects, WebViews, CORS, and embedded content;
- scan dependencies, mobile packages, build actions, and container/base images; pin or review updates and remove unused packages;
- instrument crash, abuse, auth, payment, deletion, and vendor failures with privacy-safe telemetry and an actionable response/rollback path.

Verify each control with a test or inspection. A public/anonymous database key, client-side validation, SDK setting, or monitoring dashboard is not proof of authorization, privacy, or security.

## 10. Store-review evidence packet

| Review area | Evidence to attach | Status/owner |
| --- | --- | --- |
| Privacy | In-app policy, store URL, data inventory, App Privacy Details, Google Data safety answers |  |
| AI processing | Provider/data-flow map, user notice/choice, retention/training terms, claim evidence |  |
| Account deletion | iOS in-app test, Google in-app/web test, deletion receipt, retention exceptions |  |
| Payments | Product classification, store configuration, price/renewal screenshots, restore/cancel/refund tests |  |
| UGC | Terms, content rules, report/block/filter flow, moderation owner, takedown process |  |
| Security | Threat model, auth/access tests, secret scan, dependency scan, upload tests, redaction checks |  |
| Accessibility | Alt-text review, contrast measurements, keyboard/assistive-technology checks, focus behavior |  |
| Fair design | Checkout totals, cancellation path, review provenance, claim evidence, no dark-pattern review |  |
| Support and identity | Business details, support URL, contact response process, age/child decision |  |
| Release quality | Crash-free evidence with caveats, regression tests, test accounts, known-issue register, rollback plan |  |

Do not submit a store form or publish a policy with guessed answers. Mark the row `needs counsel` or `not verified`, assign an owner, and resolve it before release when the risk is material.

## Official reference starting points

- Apple App Review Guidelines: <https://developer.apple.com/app-store/review/guidelines/>
- Apple App Privacy Details: <https://developer.apple.com/app-store/app-privacy-details/>
- Apple account deletion: <https://developer.apple.com/support/offering-account-deletion-in-your-app/>
- Apple In-App Purchase configuration: <https://developer.apple.com/help/app-review/before-submitting-for-review/configure-in-app-purchases/>
- Google Play Data safety: <https://support.google.com/googleplay/android-developer/answer/10787469>
- Google Play User Data policy: <https://support.google.com/googleplay/android-developer/answer/10144311>
- Google Play account deletion: <https://support.google.com/googleplay/android-developer/answer/13327111>
- Google Play payments policy: <https://support.google.com/googleplay/android-developer/answer/10281818>
- U.S. Copyright Office DMCA designated agent directory: <https://www.copyright.gov/dmca-directory/>
- USPTO trademark search: <https://www.uspto.gov/trademarks/search>
- FTC AI claims enforcement: <https://www.ftc.gov/news-events/news/press-releases/2024/09/ftc-announces-crackdown-deceptive-ai-claims-schemes>
- FTC reviews and testimonials: <https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers>
- FTC dark patterns: <https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers>
- OWASP Application Security Verification Standard: <https://owasp.org/projects/asvs>
- NIST Secure Software Development Framework: <https://csrc.nist.gov/pubs/sp/800/218/final>
