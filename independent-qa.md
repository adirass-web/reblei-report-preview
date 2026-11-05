# Independent adversarial QA — bounded identity and entity discovery

Reviewed November 4, 2026. Reviewer independently inspected the identity and SEC specialists' source originals and challenged their principal conclusions. This review is independent of those two specialists; the reviewer also authored the initial event-discovery report, so this is **not independent QA of that reviewer's event work**.

**Result: qualified pass for the examined filing-based identity/entity findings.** No material transcription or attribution error was found in the sampled principal claims. This does not certify complete career coverage, absence of other entities/events, or the truth of every filer representation. Three material source discrepancies remain open. Full individual employment/registration history, historical ADV coverage and native regulator/court searches remain incomplete.

## What was actually tested

- Read `specialist-identity.md`, all22 records in `identity-sources.json`, `specialist-sec.md`, the46 records in `sec-claims.json` and the SEC source manifest.
- Independently extracted the original Scout FINRA report, Ophir March2017 ADV and EntryPoint October2026 ADV. Physical PDF pages below are1-based and count covers; Scout's printed footer page is generally two lower than physical page.
- Independently reparsed all9 preserved FormD complete-submission files for the two EntryPoint feeder chains and Ophir master; checked issuer CIK/name/type, first-sale fields, reported sold amounts, investor counts and SEC filing-date headers. Examined the related-person fields for attribution.
- Visually inspected EntryPoint ADV physical pp24–25 because ordinary text extraction drops selected radio-button values.
- Recomputed SHA256 for **all20 successful SEC original/API response records and all5 identity PDF/rendered-capture records**: no mismatches. This validates integrity against the manifests, not origin certification, completeness or underlying economic accuracy. There are duplicate presentations/API histories among the20; it is not20 distinct filings.
- Inspected the original Inferent ADV and exchange-hosted Lehman release as challenges to unresolved career links.

## Principal tests and outcomes

| Test | Outcome | Exact source locator and limitation |
|---|---|---|
| Subject identity and wrong-person exclusion | Pass | [Scout FINRA](https://files.brokercheck.finra.org/firm/firm_151990.pdf) physical pp6,8; [Ophir ADV](https://reports.adviserinfo.sec.gov/reports/ADV/164729/PDF/164729.pdf) pp19–20; [EntryPoint ADV](https://reports.adviserinfo.sec.gov/reports/ADV/313946/PDF/313946.pdf) pp26–27 each pair Michael Edward Bleich with CRD4262671. No Keith Michael Bleich/CRD2372764 data is used to establish subject roles. |
| EntryPoint firm identifiers | Pass | Original ADV p1:CRD313946/SEC801-130798/CIK1992519. These identifiers belong to the firm, distinct from individualCRD4262671. |
| Career dates | Qualified pass | Scout p6 describes position start05/2009; Ophir p19 status acquired04/2012; EntryPoint p26 CIO status acquired05/2023, p27 intermediary interests acquired07/2023. These are disclosed role/status dates, not complete employment periods. The reports preserve that distinction. |
| Firm status versus individual tenure | Pass | Scout p4 gives business cessation2014-07-17; p11 gives firm registration2009-11-17–2014-09-19. Ophir rendered official status capture gives termination2017-06-29. These do not establish Bleich's employment end or corporate dissolution. |
| Ownership thresholds | Pass with wording discipline | EntryPoint p26 explicitly defines C=25% to less than50%, E=75% or more and NA=less than5%. p27 lists Bleich's twoC-coded intermediary interests. Do not replace intervals with exact stakes, add or multiply them into an exact adviser holding, or infer an affirmative direct equity stake from an officer's NA entry. |
| Historical intermediary chain | Pass with open conflict | Scout pp8–9 and Ophir pp19–20 support professional links through MEB NY INC/Finch; Scout includes NAYS LLC. Snapshot-specific bands and dates must be retained; see conflict1 below. |
| EntryPoint versus fund assets | Pass | Original ADV p8:firm RAUMUSD999157153, four discretionary accounts; p27 explicitly measures RAUM as of2026-09-30; headerp1/executionp28 date2026-10-15. p17:master-fund current gross asset valueUSD799157153. These are distinct metrics; master valuation date is not separately verified. USD200m difference is not assigned to Walleye or any other activity. |
| Feeder/master identifiers | Pass | EntryPoint pp15–17:master805-7203779905; domestic feeder805-8039696809; international feeder805-5004504749. EDGAR submissions establish domesticCIK2016250 and internationalCIK2016251. Do not substitute CIKs for805 private-fund IDs or infer an undiscovered master CIK. |
| GP identity | Pass | EntryPoint GP LLC(p26–27) and EP Fund GP, LLC(pp14–17; feeder FormD related persons) remain distinct entities. A listing as GP/manager/director equivalent is not proof of an identical legal person or an undocumented ownership chain. |
| FormD observations | Pass | Raw complete-submission XML for accessions0002016250-24-000001/000002,0002016250-25-000001,0002016250-26-000001 and corresponding2016251 chain matches extracted cumulative amounts/investor counts. Latest amountsUSD62545000 andUSD47973695 are issuer offering observations, not NAV/RAUM or annual flows. Do not sum amendments or assume counts are unique people across funds. |
| Ophir master director | Qualified pass | Original accession0001555295-12-000002, `/edgarSubmission/primaryIssuer`, `/relatedPersonsList`, `/offeringData/signatureBlock`:CIK1555295, Michael Edward Bleich director, signature2012-07-31, filed2012-08-01. No CRD is in this document; linkage relies on corroborating full name/Ophir records. Zero sold and yet-to-occur first sale in the initial notice do not prove no subsequent capital raising. |
| Walleye discovery | Pass within limit | EntryPoint p21 Schedule7.B.(2) lists Walleye Opportunities Master Fund Ltd805-3011135543 and reporting adviser Walleye Capital LLC801-113731. This supports a disclosed advisory/reporting relationship, not Bleich employment/control/ownership of Walleye. |
| Discipline disclosure scope | Pass within limit | EntryPoint physical pp24–25 visually selectNo for the displayed Item11 responses; p27 has no DRP information filed. This is the current filing's representation. It does not establish no historic personal/firm events, and does not by itself demonstrate an omission concerning Scout's2015 firm sanction. Definitions and time limits differ. |
| Inferent career link | Unresolved; no confirmation | Original Inferent Capital LLC ADVCRD292027/SEC801-112741, physicalp1 dated2019-03-06; all32 pages searched forBleich without a text occurrence. This neither establishes a Bleich role nor proves he never had one. |
| Lehman lead | Qualified lead only | Exchange-hosted September19,2006 corporate release, physicalp1, quotes Michael Bleich as Lehman head of liquidity strategy. It is a corporate statement hosted by an exchange, not a regulator-verified employment record; it supplies no individualCRD. Do not elevate it to a fully resolved CRD-linked role or infer BATS personal equity ownership. |

## Open source discrepancies — retain, do not repair by assumption

1. **MEB NY INC → Finch.** Scout original physicalp8 reports50%–<75%, relationship established08/2012. Ophir March2017 ADV physicalp20 reports codeE75%+, status acquired04/2012. The sources may reflect different snapshots or inconsistent reporting. Neither explanation is established. Preserve document/date/source per edge; no timeless consolidated percentage.
2. **Beaufort same-name private-fund IDs.** Ophir physicalp10 gives OPHIR PARTNERS BEAUFORT FUND LP805-5280422629; p14 repeats that name under805-9412438643. Both values are real source entries. They are not enough to conclude either one fund with an error or two legally distinct funds. Registry/earlier amendment reconciliation remains open. The GP's Other number47-5442903 onp9 is not proven to be a CRD.
3. **International LP legal-form field.** All four preserved International FormD submissions use issuer name EP Third Moment International, LP while entityType isCorporation. Preserve both source fields; seek Cayman legal-formation evidence. Do not auto-correct to a partnership or assert a filing violation.

## Minor preservation caveat and corrective guidance

The preserved negative FINRA/IAPD rendered-result responses showNo Results/No match, but the captured `query` property is researcher-entered capture metadata rather than a recorded form-input value. Exact-query execution is supported by the researcher's process record; those saved responses alone do not independently prove what was submitted. Stronger preservation would include actual input state or search request. The reports correctly draw no broader negative conclusion; this caveat does not undermine the positive CRD matches in three original firm filings.

Use reported less-than5%category for officer rows, avoiding language implying positive direct ownership. Treat mutable ADV download URLs as retrieval snapshots; historical filing dates come from document headers, not the filename or live endpoint. A successful official source download verifies the retained content, not that every regulator has audited its substance.

## Scope and remaining work

Litigation is limited to investment-management conduct (fund operations, trading, investor/advisory/fiduciary conduct). Personal civil matters are excluded. The Triffin/Ophir business-contract lead remains quarantined until an official pleading establishes both identity and that specific relevance; a generic contract label is insufficient. The event report was updated to this constraint.

Full-career completeness fails at this stage: early employers, the full individual registration history, the Inferent link, original historical amendment/brochure chains, corporate/overseas legal identity checks and comprehensive investment-related litigation searches are still open. The review does not certify missing periods by extrapolating a role's status date, no-result screen, initial fund notice or absence of an ADV name.

This review covers the specialist reports/originals described above. The parent normalized index was not yet present when these checks were performed; any later normalization requires its own reference-integrity check. No principal datasets were edited by this QA pass.

## Addendum — newly preserved March2025 and March2026 brochures

After the main review, independently inspected `evidence/parent-entrypoint-brochure-956158.pdf` and `evidence/parent-entrypoint-brochure-1031410.pdf` (each12physical pages), specifically pp1,4–5. No repository root or existing ZIP archives were used.

- **Pass:** covers date them March2025 and March2026. Physicalp4 attributes indirect ownership of EntryPoint to Michael Bleich through EntryPoint Partners, LP and describes both master and international funds as Cayman exempted limited partnerships. These are adviser representations in filed brochures; they strengthen the documented difference from International FormD entityTypeCorporation but do not themselves establish registry-verified legal form or an error/violation.
- **Pass:** March2025 brochurep4 gives approximate discretionary RAUMUSD578038743 as of2024-12-31; March2026p4 gives approximate discretionary RAUMUSD700332093 as of2026-03-11. Preserve the distinct measurement dates and approximation qualifier. Neither is a September2026 figure.
- **Pass with qualification:** bothp4 summarize a monthly management fee paid in advance at1/12of2% of the beginning-of-month associated capital-account balance, subject to waiver/modification. They describe a20% GP performance allocation andp5 permits waiver/modification; operating expenses are separately borne under stated terms. Do not calculate actual management or performance revenue fromRAUM: fee bases, waivers, net profit definitions and investor terms require offering documents and observations.
- **Source-text limitation:** the performance-allocation sentence onp4 appears incomplete, ending with the Funds rather than a fully specified benchmark; p5 starts with waiver language. The summary20% rate is visible, but precise hurdle/high-water-mark/calculation mechanics cannot be reconstructed from this passage. Do not silently supply standard hedge-fund terms.
- **Source-text anomaly:** each cover's registration disclaimer includes the nameVoyager amid EntryPoint text. Preserve if discussing document quality; do not infer an affiliation or a separate manager from a likely template remnant without evidence.
- **Gap remains:** these are March brochure snapshots, not a verified replacement for the unavailable October version1061309. New parent acquisitions/hashes are recorded in the parent's source manifest and were not included in the earlier20+5hash tally.

## Addendum — independently reproduced2024Q3 Form13F inconsistency

Independently parsed the two XML blocks in original complete submission `evidence/fin-1992519-0001992519-24-000008.txt` (accession0001992519-24-000008, report period2024-09-30). The cover reports `tableEntryTotal=175789` and `tableValueTotal=594`. The information table actually contains594`infoTable`rows, with raw `value`sum175789004. The discrepancy is reproduced, not a parsing error in the specialist's output.

Official Form13F instructions preserved at `evidence/fin-form13f-instructions.pdf`, physicalp6, define entry total as line-entry count and value total as the aggregate Column4fair market value; the instruction says values rounded to the nearest dollar. Physicalp13also specifies nearest-dollar value total. Thus cover-versus-table inconsistency is an open source anomaly. Retain raw fields and the independently derived row count/value sum as different observations. Do not silently swap fields, substitute a corrected cover, assume historical thousand-dollar units, attribute cause or infer misconduct. Quarantine from automated holdings trends until amendment-chain review resolves it.

The remaining newly collected13F filings are outside this addendum's numerical review; a complete15filing inventory does not mean all15have been independently checked for holdings arithmetic.

## Final addendum — bounded independent review of normalized exports

The normalized exports subsequently became available. This addendum supersedes the earlier statement that they had not been examined. Reviewed the newly generated `evidence-index.json` and opened `evidence-index.sqlite` read-only. The reviewed index contains47documents,104claims,26relationships,50financial observations,6roles and5regulatory firm events across17tables.

**Result: qualified pass, with one small disambiguation recommendation.**

- Checked all normalized document,claim,subject,entity,person,event and conflict references; none unresolved. All48document aliases resolve. Raw financial-stage document references resolve directly or through aliases.
- Verified every one of the47document file paths exists and all retained SHA256values match current file bytes. Rendered-result captures are explicitly classified as rendered captures, rather than original PDFs/HTML.
- SQLite `foreign_key_check` returned no rows; `integrity_check` returnedok. All17JSONtable contents match SQLite field values and counts. SQLite REAL ownership numbers versus JSON integers are representation differences only, with equal numeric values.
- Read all26relationship rows: directions are owner/member→owned entity, feeder→master and reporting adviser→reported fund as applicable. C/D/Epercentage bands preserve exclusive upper bounds correctly. Conflicting Scout/Ophir MEB→Finch entries remain separate, claim-linked assertions. Unknown end dates do not become verified ongoing ownership.
- Read all6role rows: status-acquisition dates remain labelled as such; the Ophir master director row labels its date as a signature observation, with appointment commencement unknown. No individual employment end is fabricated from firm cessation/registration dates.
- P002Keith Michael Bleich is marked excluded and has no role,ownership,event or claim linkage. E021Inferent is expressly unresolved as to the subject, with no confirmed Bleich role or relationship edge. Candidate-branch entities do not become confirmed subject affiliations.
- E008Beaufort is expressly an ambiguous name placeholder with both805IDs flaggedambiguous_same_name and an open conflict; it does not assert a single legally resolved vehicle. **Recommended precision:** itsF004gross-asset observation andL015GP/manager edge arise specifically from Schedule7.B.(1),ID805-5280422629. Pin that scope in their notes/date-basis fields so a downstream identifier join cannot imply that the second805ID shares those assets or GP. Existing source claims permit reconstruction; no numerical error was found.
- FinancialF001firmRAUM has the explicit2026-09-30date;F002masterGAVhas no invented same-date assumption. F033–F036keep2024Q3raw cover and independently derived observations distinct, allquarantined. F031–F032retain the2024Q2NEW HOLDINGS amendment's reporting period2024-06-30and mark it nonstandalone. No amendment-chain sum or corrected2024Q3cover is silently produced.
- Events remain fourScout firm matters and one separateWedbush matter. No personal civil proceeding is included as an investment-management event; Triffin is absent from confirmed claims/events. The exact-scope gap remains open rather than normalized into a litigation finding.

This is a consistency/attribution review of the assembled evidence, not a renewed exhaustive source search or independent arithmetic audit of every13F. Newly collected Inferent branch entities are correctly candidates; their full internal structure was not independently audited in this addendum. No existing repository files/ZIParchives were researched, and no principal index data was edited by the reviewer.

The parent accepted the Beaufort recommendation and is applying explicit Schedule7.B.(1)/805-5280422629scope toL015andF004, with no attribution to805-9412438643. The parent will regenerate both exports and perform final packaging integrity checks; this records the accepted correction without claiming a separate re-audit of the regenerated package.


## Subsequent continuation review

The earlier review above applies to the baseline package. The expanded package is reviewed separately in [cross-specialist QA](continuation/qa.md), [Cboe-original QA](continuation/qa-events.md) and [normalized-index QA](continuation/qa-index.md). No claim that every new registry response or every court system was exhaustively audited is made.


## Round2 independent review

See [employment/Inferent](continuation-2/qa-employment-inferent.md), [ownership](continuation-2/qa-ownership.md), [litigation originals](continuation-2/qa-litigation.md) and [consolidatedindex](continuation-2/qa-index.md). Source-level corrections were applied before the final register build; source bytes were not altered. Mainfindings retain approved, explicitlylabeled official-recordinferences.

## Round 3 independent review

See [Scout annual originals](continuation-3/qa-scout.md), [Inferent original brochure and bulk tables](continuation-3/qa-inferent.md), [Ophir historical role/ownership tables](continuation-3/qa-employment.md), [award follow-up](continuation-3/qa-award-followup.md), and [normalized index](continuation-3/qa-index.md).

Corrections include Scout FINRA page locators and nonmembership context, and the material EntryPoint filing-type classification. Exact original flags now state Initial SEC Registration Request=Y in both2021/2024 rows; Final SEC ERA Report is blank in2021 and Y in2024. No reason for dual2024flags is inferred. The derivative table joins were faithful; narrative labels were corrected. Original bytes were unchanged.

The new historical Ophir evidence qualifies the shared04/2012 acquired-status date: it does not independently date the later-added CCO label. MEB INC is a disclosed-name placeholder with unresolved equivalence to MEB NY INC, not an asserted separate incorporated company. Ownership filing snapshots do not become legal transaction dates or exact personal wealth.

## Round 4 independent review

See [employment and Inferent](continuation-4/qa-employment-inferent.md), [corporate identity](continuation-4/qa-corporate-identity.md), [registration and withdrawals](continuation-4/qa-registration-withdrawals.md), [litigation](continuation-4/qa-litigation.md), and [normalized index](continuation-4/qa-index.md).

The latest review checks exact CRD/FilingID joins, source bytes and archive reconstruction, original instruction pages, ownership-band limits and claim locators. It confirms that the three new ADV-W events are administrative filings with no respondent or fine; the associated firm is resolved through its claim. Inferent affiliation remains conditional and its balance-sheet difference stays quarantined. New corporate identifiers are not inferred from matching names.

The earlier round 3 statement that no reason was inferred for the dual EntryPoint flags is historical: round 4 adds original General Instruction 15 and makes a clearly labeled procedural inference. It does not infer approval, compliance, a merger or a legal name-change date. The normalized index was separately checked across all 17 tables, all 396 document hashes and all 247 claim links. This is bounded evidence/integration QA, not comprehensive court clearance.

## Round 4 independent review

See [employment/Inferent](continuation-4/qa-employment-inferent.md), [registration/withdrawals](continuation-4/qa-registration-withdrawals.md), [corporate identity](continuation-4/qa-corporate-identity.md), [litigation](continuation-4/qa-litigation.md), and [consolidated index](continuation-4/qa-index.md).

The round 3 statement that the dual 2024 flags remained unexplained is historical. Newly retrieved official instructions now support a labeled procedural interpretation; they do not adjudicate eligibility, approval, timeliness or corporate identity. The three new withdrawal records are administrative filings, with no respondent or fine assigned.

The consolidated review verified all 396 indexed document hashes, all 17 JSON/SQLite table comparisons, 247 claim evidence links and the 33 round 4 claims. This is source and integration QA within the recorded scope, not comprehensive employment, court or adverse-history clearance. The remaining work is listed separately.
