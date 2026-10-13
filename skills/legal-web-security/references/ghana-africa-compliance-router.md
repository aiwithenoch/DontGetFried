# Ghana-first and Africa-aware compliance router

> Research checked: 2026-10-13. This is an engineering and issue-spotting reference, not a legal opinion, certification, or substitute for Ghanaian or other local counsel. Re-check official sources before publishing a policy, changing collection, launching payments, or making a country-specific legal claim.

This reference changes the default jurisdiction behavior of `legal-web-security`:

- Ghana is the first jurisdictional profile when the user says the product is Ghanaian, operates from Ghana, targets Ghana, or handles Ghana-originating data.
- “Africa” is not one legal system. Never return an “Africa-compliant” conclusion without a country-by-country scope, regulator, sector, data-flow, and effective-law check.
- Regional instruments, regulator guidance, policies, consultations, draft bills, platform rules, and engineering frameworks are not interchangeable. Label which one is being used.
- The agent must inspect the real application and its actual business model before selecting legal text. Ghanaian law changes the questions to ask; it does not make a generic policy accurate.

## 1. Jurisdiction and evidence gate

Before drafting or changing anything, build a jurisdiction matrix. Do not infer the answer from a `.gh` domain, a founder's nationality, a cloud region, or a payment brand.

| Dimension | Record separately | Why it matters |
| --- | --- | --- |
| Operating entity | Incorporation/registration country, business name, legal status, physical address, tax status | Determines entity disclosures, tax, regulator registration, contracting party, and local service obligations |
| Target market | Countries where the product is advertised, sold, or made available | May trigger consumer, privacy, marketing, accessibility, payments, and licensing rules |
| Data subjects | Residence/location of users, employees, children, and customers | Privacy rules can follow the person or the originating data, not only the company |
| Processing footprint | Hosting, databases, backups, support, analytics, AI providers, payment processors, email/SMS vendors, subprocessors | Creates transfer, processor-contract, disclosure, security, retention, and incident questions |
| Sector | General SaaS, education, health, finance, payments, telecom, public service, critical infrastructure, cybersecurity service | Sector regulators and licensing can override a general web baseline |
| Distribution | Web, Android, iOS, app stores, WhatsApp/SMS/USSD, partner marketplace | Adds platform, telecom, mobile-money, store, and communications obligations |
| Commercial model | Free, subscription, one-time digital sale, marketplace, advertising, credits, donations, merchant-of-record | Changes pricing, refund, tax, consumer, payment, and advertising analysis |
| Audience and risk | Children, vulnerable users, biometric/health/precise location/financial data, user-generated content, automated decisions | Changes minimisation, safeguards, notices, consent, moderation, DPIA/risk review, and counsel escalation |

Use these statuses in the ledger:

- `observed`: supported by code, config, manifests, tests, or an authorized synthetic runtime trace;
- `provided`: supplied by the product owner but not independently checked;
- `unknown`: the evidence is missing;
- `assumed`: temporary scaffolding only, never a published fact;
- `needs counsel`: a legal interpretation, jurisdiction choice, consumer-rights decision, contract term, or filing/licence decision;
- `not verified`: a control or claim was expected but the available evidence did not prove it.

If the user only says “Africa,” do not silently choose every African country. Ask for or record the actual launch countries. If the user expressly says Ghana, run the Ghana core below and keep every other country as `unknown` until identified.

## 2. Ghana core: current-law routing

The following is a routing map, not a promise that the product is compliant. The agent must cite the exact section/source in its evidence ledger and connect it to the relevant code, route, SDK, vendor, contract, or business decision.

### 2.1 Data protection, privacy, and data flows

**Primary anchors:** Article 18(2) of Ghana's [1992 Constitution](https://ghalii.org/akn/gh/act/1992/constitution/eng%401996-12-31) provides the constitutional privacy backdrop. Ghana's Data Protection Act, 2012 (Act 843) commenced 16 October 2012. Use the [official government PDF](https://cybersecurity.gov.gh/documents/Data_Protection_Act_2012.pdf) and the [GhaLII text of Act 843](https://ghalii.org/akn/gh/act/2012/843/eng%402012-05-18) as the legal-text references. The GhaLII page is a primary legal-text mirror; the Cyber Security Authority URL is the government-hosted PDF.

When Ghana is in scope, inspect at least:

1. **Scope and territorial questions.** Section 45 covers a controller established in Ghana and certain processing using equipment or a processor in Ghana, and the Act also addresses information originating partly or wholly from Ghana. Section 18(2) requires attention to foreign data-protection law for foreign data subjects whose data is sent to Ghana for processing. Map the entity, data subject, data origin, processor, hosting, backup, and support locations; do not reduce this to “the database is in Ghana” or “the server is in the United States.”
2. **Principles and collection.** Sections 17–26 cover the data-protection principles. Trace lawfulness/reasonableness, minimality, purpose specification, notice, retention, compatible further processing, accuracy, and security to every form, API field, cookie, event, log, AI prompt, upload, and export. A checkbox cannot justify unnecessary fields.
3. **Registration.** Section 27 says a data controller intending to process personal data shall register; sections 46–56 establish the register, renewal, prohibition on processing without registration, and related consequences. The DPC's current [organisations page](https://dpc.gov.gh/for-organisations/) says organisations processing personal data should register, renew every two years, publish an organisational privacy policy, and appoint/train a data protection supervisor. The Act's section 58 wording uses “may appoint” a qualified supervisor, so the agent must surface the Act/guidance distinction and send the organisation-specific registration/supervisor question to the DPC or Ghanaian counsel rather than resolving it by guesswork.
4. **Notice and rights.** Sections 23, 27(2), 32–35, and 39–44 inform the evidence check for notice, access, correction, objection/prevention, direct-marketing objection, automated decision rights, and compensation. The DPC's [individual-rights page](https://dpc.gov.gh/for-individuals/) is regulator guidance that can help map the rights workflow. Verify the actual identity-proof, intake, authentication, response, correction, deletion/erasure, export, objection, and appeal paths.
5. **Security and processors.** Sections 28–30 require reasonable technical and organisational safeguards, processor confidentiality, and a written controller–processor contract with security measures. Inventory each SDK/vendor, the data it receives, the country it sends to, subprocessors, retention, access roles, breach obligations, and deletion/return behavior. A vendor's marketing page is not evidence of a signed DPA or a configured control.
6. **Security compromises.** Section 31 requires notification to the Commission and the affected data subject when there are reasonable grounds to believe personal data was accessed or acquired by an unauthorised person, as soon as reasonably practicable after discovery, subject to the Act's investigation-delay rule. Build an incident clock, evidence-preservation path, DPC contact route, affected-user communication, restoration plan, and country/sector overlay. The [DPC breach form and documents page](https://dpc.gov.gh/documents/) and [DPC contact page](https://dpc.gov.gh/contact/) are operational sources; do not replace the statutory analysis with a generic “72 hours” rule.
7. **Direct marketing.** Section 40 requires prior written consent for direct marketing and gives the data subject an objection route. Build purpose-specific consent, proof of consent, withdrawal, suppression, and an unsubscribe mechanism. Do not treat a pre-checked “updates” box, a bundled terms checkbox, or a transactional message as marketing consent without an evidence-based classification.
8. **Automated decisions and AI.** Section 41 addresses decisions significantly affecting an individual that are based solely on automated processing. Identify AI/model calls, prompts, training or retention, profiling, scoring, moderation, eligibility, fraud decisions, human review, explanations, appeals, and vendor geography. A claim that “Ghana requires one sentence saying AI is used” is not established by this research; disclose AI where the actual flow and applicable law, contract, platform rule, or fair-dealing expectation requires it, and escalate consequential automated decisions.
9. **High-risk processing.** The DPC's [compliance guidance](https://dpc.gov.gh/compliance/) and [self-assessment tool](https://dpc.gov.gh/self-assessment-compliance-tool/) ask about DPIAs/high-risk processing, security, consent records, cookie notices, withdrawal, breach response, and rights. Treat these as regulator guidance and evidence prompts, not a substitute for the Act. Flag AI, profiling, facial recognition, health, biometrics, children, precise location, large-scale monitoring, and public-facing sensitive-data flows for a documented risk/DPIA review.

### 2.2 Cookies, pixels, analytics, and consent

Do not invent a Ghana “cookie law” or import EU consent language as if it were Ghana legislation.

- The DPC self-assessment asks whether a website uses cookies, has an updated cookie notice, records consent, and provides withdrawal. Use those as Ghana regulator-facing implementation checks.
- The DPC publishes a separate [Cookie Policy (EU)](https://dpc.gov.gh/cookie-policy-eu/) that expressly applies to EEA and Swiss residents. It is evidence that the DPC distinguishes jurisdictions, not proof that every Ghana website has an EU-style statutory cookie rule.
- Inventory first-party cookies, local storage, SDK pixels, session replay, fingerprinting, reCAPTCHA, embedded media, fonts, maps, chat, ad tags, and server-side analytics. Record purpose, identifier, data, destination, retention, and whether the feature works without the optional technology.
- Keep strictly necessary security/session functionality separate from analytics, personalisation, advertising, replay, and cross-site tracking. Gate non-essential processing where consent is the chosen or required basis; make decline and later withdrawal as easy as accept; record version, timestamp, scope, region, and policy link.
- If the app targets the EEA, UK, Switzerland, South Africa, Kenya, Nigeria, Rwanda, or another country with different cookie/marketing rules, run that country adapter as well. Do not claim the Ghana baseline covers it.

### 2.3 Ghana electronic commerce, pricing, refunds, and business identity

**Primary anchor:** [Electronic Transactions Act, 2008 (Act 772), current official ORC text](https://orc.gov.gh/wp-content/uploads/2025/08/Electronic_Transactions_Act_no_772_2008.pdf), as amended by Act 838 and the Cybersecurity Act 2020 where shown in the text.

If the product offers goods or services through an electronic platform, inspect sections 46–54:

- **Section 47 supplier information:** expose and verify the full name and legal status, physical address and telephone, website and email, applicable self-regulatory body/code, registration details for a legal person, product/service characteristics, payment method, terms, fulfilment timing, transaction-record access, return/exchange/refund policy, dispute-resolution code where applicable, security/privacy policy, recurring-term duration where applicable, and consumer rights.
- **Total price and fees:** section 47(h) calls for the full price including transport, taxes, and other fees/costs. Render mandatory charges before commitment; do not bury them in a later step, surprise invoice, dark pattern, or currency conversion.
- **Performance and unavailable service:** section 48 includes a fourteen-day default for execution unless agreed otherwise and a seven-day refund rule where an unavailable order cannot be performed. Match the actual product and contract; do not paste those periods into every digital subscription without checking the statutory exceptions and facts.
- **Grace period and exceptions:** section 49 provides cancellation periods for certain goods/services and lists exceptions, including certain financial services, services begun with consent before the grace period ends, customised/perishable goods, unsealed software/media, gaming/lottery, and time-specific accommodation/transport/catering/leisure. Route the actual offer to Ghana consumer counsel before promising a blanket refund or no-refund rule.
- **Unsolicited communications:** section 50 requires prior consent except for the stated communications-provider notice exception, requires an option to cancel the mailing list, and requires source-identification information on request. The product must implement suppression, unsubscribe, and audit logs; not merely put an email address in a footer.
- **Non-exclusion:** section 54 means terms should not purport to remove consumer rights provided by the Act. Arbitration, liability caps, auto-renewal, “all sales final,” and class-action language require facts, enforceability, and Ghana counsel—not a copied U.S. clause.

### 2.4 SMS, calls, email, and direct marketing

Use two distinct checks:

1. **Data-protection purpose check:** Act 843 section 40 and the DPC rights page for direct-marketing consent/objection.
2. **Communications-channel check:** the [NCA FAQ](https://nca.org.gh/faqs/) and [NCA management notice](https://nca.org.gh/2021/08/06/management-of-unwanted-calls-and-text-messages/) state that Ghana's 2014 unsolicited-electronic-communications guidelines were withdrawn effective 1 August 2021, and direct providers to Act 772 section 50. The FAQ describes consumer controls for promotional SMS/calls, including `STOP` and no-cost opt-out; verify the current provider/channel implementation and applicability rather than copying a telecom rule to ordinary email.

For each campaign, prove: who consented, to what channel, for which sender/purpose, when, from which source, which sender identity is shown, how `STOP`/unsubscribe works, whether transactional and marketing traffic are separated, and how suppression propagates to every vendor and backup queue. The NCA's [2026 A2P public consultation](https://nca.org.gh/2026/03/12/public-consultation-on-regulatory-framework-for-the-management-monitoring-and-monetisation-of-international-application-to-person-a2p-messaging-traffic-in-ghana/) is a watch item, not a current obligation; do not treat a consultation as enacted law.

### 2.5 Cybersecurity, incidents, critical infrastructure, and security services

**Primary anchor:** [Cybersecurity Act, 2020 (Act 1038)](https://www.cybersecurity.gov.gh/documents/Cybersecurity%20Act%202020%20%28Act%201038%29.pdf) and the [Cyber Security Authority](https://csa.gov.gh/).

- **Incident reporting:** section 47(5) says a person in charge of an institution must report a cybersecurity incident to the relevant Sectoral CERT or National CERT within not more than twenty-four hours after detection. Classify the product, entity, sector, and institution scope before declaring a universal app SLA. This is not permission to wait: maintain an immediate internal triage path, preserve evidence, and escalate to the CSA/legal owner.
- **Critical information infrastructure:** sections 35–40 and the [CSA CII page](https://csa.gov.gh/cii.php) concern designated CII, with Ghana identifying thirteen sectors. The [CII Directive](https://www.csa.gov.gh/resources/Directive_CII.pdf) requires designated CII owners to report incidents within twenty-four hours and disclose identified vulnerabilities within seventy-two hours. Do not apply CII obligations to an ordinary SaaS app unless designation or sector facts support it.
- **Children online:** sections 62–67 address criminal online child-abuse offences. For an app used by children or hosting user content, implement child-safety, reporting, takedown, moderation, escalation, evidence preservation, and abuse-prevention controls; this is separate from a privacy checkbox.
- **Cybersecurity-service licensing:** the CSA's [licensing and accreditation page](https://csa.gov.gh/licensing-and-accreditation) and [FAQ](https://csa.gov.gh/licensing-and-accreditation-faq) describe licensing for services such as vulnerability assessment/penetration testing, digital forensics, managed cybersecurity, GRC, and cybersecurity training. Do not tell an ordinary product company that it needs a cybersecurity-service licence merely because it has security features; do check licensing if the business sells those services for reward.
- **Security baseline:** regardless of sector, inspect secrets, authentication, server-side authorization, tenant isolation/RLS, rate limits, abuse controls, upload handling, XSS/CSRF, session cookies, password reset, webhook signatures/idempotency, encryption, backups, recovery, log redaction, dependency provenance, and monitoring. Ghana law does not make a vendor name or a checklist proof of security.

### 2.6 Payments, mobile money, tax, and entity identity

- **Payments:** [Bank of Ghana's Payment Systems and Services Act, 2019 (Act 987)](https://www.bog.gov.gh/wp-content/uploads/2022/03/Payment-Systems-and-Services-Act-2019-Act-987_.pdf) and [licence categories](https://www.bog.gov.gh/fintech-innovation/licence-categories/) require a product classification. Ask whether the app operates a payment system, transfers/aggregates funds, issues stored value, provides digital credit, or only uses a licensed PSP. Do not call the app or vendor “BoG licensed” without a verified licence and exact scope. Review MoMo/payment data, settlement, chargebacks, fraud, webhook verification, reconciliation, refunds, support, and provider/subprocessor terms.
- **Tax:** [GRA e-commerce guidance](https://gra.gov.gh/file-and-pay-taxes/e-commerce/) says non-resident suppliers of electronic services for use/enjoyment in Ghana may have VAT obligations under the VAT Act 2013 (Act 870); [GRA tax registration](https://gra.gov.gh/domestic-tax/tax-registration/) and [corporate income-tax guidance](https://gra.gov.gh/domestic-tax/tax-types/corporate-income-tax/) route business/tax registration questions. Treat rates, residence, permanent establishment, invoicing, VAT, withholding, digital-service, and merchant-of-record treatment as facts for a Ghana tax professional—not as generic policy wording.
- **Entity and public details:** use the [Office of the Registrar of Companies entity search](https://www.orc.gov.gh/service-entity-information-search.php) and the project's real records to verify the legal contracting party, registration number, office/address, beneficial ownership/representatives, support contact, and authority to sell. Never invent a Ghana address, registration, tax number, DPC certificate, BoG licence, or regulator contact.
- **Commercial display:** if a Ghana electronic transaction is in scope, show the actual price/currency, mandatory taxes/fees, payment method, recurring term, delivery/access timing, transaction record, return/refund rules, and security/privacy links before commitment. Local payment rails and a Ghanaian audience are product facts to inspect, not automatic proof of licensing.

## 3. Children, age assurance, and vulnerable users

The user request to “get age consent” is a trigger to stop and inspect, not a reason to copy COPPA or GDPR language.

1. Determine whether children are targeted, likely to use the service, visible in the data, or able to upload content. Check marketing, onboarding, app-store age rating, school/parent flows, UGC, support, and analytics.
2. Do not import a universal age threshold. This research did not establish a single current Ghana Act 843 age/parental-consent threshold for every service. Record the threshold as `unknown/needs counsel` until DPC guidance and the relevant product facts establish it. Ghana's [draft Data Protection Bill](https://moc.gov.gh/wp-content/uploads/2023/03/DATA-PROTECTION-BILL.pdf) is a draft and must not be presented as current law.
3. Until the strategy is approved, minimise child data, do not run behavioural advertising or session replay on children by default, avoid unnecessary precise location/biometrics, separate parent and child accounts, protect parent verification, and provide an age-appropriate notice and rights/support route.
4. Add parental/guardian consent only where the applicable law and product risk call for it; make it verifiable, revocable, auditable, and separate from general terms/marketing consent. A typed birth date is not automatically reliable age assurance.
5. Add abuse prevention and reporting. Child online safety under the Ghana Cybersecurity Act is not satisfied by privacy notice language. For UGC, define reporting, urgent escalation, lawful preservation, takedown, appeals, and trusted contact paths.

## 4. African regional layer: use it as a router, not a substitute for national law

| Layer | Current source/status | Required agent behavior |
| --- | --- | --- |
| African Union Data Policy Framework | [AU Data Policy Framework](https://au.int/en/documents/20220728/au-data-policy-framework), adopted 28 July 2022; policy framework, not one directly applicable pan-African privacy statute | Use for interoperability/data-governance context; do not claim compliance from it |
| AU Malabo Convention | [AU Convention on Cyber Security and Personal Data Protection](https://au.int/en/treaties/african-union-convention-cyber-security-and-personal-data-protection), adopted 27 June 2014; ratification/accession and implementation vary by state; use the [current AU status list](https://au.int/sites/default/files/treaties/29560-sl-AFRICAN_UNION_CONVENTION_ON_CYBER_SECURITY_AND_PERSONAL_DATA_PROTECTION_0.pdf) | Check the actual country's status and implementing law; never say “Malabo applies to Africa” without that check |
| ECOWAS | [ECOWAS legal instruments](https://www.ecowas.int/publication/directorate-of-digital-economy-and-post-technology-legal-instruments/) and [Supplementary Act A/SA.1/01/10 on Personal Data Protection](https://www.ecodob.ecowas.int/legal_texts/journal_en/SIGNED_Data_Protection_Act.pdf); ECOWAS also lists electronic-transactions, cybersecurity, and critical-infrastructure instruments | Ghana is an ECOWAS context, but national Ghana Acts and regulators remain the primary implementation check. The 2024 revision workshop is a watch item, not a replacement for the current text |
| AfCFTA/digital trade | Use AU/ECOWAS sources only for the specific issue and current status | Do not turn trade-policy language into a privacy, refund, tax, or security conclusion |

For every regional source, record: instrument type, adoption/effective date, state status, implementing statute/regulator, product sector, and whether counsel says it changes the result. Regional harmonisation does not erase country-level registration, tax, payment, child, telecom, or consumer rules.

## 5. Country adapters to load when users or operations extend beyond Ghana

These are representative high-value adapters, not an exhaustive list of Africa. For every additional country, research its current official authority and law before publishing a country-specific artifact.

### Nigeria

- Start with the [Nigeria Data Protection Commission NDP Act 2023 page](https://www.ndpc.gov.ng/ndp-act-2023/) and [NDPC FAQs](https://ndpc.gov.ng/faqs/).
- Check controller/processor classification, registration/designation, data-subject rights, breach process, children/sensitive data, cross-border transfers, representative/extraterritorial reach, sector rules, and current NDPC guidance.
- The NDPC FAQ describes cross-border transfer provisions and adequacy/safeguard questions. Do not use a draft [cross-border guidance document](https://www.ndpc.gov.ng/Files/NDP-GAID-DRAFT.pdf) as enacted law.
- Do not substitute Nigeria's NDPA for Ghana Act 843. Produce separate notices, contracts, retention/rights workflows, and transfer records where the actual obligations differ.

### Kenya

- Start with the [Office of the Data Protection Commissioner FAQ](https://www.odpc.go.ke/faqs/), the [registration portal](https://dataportal.odpc.go.ke/Account/Register), and the [Data Protection (General) Regulations, 2021](https://www.odpc.go.ke/wp-content/uploads/2024/03/THE-DATA-PROTECTION-GENERAL-REGULATIONS-2021-1.pdf).
- Check the Data Protection Act 2019 and 2021 Regulations for registration, extraterritorial processing, sensitive data, children, data-subject rights, transfer safeguards/consent, processor contracts, and the actual data-location/vendor inventory.
- The registration portal's transfer-jurisdiction, data-location, and safeguard questions are operational evidence prompts, not proof that every app has the same registration category.

### Rwanda

- Start with the [DPO general provisions](https://dpo.gov.rw/dpp-law/general-provisions), [processing and quality rules](https://dpo.gov.rw/dpp-law/processing-and-quality-of-personal-data), [official law PDF](https://dpo.gov.rw/fileadmin/DPO/Law_relating_to_the_protection_of_personal_data_and_privacy.pdf), and [DPO FAQs](https://dpo.gov.rw/faqs).
- Check Law No. 058/2021 for territorial reach, controller/processor contracts, consent, children, sensitive data, DPO/registration, storage outside Rwanda, transfers, direct marketing, sector rules, and supervisory authorisation.
- The DPO sources describe protections including parental-responsibility consent for a child under 16 and transfer/storage questions. Verify the exact provision and current implementation for the actual product; never transport the Rwanda threshold into Ghana.

### South Africa

- Start with the official [Information Regulator overview](https://inforegulator.org.za/about/), [POPIA resources](https://inforegulator.org.za/popia/), [Chapter 8 direct-marketing/automated-decision resources](https://inforegulator.org.za/knowledge-base/category/popia/chapter-8-rights-of-data-subjects-regarding-direct-marketing-by-means-of-unsolicited-electronic-communications-directories-and-automated-decision-making/), and [eServices](https://eservices.inforegulator.org.za/services.aspx).
- Check POPIA Act 4 of 2013 for responsible-party/operator roles, information-officer registration, lawful-processing conditions, prior authorisation for relevant special/child processing, direct marketing by electronic communication, automated decisions, security compromises, and cross-border safeguards.
- South Africa's Information Regulator and POPIA are not an Africa-wide authority. Do not merge POPIA language into a Ghana notice without a data-flow and audience mapping.

### Any other African country

Create an adapter before making a legal claim:

1. Identify the national data-protection authority, primary statute, commencement/amendment status, official regulations, breach/transfer/children/marketing rules, and sector regulators.
2. Check whether the law is territorial, extraterritorial, based on targeting, based on establishment, or based on local equipment/processing.
3. Verify regulator registration/licensing, DPO/information-officer roles, transfer mechanism, incident deadline, rights route, direct marketing channel, child threshold, consumer/refund requirements, tax, payments, telecom/USSD/SMS, and accessibility obligations.
4. Record the source URL and date in the repository evidence ledger. If the source is a bill, draft, consultation, FAQ, policy, or vendor page, label it exactly and do not implement it as binding law.

## 6. Ghana/Africa-specific implementation and security review

These are engineering issue spots, not legal conclusions. They should be added to the same context-first data-flow and threat model used by the rest of the skill:

- **Phone and mobile-money risk:** treat phone numbers, OTPs, SIM-linked identity, mobile-money identifiers, and payment references as sensitive operational data. Test SIM-swap/account-recovery abuse, OTP replay, rate limits, step-up authentication for payment or account changes, webhook signatures/idempotency, settlement reconciliation, and redacted SMS/logs.
- **Shared devices and intermittent connectivity:** test logout, token revocation, session expiration, refresh-token storage, offline queues, duplicate submissions, retry/idempotency, and local storage on shared phones/cybercafé-like environments. Do not leave private data or tokens in URLs, notifications, analytics, or device caches.
- **Low-bandwidth and accessibility:** measure meaningful flows on slow networks and small screens, preserve keyboard access and screen-reader labels, use sufficient contrast, avoid color-only status, keep consent/refund/complaint paths usable, and provide text alternatives. Treat WCAG as an engineering benchmark unless the target country's law or contract establishes a different requirement.
- **Local support and escalation:** show the real Ghana business identity, support channel, privacy/rights contact, breach route, refund path, and child-safety/reporting path. Do not publish fake regulator badges, DPC/BoG/CSA certificates, or a Ghana address that the evidence does not prove.
- **Third-party and AI transfers:** map every destination and subprocessor, including analytics, replay, crash reporting, email/SMS, cloud storage, payment, CDN/WAF, fonts, maps, CAPTCHA, and AI models. Record purpose, data, country, retention, training/use, contract, consent gate, deletion, and fallback. “Hosted in Africa” is not a transfer analysis; “hosted in the U.S.” is not automatically prohibited.
- **Claims and dark patterns:** remove unsupported security/legal claims, fake reviews, fabricated user counts, false “licensed/approved” badges, hidden fees, preselected marketing consent, obstructive decline paths, and “no refund” language that conflicts with applicable consumer rights. Preserve evidence for every public claim.
- **UGC and child safety:** do not use a DMCA agent or U.S. safe-harbour clause as a universal African shield. Map Ghana Act 772 intermediary/takedown issues and the actual countries, copyright laws, moderation model, reporting channel, and escalation owner with counsel.

## 7. Required output for a Ghana/Africa run

The agent must leave or return these sections, tied to actual evidence:

1. **Scope:** repository/runtime inspected, user journey, authorized environment, countries, entity, audience, sectors, and commercial model.
2. **Ghana matrix:** Act 843, Act 772, CSA/Act 1038, CII status, NCA channel, BoG payment, GRA tax, ORC/entity, children, and accessibility findings with source type and section.
3. **Country matrix:** one row per actual country, regulator, current law, effective date, transfer/children/marketing/consumer/payment triggers, and missing evidence.
4. **Data-flow register:** source → field → purpose → storage → vendor/subprocessor → country → retention → deletion → user right → security control.
5. **Artifact crosswalk:** each privacy-policy, cookie, terms, refund, consent, deletion, email, accessibility, AI, UGC, and payment statement mapped to implementation evidence or a visible placeholder/owner.
6. **Security findings:** affected file/route/schema/vendor/config, abuse path, severity/confidence, remediation, negative test, and residual risk.
7. **Open decisions:** DPC/CSA/BoG/GRA/NCA/counsel/business-owner questions, draft/consultation items, and runtime paths not verified.

Do not return “compliant in Africa” or claim “fully legal,” “hack-proof,” “FTC safe,” or “store approved.” Return the narrower statement the evidence supports, such as “Ghana Act 843 registration and breach-workflow evidence is incomplete” or “Kenya transfer safeguards are not verified for the identified analytics vendor.”

## 8. Standalone context-first prompt

Use this prompt when an AI coding agent is asked to perform the Ghana/Africa review:

```text
Run a Ghana-first, Africa-aware legal and security review of the actual application in this repository. Do not draft generic policies and do not claim “Africa compliance.”

First inspect the repository instructions, changelog, manifests/lockfiles, routes, forms, server/API handlers, auth/session code, authorization/RLS/storage rules, schemas, uploads, webhooks, emails/SMS, cookies/local storage, analytics/replay, AI/model calls, payment code, deletion/retention jobs, logs, deployment config, claims/marketing copy, accessibility implementation, and tests. If an authorized staging/runtime target exists, use only synthetic data and low-volume checks. If it does not exist, mark runtime behavior not verified.

Build an evidence ledger with observed, provided, assumed, unknown, needs counsel, and not verified labels. Build a jurisdiction matrix for: operating entity, Ghana presence, target countries, data-subject locations, hosting/vendor countries, payment providers, sectors, children, sensitive data, UGC, AI, and distribution channels.

If Ghana is in scope, check the current official sources for Act 843 (data-protection principles, registration, notice, minimality, security, processors, breach notification, rights, direct marketing, automated decisions), Act 772 (business identity, total price/fees, terms, delivery, refund/return, transaction records, consent/unsubscribe), Cybersecurity Act 1038/CSA (incident, CII, child-online safety, security-service licensing), NCA marketing-channel guidance, BoG payment licensing, GRA tax routing, and ORC entity details. Label statute, regulator guidance, policy, consultation, draft bill, and framework separately.

If any other African country is in scope, load a country adapter from its current official regulator/statute. Do not assume Ghana, ECOWAS, the AU Malabo Convention, the AU Data Policy Framework, GDPR, COPPA, U.S. DMCA, or an App Store rule applies everywhere. Check territorial reach, registration/licensing, cross-border transfers, breach clocks, children, marketing, consumer/refund, tax, payments, telecom, accessibility, and sector rules per country.

Then produce: (1) context snapshot; (2) Ghana matrix; (3) country matrix; (4) data-flow/vendor/transfer register; (5) artifact-to-code crosswalk; (6) prioritized legal/security findings with exact locations; (7) minimal safe implementation changes and negative tests; (8) missing facts and counsel/owner decisions; (9) verification commands and runtime gaps. Do not invent entity details, DPC/BoG/CSA registration, prices, tax rates, retention periods, child ages, vendors, legal bases, or certificates. Do not publish a policy or claim compliance when material facts are unknown.
```

## 9. Source register and freshness rules

Use official sources first and keep the URL/date in the evidence ledger. The following sources were checked for this reference on 2026-10-13:

- [Ghana Data Protection Commission](https://dpc.gov.gh/), [organisations](https://dpc.gov.gh/for-organisations/), [compliance](https://dpc.gov.gh/compliance/), [individuals](https://dpc.gov.gh/for-individuals/), [self-assessment](https://dpc.gov.gh/self-assessment-compliance-tool/), [documents/breach form](https://dpc.gov.gh/documents/), [contact/breach reporting](https://dpc.gov.gh/contact/).
- [Ghana Data Protection Act 2012 official PDF](https://cybersecurity.gov.gh/documents/Data_Protection_Act_2012.pdf) and [GhaLII text](https://ghalii.org/akn/gh/act/2012/843/eng%402012-05-18).
- [Ghana Electronic Transactions Act 2008 official ORC text](https://orc.gov.gh/wp-content/uploads/2025/08/Electronic_Transactions_Act_no_772_2008.pdf), [NCA regulatory framework](https://nca.org.gh/regulatory-framework/), [NCA FAQ](https://nca.org.gh/faqs/), [NCA unwanted-calls notice](https://nca.org.gh/2021/08/06/management-of-unwanted-calls-and-text-messages/), and [NCA A2P consultation](https://nca.org.gh/2026/03/12/public-consultation-on-regulatory-framework-for-the-management-monitoring-and-monetisation-of-international-application-to-person-a2p-messaging-traffic-in-ghana/).
- [Ghana Cybersecurity Act 2020 official PDF](https://www.cybersecurity.gov.gh/documents/Cybersecurity%20Act%202020%20%28Act%201038%29.pdf), [CSA CII page](https://csa.gov.gh/cii.php), [CII Directive](https://www.csa.gov.gh/resources/Directive_CII.pdf), and [CSA licensing](https://csa.gov.gh/licensing-and-accreditation).
- [Bank of Ghana Act 987](https://www.bog.gov.gh/wp-content/uploads/2022/03/Payment-Systems-and-Services-Act-2019-Act-987_.pdf), [BoG licence categories](https://www.bog.gov.gh/fintech-innovation/licence-categories/), [GRA e-commerce](https://gra.gov.gh/file-and-pay-taxes/e-commerce/), [GRA tax registration](https://gra.gov.gh/domestic-tax/tax-registration/), and [ORC entity search](https://www.orc.gov.gh/service-entity-information-search.php).
- [AU Data Policy Framework](https://au.int/en/documents/20220728/au-data-policy-framework), [AU Malabo Convention](https://au.int/en/treaties/african-union-convention-cyber-security-and-personal-data-protection), [AU treaty-status list](https://au.int/sites/default/files/treaties/29560-sl-AFRICAN_UNION_CONVENTION_ON_CYBER_SECURITY_AND_PERSONAL_DATA_PROTECTION_0.pdf), [ECOWAS legal instruments](https://www.ecowas.int/publication/directorate-of-digital-economy-and-post-technology-legal-instruments/), and [ECOWAS Data Protection Act](https://www.ecodob.ecowas.int/legal_texts/journal_en/SIGNED_Data_Protection_Act.pdf).
- [Nigeria NDPC Act page](https://www.ndpc.gov.ng/ndp-act-2023/), [Kenya ODPC](https://www.odpc.go.ke/faqs/), [Kenya Regulations](https://www.odpc.go.ke/wp-content/uploads/2024/03/THE-DATA-PROTECTION-GENERAL-REGULATIONS-2021-1.pdf), [Rwanda DPO](https://dpo.gov.rw/dpp-law/general-provisions), and [South Africa Information Regulator](https://inforegulator.org.za/about/).

Re-check any source that is labeled current, especially regulator guidance, licence categories, consultations, draft bills, fees, tax guidance, app-store rules, and vendor behavior. Record changed dates and append the reason for any rule update to `changelog.md`.
