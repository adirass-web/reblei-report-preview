# Round 4 normalized index: independent QA

Reviewed November 4, 2026. Result: **PASS for the normalized index and the checks below. No material integration defect found.**

Scope: final evidence-index.json, read-only evidence-index.sqlite, schema.sql, work/build_continuation.py, round-4 source/claim packets and the registration/withdrawal QA note. This review writes only this note. No web search, NYSCEF access, source-original change or Git operation was performed. This is an index/provenance review; it does not independently repeat every specialist interpretation or every underlying bulk-table scan.

## Structural and preservation checks

- SQLite `PRAGMA integrity_check` returned `ok`; `PRAGMA foreign_key_check` returned no rows.
- Counts independently queried: 45 subjects, 8 persons, 37 entities, 396 documents, 247 claims, 67 financial observations, 9 events and 342 search logs.
- All 17 JSON table arrays equal their SQLite table rows semantically, including numeric values. SQLite REAL affinity renders some ownership integers as floats; that is a representation difference, not a data disagreement.
- Every one of the 396 indexed document paths exists and its bytes match the indexed SHA256.
- Every claim has at least one claim_evidence link. No blank/null locator and no blank/null document source classification was found. All claim/document/subject references satisfy the schema foreign keys.
- All 33 round-4 statements are preserved verbatim from their packets: 11 EP5, 8 EMP5, 9 CORP5 and 5 LIT5 claims. Original records, target extracts, researcher scan/search logs, failed/challenged access responses and unjoined discovery candidates retain distinct source classifications. A link to a search response is not represented as an original case record.

## Event and filing interpretation

The three added events are `administrative_adviser_withdrawal_filing`, with null respondent, claimant, fine, currency and resolution date. Event-to-claim-to-subject joins resolve exactly as follows:

| Event | Claim | Subject | Filing date |
| --- | --- | --- | --- |
| EP5-W01 | EP5-C004 | E003 EntryPoint | 2021-12-10 |
| EP5-W02 | EP5-C005 | E002 Ophir | 2017-06-29 |
| EP5-W03 | EP5-C006 | E021 Inferent | 2020-03-21 |

Their notes identify the dates as filing dates, preserve source-specific business-cessation/signature distinctions and explicitly reject disciplinary/personal-sanction attribution. The remaining six events comprise five firm regulatory events and one firm arbitration award. No new case event was created from the excluded litigation candidates or the overlapping ERA/IA exports.

EP5-C001/C003 and EMP5-C02/C04 preserve FilingID1869875 as the same filing appearing in both source families, with the dual final-ERA/initial-SEC flags explained as a procedural inference. The index does not count two registrations or two events from those appearances. Preserved original source representations/aliases may coexist without implying independent filings. EMP5-C02 likewise labels FilingID663868 overlap and retains the distinction between raw rows, identical-field disclosures and unique FilingIDs.

## Subject links and safeguards

EP5 claims resolve to EntryPoint E003, Ophir E002 or Inferent E021 as appropriate. EMP5-C01-C04/C07/C08 resolve to professional subject P001; the conditional Inferent disclosure/no-match claims EMP5-C05/C06 resolve to E021. CORP5-C001-C006 resolve to E004 while explicitly retaining the unresolved MEB INC/MEB NY INC ownership-identifier bridge. CORP5-C008 resolves to historical E037 and rejects the GLEIF namesake join. Multi-entity search claims, excluded candidates and general document-access guidance appropriately retain null subjects rather than creating unsupported identity links.

New persons P006-P008 retain exact disclosed professional CRDs. E035-E037 are historical as-filed intermediaries with unresolved corporate registry identity. Their inclusion notes reject name-only registry, bank-licensing and current-ownership conclusions. EP5 relationships retain historical snapshot qualifications and source-specific status fields; effective dates remain unknown rather than converting snapshots into transaction dates. CodeB/C/NA retain bounded bands; CodeE remains a band even when the title says sole member. CodeF trustee ownership fields are null, with no inferred percentage.

The five Inferent W2 observations retain assets 1,261,506, current liabilities 986,536, long-term debt 568,700, equity -293,731 and total liabilities/equity 1,261,505. The USD1 difference is quarantined, measurement dates remain null, and filing date is separately 2020-03-21. Negative equity is not characterized as legal insolvency or personal finance. No P001-to-E021 role exists in the roles table; disclosed overlap for other professionals does not establish Bleich employment.

The five ERA asset observations preserve the specific 2B field, filing dates and unknown measurement dates, without treating those values as personal income, fund allocation or a compliance determination. LIT5 bounded native-search zeros, challenge responses, unjoined opinions and unresolved award follow-up remain access/search limitations, not exoneration or comprehensive absence findings.
