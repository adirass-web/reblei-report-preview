from pathlib import Path
p=Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/qa-litigation.md')
s=p.read_text(encoding='utf-8-sig')
s=s.replace('This is a source-level review; a final parent report/claims draft and forthcoming Nasdaq AWC were not available for this review.','Initial source review was followed by the closing review below of the parent report/claims and the newly preserved original Nasdaq Wedbush AWC.')
start=s.find('## Remaining review')
if start>=0:s=s[:start]
s+='''## Closing review: original Wedbush AWC and parent draft

The original 12-physical-page Nasdaq AWC, `litigation/raw/nasdaq-wedbush-20100243866-02.pdf`, has now been reviewed. Complete specified pages 1, 3-4, 8-9 were extracted, rendered and visually inspected; additional payment/signature/procedural pages were read for limits. The AWC is now reviewed rather than merely a forthcoming candidate.

| Fact | Original locator | QA result |
|---|---|---|
| Acceptance | Physical p1, dated notice and acceptance sentence | Accepted February 25, 2016. This is not automatically the sanctions-effective date. |
| Respondent identifier | Physical p3, caption | Wedbush Securities Inc., CRD 877. The AWC also records its earlier Wedbush Morgan Securities Inc. name. |
| Settlement character | Physical p3, I.A | Consent without admitting or denying findings, prior to a hearing and without adjudication of an issue of law or fact. These limits apply to the adopted settlement findings; do not describe them as admissions or a contested merits judgment. |
| Scout relationship | Physical p4, opening paragraph | Explicitly names Scout Trading, LLC and says Wedbush served as its clearing firm. This is stronger than the firm report's holds-firm-assets description. It does not supply Scout's CRD or Bleich's name. |
| Censure/fine | Physical p8, I.B | Censure and $675,000 fine payable jointly to Nasdaq and FINRA; $337,500 shall be paid to Nasdaq. This is a shared total, not two separate $675,000 fines. Not a personal sanction against Bleich. |
| Undertaking | Physical p8, I.B | Revise written supervisory procedures; within 60 business days of acceptance, a registered principal must submit a signed/dated letter or qualifying work email representing revision and stating implementation date. The AWC and notice require completion notification; neither proves actual revision, submission or completion. |
| Effective date | Physical p9, opening sentence | Sanctions effective on a date set by FINRA staff. That date is not specified in the reviewed source and must remain unestablished. |
| Payment | Physical p8 and payment-election sheet physical p12 | Agreement/intention to pay, not proof of payment. The payment-election form is not a receipt or satisfaction record. |

The parent `litigation/report.md` and `litigation/claims.json` were read in full. All prior material award corrections are adopted: database/service/signature dates distinguished; legal interest boundary left unresolved; pleaded causes separated from the unexplained damages theory; exact requested amount discrepancy preserved; attorneys' fees denied; hearing fees separated; no collection/payment or exoneration inference; and firm linkage explicitly labeled probable rather than a CRD match. The new AWC supports the same Wedbush regulatory event and should not be counted as another fine.

Two final wording refinements were sent to the parent: replace claim LIT3-C12's shorthand paid jointly with payable jointly, and include the AWC's consent-without-admission/no-adjudication limit directly in the report rather than only claim LIT3-C11. The report should also specify the undertaking's 60-business-day deadline and explicitly state the unknown sanctions-effective date. These are precision/completeness refinements; the underlying verified facts and stated payment/completion limits already prevent promotion of an obligation into completed performance.

No substantive contradiction between the reviewed AWC and the bounded parent outcome was found. No other worker files were changed. This review does not extend to the parent native-search logs, later court records or proof of compliance/collection not supplied.
'''
p.write_text(s,encoding='utf-8')
print('QA updated; only owned QA file edited.')
