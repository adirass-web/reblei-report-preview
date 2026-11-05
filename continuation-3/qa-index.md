# Independent normalized-index QA, continuation 3

Reviewed November 4, 2026. Snapshot: schema 2, generated **2026-11-04T18:28:16.832449+00:00**. This review checks integration and evidentiary boundaries; it does not claim exhaustive career, regulatory or court coverage. This QA note and, at the parent's explicit follow-up request, the owned EMP4-C08 evidence-locator metadata in continuation-3/employment/claims.json were written. No normalized index, database, original source bytes or Git state was changed by this reviewer.

**Result: passed. No blocking normalization or substantive integration issue found.** One locator-clarity observation was corrected in the owned specialist claim metadata as described below; the parent owns the subsequent rebuild.

## Integrity and agreement

- Independently recomputed SHA-256 for **all 329 indexed document files**. Every hash matches; all resolved files remain within this investigation root.
- Compared every row across **all 17 JSON and SQLite tables**, including parsed nested metadata JSON and duplicate-row counts. Counts and values agree semantically. Equivalent numeric SQLite representation is not treated as a factual discrepancy.
- SQLite read-only `integrity_check` returns `ok`; `foreign_key_check` returns no rows.
- All indexed PDF files with recorded page counts have matching actual physical page counts.
- `validation.json` table counts agree with the reviewed index: 39 subjects, 5 persons, 34 entities, 29 identifiers, 329 documents, 348 document aliases, 214 claims, 347 claim-evidence links, 10 roles, 34 relationships, 57 financial observations, 6 events, 29 event-claim links, 265 search logs, 23 conflicts, 29 conflict-claim links and 382 retrieval attempts.

Reviewed snapshot hashes:

- `evidence-index.json`: `f5d1b18074ec45614163128704450ed70022fa9d02ec0fc9bb67a7542b1ed8d9`
- `evidence-index.sqlite`: `a30a3be1d8dcfef29ead6a19a621672e74f24fcccd8d4de8953b644b97f51e48`

## Ophir names, roles and ownership snapshots

E034 is explicitly an **as-filed MEB INC name placeholder**, separate from E004 MEB NY INC for tracking unresolved source spellings. Its entity type/status/note expressly deny that this normalization establishes a separate incorporated company, a legal rename or equivalence. No unique registry identifier was added to resolve that question. EMP4-X-NAME retains the mixed names in the 2014-2016 paired rows and the unresolved alternatives.

EMP4-L01 points Bleich to the historical MEB INC spelling with unresolved identity status and NULL ownership/effective-date fields. EMP4-L02/L03/L04 retain the March 18 and June 17, 2016 disclosures as **snapshots**: the D/C versus E bands are attached to the named intermediary relationships, while effective_from/effective_to stay NULL. The notes and EMP4-X-OWNERSHIP explicitly preserve that the records do not establish a 2016 transaction date, terms, sale or complete economic exit. No fabricated 2016 effective date was introduced.

R002 retains the reported 2012-04 field with a specific qualification: one acquired-status field in a combined CEO/CCO row does not establish that CCO duties began then. It also states that earlier CEO-only rows precede the combined wording and that CEO cessation is not proved. The historical role claims retain full CRD/FilingID joins rather than replacing them with signatory-title succession.

The new claims link directly to the original SEC bulk ZIP members, the retained target-row derivatives and the original 2017 Ophir PDF. The legend at physical PDF pages 19-20 supports C=25%-less than 50%, D=50%-less than 75%, E=75% or more, and Schedule A NA=less than 5%; those ranges are not converted into exact wealth or cumulative ownership. Original member bytes, CRC/size verification and target row ordinals remain retrievable through document aliases. Separate source QA in `qa-employment.md` verified all nine EMP4 claims and the compressed reconstruction.

**Locator correction completed:** the reviewed snapshot's EMP4-C08 link to the 2017 Ophir PDF inherited a claim-wide CSV/FilingID locator rather than specifying physical page 20. At the parent's explicit request, the owned specialist claim now has five per-source evidence entries. The PDF entry explicitly identifies physical page 20, Schedule B, and limits its corroboration to the March 2017 snapshot. The original Base A and its derivative identify the firm/FilingID/submission-date correlation; the original Schedule A/B and target-row derivative identify the actual historical ownership rows and bounded omission scope for FilingIDs 993846, 1019291 and 1070803. No factual statement, source bytes, claim count or source count changed. The updated specialist claims file SHA-256 is `419c788918a14f35311a934eb81ed70743f6886b0f642850ba927a376804d0bc`; all five references resolve and all nine claims remain. Specialist claims are not an original source in their own manifest, so no original-source checksum entry required modification.

The JSON/SQLite digests above identify the pre-correction 18:28:16 snapshot actually checked by this reviewer. The parent will rebuild the register and verify the changed locators/new generated timestamp; the factual and integrity findings here do not pretend that the subsequent byte hashes are unchanged.

## Corrected EntryPoint fields and unresolved history

Independently read the original historical `ADV_Filing_Types_20111105_20241231.csv` rows for FilingIDs 1542238 and 1869875. The first has Initial SEC Registration Request=Y and the exact Final SEC ERA field blank; the second has **both** Initial SEC Registration Request=Y and Final SEC ERA Report=Y. INF4-C008 and INF4-X-ENTRYPOINT retain that distinction, the exact CRD continuity, the different names/SEC file numbers and the unresolved legal-history explanation. Blank is not normalized as an affirmative final ERA report, and the 2024 dual flags are not silently repaired.

Other corrected conflicts remain source-specific: the Inferent Client/Master wording does not create a new proven entity or Bleich affiliation; the rejected CIK lead is not promoted to an entity identifier; and acquired-status, execution, submission and transaction dates remain distinct.

## Events and monetary boundaries

The event table remains **six records**: five existing firm regulatory events and the separately classified Scout/Wedbush arbitration. No new personal Bleich sanction or duplicated joint fine is added.

EVT-E005 retains the single $675,000 joint FINRA/Nasdaq Wedbush fine, including the $337,500 Nasdaq portion, with sanctions effectiveness, payment and undertaking completion unresolved. The later original AWC enriches that event rather than creating another fine.

LIT3-E001 remains an inferred firm-identity arbitration mapping. Its fine_amount is NULL, Bleich is not made a party, and the note retains the on-or-about claim date, November 18 index/service date, November 16 signatures and unresolved interest-transition date. Award obligations are not treated as collected money. The award, reimbursement and FINRA hearing fees stay separate from regulatory penalties. Nothing in the new historical ownership/role data changes those legal-status limits.

This passed review applies to the specified JSON/SQLite snapshot and current source files. It does not establish unobserved employment intervals, legal corporate succession, transaction dates, payment/compliance completion, absence of other proceedings or exhaustive court clearance. Later Markdown-only navigation changes do not alter these reviewed data digests.

## Parent post-correction check

The register was rebuilt at 2026-11-04T18:33:44.103916+00:00 after the independently requested EMP4-C08 locator refinement. Counts remain329documents,214claims and6events. Its original2017ADV link now explicitly locates physicalpage20 and limits that PDF corroboration toMarch2017; historical2016snapshots retain their originalCSVlocators. All329original/source hashes were rechecked by the builder, with foreign keys and SQLite integrity passing. No substantive finding, source byte, role date, ownership band or event changed.

Final JSON SHA256: b3c9e34c0098dbea1449c3d190ed8d339fb754170ccf49bda20f6cc817ca34b8

Final SQLite SHA256: 6c21ab054431562a31a0becbd8743728ca5f5adf2706d27c8c7995fe1622b0b1
