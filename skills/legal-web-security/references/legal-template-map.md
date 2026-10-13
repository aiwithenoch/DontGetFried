# Legal template map

This repository's templates are attorney-drafted starting points released under CC0 1.0. The `<mark>` tags identify fields that need customization. Select a template only after checking the user's facts, scope, and jurisdiction; have counsel confirm the result before it is published or signed.

## Candidate templates

| Repository path | Candidate use | Questions to resolve before relying on it |
| --- | --- | --- |
| `templates/privacy-policy-us/` | U.S.-focused privacy disclosure for a service collecting personal information | Which state and federal laws apply? Are users outside the U.S. targeted? Do actual collection, sharing, rights, retention, and tracking behavior match the text? |
| `templates/privacy-policy-gdpr/` | Broader privacy-policy starting point covering U.S. state laws and GDPR/UK GDPR concepts | Which controller/processor roles, establishments, targeting, transfer mechanisms, legal bases, rights, and representatives actually apply? |
| `templates/cookie-notice/` | Cookie policy/notice and tracking-technology disclosure | Which technologies execute before and after a user choice? What is the regional consent/notice requirement and how is withdrawal honored? |
| `templates/dpa-us/` | U.S. personal-data processing addendum | Who is the customer, provider, controller, or processor? What data, purposes, subprocessors, security measures, deletion, and audit commitments are real? |
| `templates/dpa-global/` | Global/U.S./EU/EEA/UK/Swiss data-processing starting point | Which transfer and supplementary-measure facts are current, and which annexes, subprocessors, restricted data, and retention rules need completion? |
| `templates/business-associate-agreement/` | HIPAA business-associate agreement starting point | Is there a covered-entity/business-associate relationship and protected-health-information processing? Obtain specialist review. |
| `templates/terms-of-use/` | Terms of service/use covering access, IP, liability, disputes, and use rules | What product promises, prohibited conduct, jurisdiction, consumer rules, warranty limits, and dispute process are intended and enforceable? |
| `skills/legal-web-security/references/refund-policy-outline.md` | Facts-required refund, cancellation, renewal, and chargeback outline for paid products | What are the actual prices, billing cadence, renewal notices, cancellation path, eligibility rules, statutory rights, fulfillment state, and payment-provider constraints? Obtain counsel/business-owner approval before publication. |
| `templates/master-services-agreement/` | Technology/services commercial agreement | What services, acceptance, support, IP, confidentiality, security, privacy, indemnity, liability, and termination terms were negotiated? |
| `templates/mutual-nda/` or `templates/one-way-nda/` | Confidentiality obligations for mutual or one-way disclosure | Who discloses what, for what purpose, with which exclusions, duration, permitted recipients, and remedies? |
| `templates/advisor-agreement/`, `templates/employee-offer-letter/` | Advisor or California exempt-offer-letter starting points | Are role, worker classification, location, equity, IP, confidentiality, arbitration, and local employment rules confirmed? |

## Use the map safely

1. Read the linked `README.md` when it exists, then inspect only the relevant `template.md`.
2. Copy the template into the user's document workflow only with the repository license and attribution expectations understood; do not represent it as a final legal instrument.
3. Keep every unresolved `<mark>` field, bracketed placeholder, optional clause, and jurisdiction-sensitive choice visible until an owner resolves it.
4. Build a behavior crosswalk: each material statement should point to the product behavior, configuration, vendor, or operational process that makes it true.
5. Flag stale or mismatched language instead of rewriting it from memory. Verify current law and contract requirements with qualified counsel or an authoritative source.
6. After an implementation change, re-check the affected notice or contract. A policy update that does not match deployed behavior is a defect, not a completed compliance task.

## Common escalation triggers

Escalate before publication or implementation when the work involves children, health or biometric data, precise location, financial/payment data, employment decisions, automated decisions with significant effects, cross-border transfers, regulated services, breach response, law-enforcement requests, customer security commitments, indemnities, liability caps, or a promise about deletion, encryption, certifications, or training data.
