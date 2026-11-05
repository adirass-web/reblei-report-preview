# Independent supplied-source review

Review date: 2026-11-05. Scope: tasks 1–3, `work/adapter.py`, its generated coverage/dispositions/index, and `scout/dossier.md` / `opeh/dossier.md`. Read the shared contract and source-review package; inspected adapter tests and the adapter/Scout/OPEH author reports. No external research, source mutation, extraction, arithmetic reconstruction, subagents or commits. Only this audit file was written.

## Final verdict after round 1

**Spec: approved. Quality: approved. P2: ADDRESSED.** No unresolved source-review findings.

Reviewed `.superpowers/sdd/supplied-dossiers/adapter-fix-round1.diff` and the appended adapter fix report. The fix uses a conservative whitelist for all twelve mixed entity projections: neutral indexing labels/types, lane-owned source citations/support, and adapter bookkeeping. All operational mixed identifiers are empty; original flags, attribution, confidence, rationale, statement and entity-reference fields are absent. The full accepted original entity remains unchanged in `canonical_record`. The new explicit `indexing_metadata_only` status and scope note correctly explain that labels are not identity joins. Source-owned supporting records preserve the actual in-lane assertions.

Independent rebuilt-object inspection confirmed all twelve variants satisfy those properties, the two reported identifier leaks are gone, the stored generated index equals the current rebuild, acceptance totals are unchanged, and all 8,869 typed edges remain. Read the two new regression tests and implementer's evidence of their initial failures and subsequent **18-test** pass plus input-freeze/deterministic generation verification. No redundant unchanged suite was rerun here. No new breakage was found in the scoped fix. Final portable/browser exclusion of the audit-only `canonical_record` is still for the separate integration review; it is not an outstanding adapter/source-prose issue.

## Initial verdict (superseded)

**Spec: changes requested (one P2). Quality: changes requested for the same source-partition defect; authored narratives approved.** No other material finding.

**P2 — Scoped entity metadata imports identifiers unsupported by its own lane.** `work/adapter.py:178–191` copies the whole mixed canonical entity and narrows only citations/support/source mentions. Consequently `ent-ophir-partners-llc--opeh` retains `identifiers={CRD:164729, SEC:801-77121}` although its operational sources are the OPEH note/composite; those sources name Ophir in the predecessor recital without these regulatory identifiers. `ent-scout--opeh` retains `CRD:151990` although its sole operational source is `doc:1ced6091a1f7f046a64a8099fd2e1a1c1ab0d8406a82775c7af8f94be241104e#section=body`, an EDGAR CSV containing CIK 1474522 / file 008-68420, with no CRD. The CRD/SEC values are supported by Scout sources. `work/build_front.py:105` renders operational fields including these identifiers; stripping `canonical_record` does not remove them. A generic appendix-metadata/scope label does not establish lane support for specific identity attributes. Keep unsupported attributes in the untouched audit-only canonical object, and limit or explicitly qualify the operational projection using lane-specific support. Add a regression check for these actual variants. This does not require altering accepted entities.

## Accepted coverage and implementation checks

- Independent `build_index` inspection found Scout 20 occurrences / 18 documents / 17 findings / 104 calculations; OPEH 21 / 20 / 9 / 25. Acceptance totals are 47 assertions, 26 findings, 129 calculations, 42 links and 40 discrepancies. All have dispositions.
- Exactly six mixed statements are deferred: the two named assertions, three links and one discrepancy. Scoped metadata does not alter those dispositions. Every raw entity mention is retained; verified obligation exports are aliases, not duplicate acceptance records.
- Inspected typed dependency extraction, literal-zero comparison handling, joins, source/archive allocation, citation validation, exact-canonical reconstruction validation and input hashing. No arithmetic is introduced. The three additional event-relation fields (`corrects_event_id`, `superseded_by_event_id`, `economic_event_id`) remain canonical semantic metadata; their target events are present and same-lane, so no current missing-evidence defect was found.
- Read-only narrative scan: Scout 140 record links / 111 distinct IDs; OPEH 88 / 67. No missing ID or wrong-lane target. All 17/9 accepted findings are linked. All 25 OPEH calculation IDs occur. All 31 linked Scout calculation outputs and 25 OPEH outputs were compared with accepted results/statuses; displayed narrative values agree. This was comparison to accepted results, not redoing the existing calculations.
- Scout's mixed-ID links occur only in express deferred scope notices. OPEH mentions the mixed IDs only as literal boundaries. Neither reproduces their combined arguments.
- `git diff --stat 40e77bd1e57c0fce62a3a962d977c05b54724e8a -- corpus analysis` returned no changes. The adapter report documents its 16 passing tests, 56 unchanged repository tests, complete 1,814-file freeze and generation verification. These unchanged suites were not repeated for this review.

## Narrative assessment

Scout preserves the firm respondent / representative signature / personal-liability distinction; consent without admission/adjudication; broader investigation versus applicable membership period; separate quote-case payment statement; historical roles and nonmultipliable ownership bands; named NAYS repayment versus unnamed remaining member; profit versus operating cash; reported stocks versus gross flows; the retained $1 sector residual and mislabeled financing subtotal; dash versus numeric zero; missing flow statements; and conditional installment arithmetic versus actual collections. Secondary biography, later-role, disclosure, Harrison/counsel and same-name theories remain attributed in the appendix, with no public-research claim.

OPEH preserves one collective principal despite two makers and repeated copies; predecessor/guaranty recital versus fresh funding; personal maker capacity without an established regulatory-person bridge; creditor assertions versus court findings; dated interest cutoff versus requested additional-interest start; annual/subannual, boundary, rounding and calendar assumptions; separate cure/election/notice clauses; two null not-testable proposals; and discontinuance/administrative correction versus payment, release, merits award or a current balance. Missing inputs qualify particular conclusions and do not erase supported historical conclusions. No material qualifier loss was found in either authored narrative.

## Original supplied passages independently inspected

These are selective reviewer checks, additional to the accepted all-pages baseline and the authors' broader documented source reading. Hashes below identify `doc:HASH#page=N` (physical PDF page); native text/CSV references use `#section=body`. Stored OCR/native text was read directly; no fresh extraction was generated.

| Source hash | Physical pages / region | Conclusions checked |
|---|---|---|
| `2524a1aa0d26e796c8f742d56093461670e137130e55520fa0c0a14b00e374f3` | 6–9 | 2009 balance, period/loss, aggregate contribution and opening dash, negative cash flow and closing cash. |
| `a07386b67822437b63ed80ce01b01561f385bcbd96a7c63b89e2bc47835cfb78` | 6–7, 9; p.7 image | 2010 balance/income/cash; image resolves OCR's erroneous $1,207,143 to $1,297,143. |
| `cedbcd5bf0c7a6907fc2a5c30dde40f54259bdcfa46ab8db434f3b283050bbb9` | 6–7, 10, 13, 17 | 2011 balance, two Net Income labels, cash/financing mislabel, eleven sector components, subordinate terms/expense, regulatory capital. |
| `fd7fd04a2d463b0b7a6d0996b26d4a67bfcc52c8cc6ed20488ab06bca77492c5` | 5–6, 9 | 2012 balance, Finch reorganization/business scope, $9m debt and note interest. |
| `2b95a042ab5e1201576f72dd6c78bbbe91f21402768475d15f1868f160e9e7b9` | 6, 11–12 | 2013 balance, $4m note, $5m NAYS repayment/unquantified interest, demand member advance, $446,291 parent sharing. |
| `98d9acb711bf01f2dd8ad0c491087d5bb57dd9c46bfba52cdc5f8cd346994716` | 6, 8–9, 11, 16, 24 | Exact CRD, direct/indirect capacities and bands, historical registration, disclosure matrix, narrow $10k payment statement. |
| `578da5a59d1762f4ecb4b30c3a25f878e26899dc4dfeff5894d922c8b9790660` | 3, 19–20 | Selected eligibility item, historical CEO/CCO, exact CRD, Schedule A/B bands and DRP wording. |
| `1a1ba19f78c6b68b5956b5dc5feecfda6a8164db7a2c5f8162475d1ca77a4430` | 1, 3–7, 9–11 | Acceptance, firm/consent scope, periods, Rule 204 activity/quantities, supervision, fine, representative execution and quarterly election. |
| `335d02e7b7b8f171e488a91ba9ad1f8cd0f5a5dd36862426d4ea6b05880e4c8b` | 1–4 | Maker/holder, single principal, security recital, annual actual/360 rates, maturity/Business Day, cure/election, notice/waiver/assignment, predecessor recital, apparent execution wording. |
| `fcab671544eb296de33fc6a850d3dac5170af6bd829acd3c5aca6963a0ef4079` | 1–3 | Sosnick membership, loan/delivery allegation, para.10–11 cutoff, alleged delivery and requested relief. |
| `dda6462c992a2c25b343b16fbe63fced88fa0f7c0393f919d91f10df17ce57c1` | 1 | Demand date, amounts, 15% and delivery legend. |
| `fd9afe06e208578c033189f12c188e9ab4f6d7bca644da8f592f07cfd84e3bae` | 1 | Requested relief, start date, per diem and fee scope. |
| `510149f9ff4b8601f7cbe22e813d7883f3104f3431eed016ce2fe6208d499519` | 1–2; p.1 image | Image confirms November30/December3 **2018**, moot/disposed handwriting; Notice/Stipulation difference and without-prejudice/costs scope. |
| `cf92cd916d5314f1b00a2e74f3661ff6eba104cb667a86298ce2a592570009c1` | 1 | December2020 administrative error/correction, no reopening/payment inference. |
| `208aadb036798dd224654689b0edd5e370f383e43c691d69a4fc99851b0081a5` | Native pp.1, 27 | Caption, filing date and attributed Scout comparator allegations. |
| `bee45b687c95d8daa1b49efe316cac13e0690cbe72ccfcce0b5814eb66c5c728` | Native pp.2–4, 14, 19–20, 22; OCR p.18 | Attributed biography/BATS and nonparty acknowledgment; Harrison, counsel, client-fee award and proposed legal theories. |
| `e11ec1f2c4a6b631ea322f8698729edf66fd9d464402cf6203cd721ee1ba5018` | Supplied Markdown body | Later-role/universal-clean-history assertions, Wedbush/FXCM, ownership and same-name/null-search leads are attributed rather than adopted. |
| `a13f7edef78fc2fb7786aa38901e81a6afe1e197ccae10bb591dfd4202bc1c62` | Supplied TXT body | Harrison parties, index reference, blank dates/placeholders and draft status. |
| `1ced6091a1f7f046a64a8099fd2e1a1c1ab0d8406a82775c7af8f94be241104e` | Entire supplied CSV | Nine indexed references, Scout CIK/file metadata, absence of CRD; no underlying URL followed. |

Generated browser/print behavior and final portable asset sealing are outside this source-review verdict and require the separate front/integration review.
