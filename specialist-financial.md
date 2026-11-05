# Financial specialist — original SEC collection and observations

Research cut-off: November4,2026. This stage independently retrieved public SEC records; no pre-existing repository material was consulted. All figures below describe what records report, with specified units and limits.

## Collection completed

All **15 filings** in the independently preserved SEC submissions response for EntryPoint Capital, LLC, CIK1992519, are now preserved as original complete-submission text. Four were already acquired during SEC discovery; eleven additional originals were downloaded in this stage. They comprise **12 Form13F submissions** (11 original quarterly reports plus one amendment) and **3 N-PX submissions**. The retrieved response lists no older-history file. This defines the collected history, not a claim that no other records exist.

New acquisition metadata is in `financial-sources.json`; previously preserved originals remain indexed in `sec-sources.json`. This stage does not mutate those earlier files. Hashes for all12 newly preserved successful responses (11filings plus official instructions PDF) were checked. The unsuccessful direct FAQ request is logged separately in the same acquisition array. A Parallel Search discovery log is in `financial-search-log.json`.

## Units and interpretation

Original SEC Form13F instructions, preserved as `evidence/fin-form13f-instructions.pdf` (14physical pages), specify **US dollars rounded to the nearest dollar**, not thousands. See physicalp6, SpecialInstructions6(c) and8; p13 summary-page value total; p14 information-table value column. The retrieved document bears form revision07-23 onp1. Parallel Search also located SEC FAQ36's explanation that the nearest-dollar rule took effectJanuary3,2023; the FAQ's original HTML could not be downloaded, so the preserved form instructions supply the original-source unit proof.

These totals represent the securities reported on each Form13F. They are not firmRAUM, full net/gross portfolio assets, fundNAV, personal wealth, revenues, fees or performance. Changes in reported values do not establish investment returns. Investor and account identities cannot be inferred from these summaries.

Original instructions physicalpp4–5, SpecialInstruction3, distinguish restatements from additions. A NEW HOLDINGS amendment supplements a same-period report; its value is not a replacement full-period total. No amendment totals have been blindly added here, and no reconstructed2024Q2 holdings total is asserted.

## Form13F cover observations

Each row retains raw cover fields with scale multiplier1. Original files, document IDs, exact XML locators and interpretation flags are in `financial-observations.json`.

|Report period|Filed|Accession|Form|Raw cover entries|Raw cover valueUSD|Treatment|
|---|---|---|---|---:|---:|---|
|2023-12-31|2024-02-14|0001992519-24-000002|13F-HR|1,330|104,310,601|Original report|
|2024-03-31|2024-05-14|0001992519-24-000004|13F-HR|1,385|111,531,769|Original report|
|2024-06-30|2024-08-13|0001992519-24-000005|13F-HR|821|68,409,846|Original report|
|2024-06-30|2026-08-13|0001992519-26-000006|13F-HR/A|536|146,855,443|NEW HOLDINGS|
|2024-09-30|2024-11-13|0001992519-24-000008|13F-HR|175,789|594|QUARANTINED: internal mismatch|
|2024-12-31|2025-02-11|0001992519-25-000002|13F-HR|694|237,962,995|Original report|
|2025-03-31|2025-05-14|0001992519-25-000003|13F-HR|652|218,475,555|Original report|
|2025-06-30|2025-08-11|0001992519-25-000004|13F-HR|590|199,503,768|Original report|
|2025-09-30|2025-11-13|0001992519-25-000007|13F-HR|643|258,221,999|Original report|
|2025-12-31|2026-02-12|0001992519-26-000002|13F-HR|639|256,342,753|Original report|
|2026-03-31|2026-05-14|0001992519-26-000005|13F-HR|731|341,215,511|Original report|
|2026-06-30|2026-08-13|0001992519-26-000007|13F-HR|768|412,064,875|Original report|

### Material internal inconsistency:2024Q3

Original accession **0001992519-24-000008**, filedNovember13,2024 forSeptember30,2024, reports `tableEntryTotal=175789` and `tableValueTotal=594` in its cover-summary XML. These are confirmed raw fields, not an extraction substitution. The filing's second embeddedXML information table contains **594 entries**; summing its raw integer `value` fields gives **175,789,004USD** under the applicable nearest-dollar instructions.

The cover and table therefore conflict. Cause is undetermined; no automatic correction or wrongdoing inference is made. The raw cover observation remains preserved but is marked **quarantined_internal_inconsistency**, unusable for comparison. The separately labelled count/sum reconciliation is recorded within that observation. This narrow reconciliation was performed because the cover anomaly was detected; other information tables were not position-by-position audited during this bounded cover-summary stage.

The original [complete submission](https://www.sec.gov/Archives/edgar/data/1992519/000199251924000008/0001992519-24-000008.txt) is preserved at `evidence/fin-1992519-0001992519-24-000008.txt`. This discrepancy should remain an explicit conflict in the consolidated register and receive independent QA.

### Period and amendment caveats

The August13,2026 amendment **0001992519-26-000006** concerns **June30,2024**, amendmentNo1, typeNEW HOLDINGS, notJune2026. It reports536 new entries and146,855,443USD on its own summary. Its latest filing date does not make it the latest portfolio period.

The latest original holdings report in the retrieved history is **June30,2026**, accession0001992519-26-000007, filedAugust13,2026, reporting768 entries and412,064,875USD. No September30,2026 Form13F appears in that retrieved response. As ofNovember4,2026, the standard45-day quarter-end filing window has not elapsed; the absence should not be labelled delinquency. GeneralInstructions1 and3, physicalp1, describe that filing window.

Earlier cover pages sometimes retain SEC file number802-125863, while later pages report801-130798. The exact value as filed is retained in each observation. Registration history and any stale-field interpretation require separate evidence; these are not interchangeable identifiers silently rewritten across history.

## FormD observations reused without downloading duplicates

Nine cumulative offering observations from original full submissions are included in the same observations JSON: four for each EP Third Moment feeder and one initial Ophir master notice. Their source documents/hashes remain in `sec-sources.json`.

|Issuer|Filed|Accession|Cumulative soldUSD|Reported investors|
|---|---|---|---:|---:|
|Ophir Partners Master Fund Ltd|2012-08-01|0001555295-12-000002|0|0|
|EP Third Moment Fund, LLC|2024-03-22|0002016250-24-000001|15,720,000|18|
|EP Third Moment Fund, LLC|2024-06-04|0002016250-24-000002|15,720,000|18|
|EP Third Moment Fund, LLC|2025-03-14|0002016250-25-000001|47,245,000|21|
|EP Third Moment Fund, LLC|2026-03-12|0002016250-26-000001|62,545,000|23|
|EP Third Moment International, LP|2024-03-22|0002016251-24-000001|10,946,314|12|
|EP Third Moment International, LP|2024-06-04|0002016251-24-000002|10,946,314|12|
|EP Third Moment International, LP|2025-03-14|0002016251-25-000001|34,750,715|17|
|EP Third Moment International, LP|2026-03-12|0002016251-26-000001|47,973,695|18|

Each amount is the issuer's cumulative amount sold in that notice. Do not sum amendments, treat cumulative proceeds as currentNAV, or infer unique natural-person investors. No separate measurement date is stated; filing date is preserved independently rather than silently converted to a measurement date. Ophir's2012 notice reports first sale yet to occur; zero at that time does not show permanent failure to raise funds.

## Limits and next work

The observations JSON contains **21 observations**:12 cover summaries (one quarantined) and9FormD notices. This stage does not estimate fees, carried interests, ownership income, flows or performance, reconstruct amended holdings, or audit the remaining information tables. The original complete submissions retain those tables for subsequent work. This bounded collection is complete against the retrieved15-filing EntryPoint submissions list; broader full-career financial coverage remains dependent on additional entities and historical records.
