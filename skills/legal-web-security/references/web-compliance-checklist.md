# Public-web legal, trust, and accessibility checklist

Use this checklist for a public website, application, checkout, marketing flow, email program, or user-facing form. It is an engineering release gate and issue-spotting aid, not a legal opinion. Mark every row `verified`, `not verified`, `not applicable — reason`, or `needs counsel`; attach the evidence, owner, and date.

## 1. Customer-facing legal documents

- **Privacy policy:** publish a fact-matched privacy policy before or at the point required for collection. Start with `templates/privacy-policy-us/` or `templates/privacy-policy-gdpr/` only after confirming jurisdictions, roles, data categories, purposes, sharing, transfers, retention, rights, vendors, and actual product behavior.
- **Terms of service/use:** link the terms before the relevant use or purchase. Start with `templates/terms-of-use/`; confirm the service description, acceptable use, IP, warranties, liability, disputes, subscription terms, and user promises with counsel.
- **Refund/cancellation policy:** if the product takes payment, state the actual refund eligibility, timing, method, cancellation, renewal, delivery, exceptions, statutory-rights reservation, and contact process. Use [the refund-policy outline](refund-policy-outline.md) until an approved policy exists; never invent a universal refund period.
- **Cookie policy/notice:** use `templates/cookie-notice/` to explain each cookie or similar technology, purpose, provider, duration, category, and control. Reconcile it with the privacy policy, SDK inventory, and consent system.
- **Business details:** show the legal/trading name, contact method, customer-support route, and any address, registration, license, or jurisdiction details required for the business and target market. Do not fabricate a business identity or use a placeholder in production.
- **Link integrity:** keep policy links visible, readable, keyboard-accessible, localized where required, versioned, and reachable from the relevant form, checkout, footer, and account/privacy settings. Check that the deployed text matches the behavior.

## 2. Consent, collection, and data rights

### Forms and consent

- Inventory every field and explain its purpose, required/optional status, retention, recipient, and deletion path.
- Remove fields that are not necessary for the stated purpose. Do not collect a phone number, date of birth, precise location, contacts, identity document, or sensitive data merely because a vendor or form template makes it convenient.
- Use clear, specific consent language for optional processing. Do not preselect optional consent, bundle marketing consent into terms acceptance, hide material information, or make rejection harder than acceptance.
- Separate service-required processing, optional analytics/advertising, and marketing subscriptions. Provide an accessible way to withdraw or change optional choices.
- Record only the minimum consent evidence needed: purpose/version, timestamp, region or ruleset when relevant, source, and choice. Protect it like personal data.
- Test validation and error messages without echoing sensitive values. Make labels, instructions, error recovery, and policy links accessible.

### Cookie consent banner

- Classify technologies as necessary or optional based on actual behavior; do not let a vendor's label decide the category.
- Gate optional cookies, pixels, and SDK initialization until the applicable choice is made. Verify tags in a clean browser profile and after withdrawal, not only by inspecting banner copy.
- Present accept, reject, and manage choices with comparable prominence and no confirm-shaming, obstruction, or preselected optional toggles.
- Make the banner and preference center keyboard-operable, screen-reader understandable, focus-visible, contrast-safe, dismissible where appropriate, and usable on small screens.
- Persist the choice only for the necessary period and purpose; provide a visible way to reopen settings and withdraw. Test consent across subdomains, sessions, logged-in states, and vendor calls.

### Data minimization, deletion, and age

- Map collection, storage, analytics, support, backups, and vendor transfers. Delete or anonymize data when the stated retention period or approved request requires it, including caches, queues, replicas, and vendor systems where applicable.
- Provide a clear data-deletion request option and a safe workflow: accessible entry point, identity verification proportional to risk, scope confirmation, status/receipt, approved exceptions, vendor propagation, and audit evidence without exposing the requester's data.
- If children may use the service or the service targets children, establish the applicable age threshold and parental-consent/notice process with counsel before collecting data. Minimize collection, avoid profiling/marketing where not approved, and do not infer age consent from a generic terms checkbox.

### Third-party SDK and vendor audit

For every SDK, pixel, widget, API, analytics tool, payment tool, or embedded service, record:

- owner, version, purpose, data fields, identifiers, cookies/storage, permissions, destinations, subprocessors, retention, and model-training or reuse terms;
- whether it runs before consent, after a specific choice, only server-side, or not at all in a region;
- security review, privacy/DPA status, transfer basis or counsel question, vendor deletion/opt-out support, and removal/rollback path.

Remove unused SDKs, excessive permissions, undocumented trackers, and vendors that cannot meet the approved data and security requirements. Re-run the inventory after dependency or tag-manager changes.

### Email preferences

- Include a clear unsubscribe or equivalent opt-out path in commercial email, make it easy to use, and maintain a suppression list across providers and products.
- Keep transactional/relationship messages distinct from marketing; do not use that distinction to hide promotional content or ignore a valid opt-out.
- Test the link, token expiry, authentication burden, mobile rendering, and propagation to every sender. Record the applicable jurisdiction and service standard with counsel.

## 3. Fair design, pricing, reviews, and claims

- **Remove dark patterns:** no confirm-shaming, disguised ads, forced continuity, preselected optional purchases, confusing privacy choices, obstructive cancellation, false hierarchy, or a path that makes acceptance easy and refusal or deletion difficult. Use plain labels and comparable prominence for materially different choices.
- **Remove hidden fees:** show the total mandatory price, recurring amount/frequency, taxes or delivery charges where applicable, trial-to-paid conversion, renewal timing, cancellation method, and refund terms before commitment. Re-test the final amount for different regions, devices, quantities, and account states.
- **Remove fake reviews:** publish only authentic experiences or clearly labeled testimonials; do not fabricate, buy, alter, suppress, or selectively present reviews in a misleading way. Disclose material connections and incentives. Treat AI-generated testimonials as high-risk and escalate them.
- **Remove unsupported claims:** every material claim has an evidence owner, source, date, scope, and expiration/review trigger. Qualify claims such as `secure`, `private`, `encrypted`, `compliant`, `no hidden fees`, `unlimited`, `zero data`, `carbon neutral`, or performance guarantees. Do not copy vendor marketing as proof.

## 4. Accessibility baseline

Use WCAG 2.2 AA as an engineering baseline unless the project has a documented alternative; this does not decide which accessibility laws apply.

- Add meaningful `alt` text for informative images, empty alt text for decorative images, and an equivalent text description for charts or complex visuals. Do not use filenames, duplicated nearby text, or vague labels such as `image`.
- Measure text contrast: target at least 4.5:1 for normal text and 3:1 for large text; document exceptions and re-test states such as hover, disabled, error, focus, dark mode, and consent overlays.
- Make every function operable with a keyboard: logical focus order, visible focus, no keyboard trap, usable dialogs/menus, skip/bypass mechanism where needed, and focus returned to a sensible control after closing an overlay.
- Use native semantic controls where possible, label form fields programmatically, expose error/status changes, and test the privacy banner, consent controls, checkout, deletion request, and unsubscribe path with keyboard and assistive technology.

## 5. Fonts, images, and other assets

- Keep an asset inventory with source, creator, license, permitted use, attribution, modification, seat/domain limits, expiration, and proof of purchase or permission.
- License fonts, stock images, icons, illustrations, music, and code before shipping. Do not assume that a search result, free download, npm package, or AI output is unencumbered.
- Store required notices and attributions with the project, and replace assets whose license cannot be verified. Ensure licensed assets still receive appropriate alt text and do not encode essential text only in an image.

## Release evidence

| Check | Evidence | Owner | Status | Review date |
| --- | --- | --- | --- | --- |
| Privacy, terms, refund, and cookie documents | Deployed URLs, version/date, counsel/business approval |  |  |  |
| Consent and data minimization | Form inventory, clean-browser tag test, consent records |  |  |  |
| SDK/vendor audit | Inventory, contracts/DPA, permissions, removal plan |  |  |  |
| Deletion and age safeguards | Request test, deletion receipt, age/parental-flow decision |  |  |  |
| Fair pricing, reviews, and claims | Checkout capture, review provenance, claim evidence |  |  |  |
| Accessibility | Automated/manual results, keyboard pass, contrast measurements, alt review |  |  |  |
| Asset licensing and business identity | License records, notices, published contact details |  |  |  |
| Email opt-out | Test message, unsubscribe result, suppression propagation |  |  |  |

## Reference starting points

- WCAG 2.2: <https://www.w3.org/TR/WCAG22/>
- WCAG 2.2 Non-text Content: <https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html>
- WCAG 2.2 Contrast (Minimum): <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html>
- WCAG 2.2 Focus Visible: <https://www.w3.org/WAI/WCAG22/Understanding/focus-visible>
- FTC dark patterns guidance: <https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers>
- FTC reviews/testimonials rule: <https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers>
- FTC commercial-email guidance: <https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business>
