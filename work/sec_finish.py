from pathlib import Path
import json,hashlib
p=Path('outputs/sec-sources.json');docs=json.loads(p.read_text())
for d in docs:
 if d.get('status_code')!=200:continue
 raw=Path(d['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==d['sha256']
 if raw.startswith(b'%PDF'):d['preserved_format']='original PDF';d['source_class']='official filing'
 elif raw.startswith(b'<SEC-DOCUMENT>'):d['preserved_format']='original SEC complete submission text/SGML with embedded XML';d['source_class']='official filing'
 elif raw.lstrip().startswith(b'{'):d['preserved_format']='original SEC JSON API response';d['source_class']='official filing-history metadata'
 else:d['preserved_format']='official rendered HTML from SEC XSL endpoint';d['source_class']='official filing presentation'
p.write_text(json.dumps(docs,indent=2),encoding='utf8')
report=r'''# SEC specialist — identity and entity discovery

Research cut-off: November 4, 2026. Work is a bounded Step 1 discovery pass, with a subsequent bounded filing-chain collection. Official filing assertions are verified **as filed**, not independently audited economic or legal conclusions. Private addresses and family matters were not researched.

## Material verified findings

1. **EntryPoint identity chain is independently confirmed.** The preserved original ADV identifies EntryPoint Capital, LLC, firm CRD **313946**, SEC **801-130798**, CIK **1992519** (physical PDF p1). Its Schedule A identifies **Michael Edward Bleich, individual CRD4262671**, as Chief Investment Officer, status acquired **05/2023**, control person Y (p26). This is the acquisition date reported for this status, not proof that his entire relationship with the firm began then.
2. **The reported October 15 ADV and $999,157,153 RAUM are confirmed from original bytes.** Header p1 and signed execution p28 date the amendment October 15, 2026. Item 5F (p8) reports total/discretionary RAUM **USD999,157,153**, four accounts, zero nondiscretionary RAUM, and non-US client RAUM USD533,470,137. Schedule D Miscellaneous explicitly gives the RAUM measurement date **September 30, 2026** (p27). This verifies what the filing reports, not fund performance, revenue, fee income or personal wealth.
3. **The private fund's gross asset value is a different number:** EP Third Moment Master Fund, LP reports **USD799,157,153** (p17). The field says current gross asset value. Do not silently assign the September 30 RAUM date to this different field, or equate it with NAV. Do not attribute the USD200m numerical difference to a particular relationship without further evidence.
4. **A further private-fund relationship was discovered:** Walleye Opportunities Master Fund Ltd, private fund ID **805-3011135543**, appears under Schedule D7.B.(2) (p21); the adviser providing its full private-fund reporting is **Walleye Capital LLC, SEC801-113731**. This establishes the disclosed advisory/reporting connection. It does not establish Bleich employment, ownership, or control of Walleye.
5. **The historical Ophir master-fund link is independently corroborated.** The original complete SEC submission **0001555295-12-000002**, filed **August 1, 2012**, identifies Ophir Partners Master Fund Ltd, CIK **1555295**, a Cayman exempted company with limited liability, incorporation year2012. Related Persons names **Michael Edward Bleich** as Director; Michael Bleich signs as Director **July 31, 2012**. No individual CRD is present in Form D; corroborate with Ophir CRD164729 firm records for the cross-source identity chain.

## Confirmed EntryPoint structure, as reported

Source throughout: [official ADV](https://reports.adviserinfo.sec.gov/reports/ADV/313946/PDF/313946.pdf), preserved as `evidence/sec-313946-adv.pdf`.

| Entity/person | Identifier | Documented relationship | Physical PDF locator |
|---|---|---|---|
| Michael Edward Bleich | CRD4262671 | CIO of EntryPoint Capital, status acquired05/2023, control personY |26, ScheduleA|
| EntryPoint Partners, LP | corporate registry ID not yet obtained | Direct member of EntryPoint Capital from10/2020; codeE,75% or more; controlY |26, ScheduleA|
| EntryPoint GP LLC | corporate registry ID not yet obtained | Listed with statusGENERAL PARTNER from10/2020, codeNA, controlY; designation retained as filed |26, ScheduleA|
| Michael Edward Bleich → EntryPoint GP LLC | CRD4262671 | Member from07/2023; codeC,25% to less than50%; controlY |27, ScheduleB|
| Michael Edward Bleich → EntryPoint Partners, LP | CRD4262671 | Limited partner from07/2023; codeC,25% to less than50%; controlY |27, ScheduleB|
| EP Fund GP LLC | distinct from EntryPoint GP LLC | Disclosed related person; manager/GP or equivalent listed for master and both feeders |14–17|
| EP Third Moment Master Fund, LP |805-7203779905|Cayman master fund; named manager/GP or equivalent EP Fund GP, LLC|15|
| EP Third Moment Fund, LLC |CIK2016250;805-8039696809|Delaware feeder to master|15–16|
| EP Third Moment International, LP |CIK2016251;805-5004504749|Cayman feeder to master|15–17|
| Lawrence Edward Leibowitz |CRD2024745|EntryPoint CEO from10/2020; member of EntryPoint GP LLC from10/2020, codeC|26–27|
| Andrew Louis Alkon |CRD5079758|CCO/COO/CFO from05/2023|26|
| Richard A.Desich Irrevocable2005 SD Trust |corporate/trust ID not obtained|Member of EntryPoint GP LLC from11/2024, codeC; controlY|27|
| South Dakota Trust Company |corporate ID not obtained|Trustee of the named ownership trust from12/2020, codeF; controlY|27|
| Walleye Opportunities Master Fund Ltd |805-3011135543|Private fund reported under7.B.(2); Walleye Capital LLC provides full reporting|21|

Ownership-code thresholds describe the particular entity in the row. They are not exact percentage interests in EntryPoint Capital and cannot be added or multiplied to obtain an exact beneficial stake. CIO Schedule A codeNA means the form's less-than5% category; it is not proof of an affirmative stake.

## Preserved historical fund filing chains

The full original SEC complete-submission text was saved for every filing listed below. Source URLs, accession IDs, filing dates, retrieval timestamps, file sizes, SHA256 and claim links are in `sec-sources.json`. These filings have no PDF pagination; use the specified XML paths and SEC header.

| Issuer | CIK | Accession | Filed | Cumulative amount sold USD | Investors already invested |
|---|---|---|---|---:|---:|
|EP Third Moment Fund, LLC|2016250|0002016250-24-000001|2024-03-22|15,720,000|18|
|same|2016250|0002016250-24-000002|2024-06-04|15,720,000|18|
|same|2016250|0002016250-25-000001|2025-03-14|47,245,000|21|
|same|2016250|0002016250-26-000001|2026-03-12|62,545,000|23|
|EP Third Moment International, LP|2016251|0002016251-24-000001|2024-03-22|10,946,314|12|
|same|2016251|0002016251-24-000002|2024-06-04|10,946,314|12|
|same|2016251|0002016251-25-000001|2025-03-14|34,750,715|17|
|same|2016251|0002016251-26-000001|2026-03-12|47,973,695|18|
|Ophir Partners Master Fund Ltd|1555295|0001555295-12-000002|2012-08-01|0|0|

These are cumulative as-filed offering observations, not period fundraising flows, current NAV or RAUM. Do not sum amendments. Counts are reported issuer investor counts, not verified unique natural persons. The Ophir notice says first sale had yet to occur; zero sold in this initial notice does not show it never later raised capital.

Both EP feeder filing chains list EntryPoint Capital as Investment Manager and EP Fund GP, LLC as General Partner in Related Persons. The domestic feeder reports previous name **EP Healthcare Transformation Fund, LLC**, incorporation2021, first sale2023-09-01. International reports incorporation2023, first sale2023-12-01. Filing histories independently confirm all four supplied fund/adviser CIKs.

Official source examples: [domestic2026 complete submission](https://www.sec.gov/Archives/edgar/data/2016250/000201625026000001/0002016250-26-000001.txt), [international2026 complete submission](https://www.sec.gov/Archives/edgar/data/2016251/000201625126000001/0002016251-26-000001.txt), [Ophir2012 complete submission](https://www.sec.gov/Archives/edgar/data/1555295/000155529512000002/0001555295-12-000002.txt).

## Other EntryPoint filings preserved for the next stage

The SEC original submissions API lists15 filings, with no older-history file pointer in the retrieved response. The following full submissions were preserved:

- **0001992519-24-000002**:13F-HR, filed2024-02-14, period2023-12-31; the earliest filing shown in the retrieved history. This is not proof it is the firm's earliest public record of any type.
- **0001992519-26-000007**:13F-HR, filed2026-08-13, period2026-06-30.
- **0001992519-26-000006**:13F-HR/A, filed2026-08-13, **period2024-06-30**, amendment type **NEW HOLDINGS**. It must be applied to the appropriate2024 reporting chain; do not misclassify it as2026Q2 or blindly replace/sum all2024 filings without reviewing amendment instructions and the original.
- **0001992519-26-000008**:N-PX, filed2026-08-18, period2026-06-30.

The first and latest13F covers identify Andrew Alkon as COO signatory; they do not prove that Bleich personally owns the securities. Holdings totals and their proper amendment/unit treatment remain for the financial-observation stage.

## Conflicts, limitations and next checks

- **International legal-form discrepancy:** every preserved International FormD (2024–26) names the issuer “EP Third Moment International, LP” but explicitly selects **Corporation** as entityType. Preserve both values. A legal-form determination requires Cayman registry/formation evidence; do not auto-correct the filing to limited partnership or declare an error established.
- **Name spelling:**2026 domestic FormD issuer address says “ENTRYPOINT PARNTERS LP”; normalize only as an address spelling variant and do not infer a separate entity from that typo.
- **Distinct entities:** EntryPoint GP LLC and EP Fund GP LLC must remain separate. Shared officers, addresses, a similar name, and a fund-manager listing do not establish identical legal identity.
- **Prior ownership leads:** MEB NY Inc, Finch LLC and NAYS LLC are not present in this current EntryPoint ADV. Their historical roles must be investigated through historical adviser/corporate records; absence here does not negate historic affiliation.
- **Inferent:** no determination made in this SEC subtask. Parent has a separate official Inferent ADV without a Bleich text occurrence; do not join the entity to the subject without stronger evidence.
- **Brochure:** supplied version1061309 returned404 at the stated official files.adviserinfo endpoint; no original brochure was obtained in this subtask. The ADV lists brochureID401422; this is a different identifier, not a verified replacement versionID.
- **Disclosure scope:** ADV p27 lists no information filed in criminal/regulatory/civil DRP pages. This is a filing observation, not a finding that no historic proceedings exist. Item11 visual checkbox review and separate FINRA/Nasdaq/court review belong to independent QA.
- **Acquisition limits:** Firecrawl search did not run because credits were exhausted. Direct SEC raw XML returned403 for some requested formats. Official SEC complete-submission text and two rendered SEC XSL pages were successfully obtained instead, with all attempts retained in the acquisition log. No paid access was used.
- **Preservation:**20 successful official document/API response records and8 failed retrieval attempts. All20 saved originals were checked against their SHA256 on completion.20 is not a count of unique filings: it includes4 JSON filing histories and duplicate rendered presentations of2 filings.46 structured claims are in `sec-claims.json`; extraction text is separately labelled with its own hash. Physical PDF page numbering is1-based. UTC retrieval timestamps are recorded per response.

ADV original SHA256: `a7f4fa57a87c511d908153a2db9fb57c87355f6b0b0fb6b4deff578156116054`.
'''
Path('outputs/specialist-sec.md').write_text(report,encoding='utf8')
print('Report saved; all20 original hashes verified.')
