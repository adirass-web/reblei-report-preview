# Bounded independent review of the consolidated continuation index

Reviewed 2026-11-04T17:30:34.753732+00:00. Snapshot `evidence-index.json` generated 2026-11-04T17:27:58.256383+00:00, SHA-256 `dfad4b2185297474b07a81c7c84b1f62413bcfd56d9b25686a92cfbd34cc4026`. Both JSON and SQLite were read without editing principal data. Later package regeneration requires the parent's final integrity check.

**Result: pass for the checks below. No substantive normalization error found.** This is a bounded index/provenance review, not exhaustive professional or litigation clearance. The reviewer authored the investment-litigation branch, so the semantic correctness of that branch's new Cboe findings requires the separate reciprocal reviewer; checking its normalization here is not independent factual certification of the reviewer's own research.

The snapshot contains 131 documents, 140 document aliases, 149 claims, 178 claim-evidence links, 33 entities, 6 roles, 27 relationships, 50 financial observations, 5 events, 118 search-log rows and 13 conflicts. Counts include source captures/reused presentations and are not numbers of unique filings, people or established subject affiliates.

## Integrity checks

- Every normalized document/claim/subject/person/entity/event/conflict reference resolves. All 140 aliases resolve to a retained canonical document.
- All 131 indexed retained files exist and match their SHA-256 values. This includes transformed captures and retained error responses as classified, not only original filings; a hash does not establish the underlying statement's truth.
- SQLite foreign-key check returned no rows, integrity_check returned ok, and all 17 normalized table contents match JSON field values and counts.
- Case/respondent pairs are unique. The three newly recovered Cboe PDFs support the existing events rather than creating duplicates: there remain four Scout events and one separate Wedbush event.

## Requested attribution and quarantine checks

| Check | Result |
|---|---|
| New Cboe primary orders | New claims attach to existing Scout matters; no duplicate events or new personal-sanction event. |
| Consolidated Cboe date difference | EVT-E003 retains FINRA's June 26, 2013 resolution field and explicitly notes the original July 3 order date. LIT-C002/LIT-C009 and LIT-X001 retain the two date types. Neither date is silently erased. |
| E032 LBHI contract record | Separate debtor entity, distinct from the unresolved legal employer. CONT-R001 labels the P001 join provisional and contains no fabricated effective/employment date or ownership band. EARLY-C003's provisional full-name-without-CRD status and limitations are retained. |
| E033 Finch 2026 | Formation February 24, 2026 retained; excluded from historical 2012 linkage. No ownership/role relationship connects it to the subject or historical Finch. |
| Delaware registry identifiers | IDs 3458887, 3458856, 5142327 and 4688408 remain provisional name/chronology mappings with no proven corporate ownership-ID join. The 2026 Finch ID 10521968 maps to its separate excluded historical candidate. |
| Rejected CIK 1977777 | No normalized identifier assigns it to EP Fund GP or the subject. CORP2-CIK-REJECTION and the explicit conflict preserve the rejected lead and official Cata Labs source. |
| Inferent | E021 and related conditional branch are not promoted to verified Bleich employment/ownership. No Inferent role appears in the roles table. Original-URL extracts retain their lower evidence status; nonappearance of Bleich does not become proof of absence. |
| Wrong-person exclusion | P002 Keith Michael Bleich has no role or relationship linkage, and no event is assigned to him or promoted from him to the subject. |
| Ownership and dates | Source-specific historical percentage bands/edges remain separate. Status-acquisition and signature dates retain their limited date basis. No exact downstream beneficial stake or current cap table is invented. |
| Financial quarantines | The 2024Q3 cover/table anomaly retains separate raw and derived observations. The 2024Q2 NEW HOLDINGS amendment remains nonstandalone. No RAUM, master gross assets, Form D sales, 13F values or personal wealth are combined. |
| Private litigation | The event table contains only the five regulatory firm matters. No personal civil case or unverified Triffin investment nexus is normalized as a subject investment-management event. |

## Scope limits

The independent substantive source review of career/corporate/Inferent is documented in `qa.md` and covers 32 claims and 68 retained-source hash checks after the added Form D reuse. This index review checks their preservation and attribution after normalization. It does not establish complete employment dates, corporate legal identity/ownership links, current good standing, Cayman legal form, Inferent succession or complete native-court/enforcement coverage. No legacy repository root records or ZIP archives were accessed.

Final-generator refresh: repeated all reference/alias, 131-file hash, SQLite integrity/foreign-key, 17-table JSON/SQLite equality and requested identity/event/quarantine checks against the final snapshot identified above. All passed; counts and substantive safeguards are unchanged. No additional research or principal-data edits were performed.
