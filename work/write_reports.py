from pathlib import Path
import json,datetime
p=Path('outputs');d=json.loads((p/'evidence-index.json').read_text(encoding='utf8'));t=d['tables']
(p/'README.md').write_text('''# Michael Edward Bleich — independent official-record investigation

Research cut-off: **November 4, 2026**. Subject: **CRD4262671**.

This batch establishes the official identity/entity baseline, collects accessible filing histories, records investment-management regulatory events and financial observations, and performs independent adversarial review. **The full-career investigation is not complete.** Early career, Inferent linkage, original corporate ownership records and comprehensive investment-management court coverage remain open.

Repository: private `adirass-web/ReBlei`. Separate branch: `research/bleich-official-records-2026-11-04`. This investigation is confined to `investigations/2026-11-04-official-records/`.

**Existing repository material was not used as research evidence.** Existing root files are untouched. Personal civil proceedings and private home/family matters are excluded. The five referenced ChatGPT Library files were inaccessible and have not been reconciled.

## Read first

- [Findings and gaps](findings-and-gaps.md)
- [Decisions and scope](decisions-and-scope.md)
- [Document index](evidence-index.md)
- [Independent QA](independent-qa.md)
- [Next-stage retrieval queue](next-stage-queue.md)

## Evidence and structured records

- [Original records and explicitly labelled result captures](evidence/)
- [Normalized JSON index](evidence-index.json)
- [Relational SQLite database](evidence-index.sqlite)
- [Table exports](tables/): persons, entities, identifiers, roles, relationships, documents, claims, claim_evidence, financial_observations, events, event_claims, search_logs, conflicts, conflict_claims, retrieval_attempts and source aliases.
- [Database schema](schema.sql)
- [Validation results](validation.json)
- `SHA256SUMS.txt` verifies all files in this folder except itself. The originals are immutable captured responses; derived text and analysis are separate files.

The index contains **47 captured source representations**, **104 source-linked assertions**, **31 entity entries including unresolved candidates**, **26 relationships**, **50 financial observation rows** and **55 search-log entries**. These are counts of records, not counts of independently verified facts, unique filings, unique funds, people or events. One representation may support multiple claims. Duplicate specialist references resolve through document aliases.

## Specialist reports and process records

[Identity](specialist-identity.md) · [SEC entities and filings](specialist-sec.md) · [Investment-management regulatory events](specialist-events.md) · [Corporate candidates](specialist-corporate.md) · [Financial observations](specialist-financial.md)

The corresponding `*-sources.json`, claim/observation JSON and search logs preserve specialist provenance. `work/` retains acquisition, indexing and documentation scripts. The index can be rebuilt from this folder with `python work/build_index.py .` using Python's standard library. Acquisition scripts record this session's working paths; do not bulk rerun them without checking their paths and source limits.

Search providers: native web discovery initially; **Parallel Search** following the user's provider instruction. Direct HTTPS retrieved originals from SEC, FINRA, Nasdaq and government open-data endpoints. Firecrawl's initial requests did not run because credits were exhausted; no subsequent use. No Tavily tool/plugin was available. Interactive browser searches are recorded separately; later collection did not depend on Chrome.

## Evidence interpretation

Official filings are attributed **as filed**, not independently certified financial or legal conclusions. RAUM, private-fund gross assets, FormD cumulative sales and Form13F reportable holdings are distinct. Registration/status dates do not establish complete employment periods. Ownership bands are not exact economic entitlements. Missing results do not establish absence of misconduct.

Independent review checked the core original claims and a bounded second pass over the normalized index. It did not audit every holding, every filing's arithmetic, all offshore registers or all court systems. Original discrepancies and access gaps remain visible.
''',encoding='utf8')
(p/'findings-and-gaps.md').write_text('''# Findings and material gaps

November 4, 2026. Official-record statements are verified as filed. Full career coverage remains incomplete.

## Identity and professional chronology

| Record observation | Date basis | Evidence |
|---|---|---|
| Michael Edward Bleich is individual CRD4262671; Scout CEO/managing member | Position reported from05/2009; no full employment interval inferred | FINRA Scout original physicalpp6,8; ID-C001/C003 |
| Ophir Partners LLC CRD164729/SEC801-77121 lists him as CEO/CCO | Status acquired04/2012, in March30 2017 ADV | Ophir original physicalpp1,19; ID-C011/C012 |
| Ophir Partners Master Fund Ltd CIK1555295 lists full-name director; Michael Bleich signs | SignatureJuly31 2012; filedAugust1 2012 | SEC accession0001555295-12-000002, RelatedPersons/signature; SEC-D corresponding claims |
| EntryPoint Capital LLC CRD313946/SEC801-130798/CIK1992519 lists exact full name and CRD as CIO/control person | ScheduleA status acquired05/2023; not proof the whole relationship began then | EntryPoint Oct15 2026 ADV physicalpp1,26; SEC-C001/C002 |
| Indirect EntryPoint GP LLC member and EntryPoint Partners LP limited partner | Each status07/2023; each25% to less than50% | Same ADV physicalp27; SEC-C003/C004 |

[Scout original](evidence/id-finra-scout-151990.pdf) · [Ophir original](evidence/id-sec-ophir-164729-adv.pdf) · [EntryPoint original](evidence/sec-313946-adv.pdf)

The Scout report distinguishes firm cessationJuly17 2014 from registration dates. Ophir's official status page reports SEC terminationJune29 2017. Neither date establishes the subject's personal departure or corporate dissolution.

Lehman, Barclays and Chase remain early-career leads awaiting an original official employment/registration chain. A2006 Cboe-hosted corporate release names Michael Bleich as Lehman's head of liquidity strategy; it is retained as a lead, not used to force a name-only identity join. Inferent's official2019 ADV confirms that firm's identity but contains no Bleich text match. Third-party research-head and employment dates remain unverified.

## Ownership and fund universe

The historical FINRA/Ophir records document the Bleich–MEB NY Inc.–Finch chain, with NAYS/Dror Niv as a separately disclosed historical ownership branch. Finch is disclosed in connection with both Scout and Ophir. Percentages and status dates are source-specific: Scout shows MEB/Finch50%–less than75% from08/2012; Ophir2017 shows75%+ from04/2012. Do not combine these into one timeless stake.

EntryPoint Partners LP is disclosed as a75%+ direct member of EntryPoint Capital. EntryPoint GP LLC and EP Fund GP LLC are legally distinct names/functions and remain separate entries. The EP Third Moment master and its domestic/international feeders are linked in the ADV. The domestic feeder's FormsD disclose former name **EP Healthcare Transformation Fund, LLC**.

Walleye Opportunities Master Fund Ltd805-3011135543 appears in EntryPoint Schedule7B2, with Walleye Capital LLC SEC801-113731 furnishing full fund reporting. This does not establish Bleich ownership, employment or control of Walleye. See SEC-C009/C011/C012 and the [relationship table](tables/relationships.csv).

Ophir's Beaufort fund name appears under805-5280422629 in7B1 and805-9412438643 in7B2. It is an ambiguous name placeholder in the index. Its GP and gross-assets observations are pinned specifically to the7B1 identifier, not both identifiers.

NY open-data name matches suggest DOS3772241 for MEB NY Inc. and DOS6795220 for EntryPoint Partners LP. These are provisional candidates, not confirmed owner-resolved corporate joins. The government dataset itself disclaims formal-record/current-status/certified-copy effect; original registry filings remain necessary.

## Financial observations

| Metric | Amount USD | Measurement date or scope | Evidence |
|---|---:|---|---|
| EntryPoint discretionary RAUM |578,038,743|December31 2024; brochure says approximately|March2025 brochure version956158,physicalp4|
| EntryPoint discretionary RAUM |700,332,093|March11 2026; brochure says approximately|March2026 brochure version1031410,physicalp4|
| EntryPoint discretionary/total RAUM |999,157,153|September30 2026; four accounts|October15 2026 ADV,physicalpp8,27|
| EP Third Moment master current gross assets |799,157,153|Separate metric; measurement date not independently established|Same ADV,physicalp17|
| Latest retrieved EntryPoint13F cover total |412,064,875|June30 2026; filedAugust13 2026; reportable holdings only|Accession0001992519-26-000007|
| Domestic feeder cumulative FormD amount sold |62,545,000|March12 2026 notice;23 issuer-reported investors|Accession0002016250-26-000001|
| International feeder cumulative FormD amount sold |47,973,695|March12 2026 notice;18 issuer-reported investors|Accession0002016251-26-000001|

All four FormsD shown in each EP feeder's retrieved history and all15 EntryPoint submissions shown in its history were preserved. Ophir's2012 initial FormD reports zero sold before first sale; this does not establish that the fund never later raised money. Amendments must not be summed as separate fundraising flows. Investor counts are not verified unique natural persons.

The2024Q3 EntryPoint13F (0001992519-24-000008) has an internal inconsistency: its cover reports175,789 entries andUSD594; its information table contains594 rows summingUSD175,789,004. Both raw and independently reproduced derived observations are retained and quarantined from clean trends. No cause or corrected filing is inferred. The2024Q2 NEW HOLDINGS amendment filedAugust2026 also remains separate from a replacement full-period total.

March2025/2026 brochures summarize a monthly management fee of one-twelfth of2% of beginning-month investor capital-account balances, subject to waiver/modification. They state a20% GP performance allocation, but the calculation sentence is incomplete. Do not reconstruct hurdles/high-water marks or actual revenue, or apply headline rates mechanically to firm RAUM or personal ownership bands. October brochure1061309 was not retrieved.

## Investment-management conduct and litigation

Original Nasdaq AWC20100243866-01 names **Scout Trading LLC** as respondent. It was acceptedApril7 2015, with censure andUSD3million fine, without admission or denial and without adjudication. Michael Bleich signed for Scout as managing member onApril1. This instrument does **not** establish a separate personal sanction against him. The broader investigative period differs from its applicable Nasdaq-member period. See [AWC original](evidence/evt-scout-nasdaq-20100243866-01.pdf),physicalpp1,3–7,10.

The FINRA Scout report separately discloses three CBOE firm events with censures andUSD5,000,USD7,500 andUSD10,000 fines. These are verified report disclosures; underlying CBOE orders remain to be retrieved. A Wedbush clearing-firm event is kept separate and is not added to Scout's or Bleich's penalties.

Personal civil proceedings are excluded. The Triffin/Ophir business-contract lead is quarantined because original pleadings and an investment-management-conduct nexus have not been established. No comprehensive court or disciplinary clearance is claimed.

## Access and completeness limits

Individual BrokerCheck/IAPD PDF endpoints returned403; actual CRD searches returned no result. The archived search-result text records the query through researcher provenance rather than independently preserving the input control. These limitations do not negate the exact CRD/full-name links in firm originals or establish no personal sanctions.

Uncompleted work: early-career official employment chain, historical ADV amendments and brochures, owner-linked corporate originals, Cayman legal-form records, original CBOE orders, professionally relevant court database coverage, and reconciliation of the five inaccessible prior Library documents. Existing ReBlei source material was excluded by instruction.

[Independent QA](independent-qa.md) gives the examined scope and remaining discrepancies. [Next-stage queue](next-stage-queue.md) identifies concrete retrieval tasks.
''',encoding='utf8')
(p/'next-stage-queue.md').write_text('''# Next-stage retrieval queue

This is an operational continuation queue, not a claim of completed full-career coverage. Continue free independent official-record work; do not use existing ReBlei root material or personal civil proceedings.

| Priority | Required record or check | Why / completion gate | Current condition |
|---|---|---|---|
|1|Official individual CRD4262671 employment/registration/disclosure history|Resolve Lehman/Barclays chronology and full individual disclosure record|PDF403; actual UI no-result; a current public report may not be available|
|1|Historical Ophir and EntryPoint ADV amendments, including original status-change filings|Separate employment, role acquisition and changes in ownership over time|Current/latest retained snapshots are insufficient for full history|
|1|Original corporate records for MEB NY,Finch,NAYS,EntryPoint entities,Beaufort GP/fund|Authenticate legal IDs and owner-linked legal identity, not names alone|NY open-data candidates only; formal registry access/records unresolved|
|1|Cayman formation and status records for EP international/master and Ophir master|Resolve LP/Corporation discrepancy and legal status|Public US filing representations conflict; no certified offshore record obtained|
|1|Underlying CBOE orders14-0018,12-0099/12-0126,12-0059|Confirm full findings, respondent and terms beyond BrokerCheck disclosures|Official historical orders not yet located|
|2|Investment-management court searches for confirmed persons/entities|Retrieve docket, complaint, amended pleadings and disposition with identity/nexus checks|No exhaustive PACER/NYSCEF/NJ/other relevant court coverage; no paid access authorized|
|2|Inferent official role/employment/transaction evidence|Confirm or reject research-head role and any Ophir transaction, without assuming legal succession|Official Inferent ADV has no Bleich text; third-party leads remain|
|2|Original EntryPoint brochure1061309 and prior Ophir brochure247246|Authenticate versions and complete economics/governance narrative|Supplied EntryPoint endpoint404; March2025/2026 versions independently preserved|
|2|13F2024Q3 corrected filing/reconciliation and2024Q2 amendment chain|Keep anomaly quarantined until original amended evidence resolves it|Raw and derived values preserved; no silent correction|
|3|Prior ChatGPT Library files|Reconcile old claims and citation errors against preserved originals|Not accessible through available connection; user confirms no local copies|

No outreach, new account, purchase or default-branch merge has been authorized. Do not infer no event, no employment or no entity from inaccessible sources or bounded negative searches.
''',encoding='utf8')
lines=['# Preserved document index','','All SHA256 values identify captured bytes, not a certification of the filing assertions. Source-class distinctions and unsuccessful requests are in the structured index. Physical PDF pages are1-based; XML/JSON records use field locators.','','|Document ID|Source / type|Date or period|Preserved bytes|Official URL|SHA256|','|---|---|---|---|---|---|']
for x in t['documents']:
 def clean(a):return str(a or '').replace('|','/').replace('\n',' ')
 lines.append('|'+ '|'.join([clean(x['document_id']),clean(x['authority'])+' / '+clean(x['document_type'] or x['source_class']),clean(x['filing_date'] or x['period_end']),f"[{Path(x['file_path']).name}]({x['file_path']})",f"[source]({x['official_url']})",'`'+x['sha256']+'`'])+'|')
(p/'evidence-index.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Wrote findings, decisions navigation, document index and retrieval queue.')

