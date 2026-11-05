# Exact-ID historical employment and Inferent disclosure scan

Research date: November 4, 2026. Subject: **Michael Edward Bleich, CRD 4262671**. Keith Michael Bleich, CRD 2372764, is excluded. This pass reused newly retrieved official investigation sources; legacy repository material was not read.

**The complete scans of the recovered IA and ERA Schedule A/B files found the subject only in Ophir and EntryPoint disclosure records. No third firm was discovered by exact ID.** The six identified Inferent filings contain no matching subject ID or full name. These are owner/executive-disclosure searches, not proof of all employment or of nonemployment at Inferent.

## Sources and reproducible scope

The four original compressed SEC bulk members were reused by reference. Each expanded work cache was independently SHA-256 checked against the previously CRC/size-verified original. The archive is `adv-filing-data-20111105-20241231-part1.zip`; the date window is the archive/member naming scope, not an assertion that it contains every possible professional record. No archive was downloaded again.

| Recovered source family | Schedule A/B data records scanned | Exact OwnerID 4262671 rows | Matched FilingIDs | Base records scanned |
|---|---:|---:|---:|---:|
| IA | 3,147,383 | 31 | 15 | 471,129 |
| ERA | 469,754 | 13 | 5 | 72,618 |

Every IA exact-ID match has type I and the full name BLEICH, MICHAEL, EDWARD. Exact matched FilingIDs were joined to the corresponding Base table, retaining firm CRD, firm/file names, submitted date, execution date and signatory capacity. IA and ERA exports remain separate. FilingIDs **663868** and **1869875** occur in both; five original-field rows are identical across families. Thus **44 raw matches represent 39 distinct field-value disclosures across 18 unique FilingIDs**, not 44 separate roles or events. See EMP5-C01/C02.

CSV record ordinals are one-based data-record positions excluding the header, rather than assumed physical line numbers. Latin-1 was used as a reversible parser for the original CSV bytes. Expanded files remain only in workspace work caches. Derivatives preserve the original target fields and source record ordinals; they are not presented as original regulator files.

## Firm and role results

The exact-ID joins resolve only to **Ophir Partners LLC, CRD 164729**, and **EntryPoint Capital, LLC, CRD 313946**. They do not cover every broker record, research employee or possible historical affiliation.

The ERA scan adds an earlier retrieved Ophir snapshot: **FilingID 656739, submitted August 1, 2012**, with SEC-file field **802-77010**. Its Schedule A lists Bleich as **CEO**, acquired-status **04/2012**; Schedule B lists him as **OWNER in MEB INC**, acquired-status **05/2009**. The latter belongs to the named intermediary relationship, not an Ophir employment start in May 2009. The filing's execution date, July 31, 2012, is retained separately. This earlier source confirms a dated disclosure; it does not independently date employment or establish legal registration status. See EMP5-C03.

The IA Ophir rows repeat the already reviewed 2012-2017 history. The previously preserved MEB INC/MEB NY INC mismatch and combined CEO/CCO date limitations remain unresolved; this scan does not silently repair them or introduce a role-end date.

For EntryPoint, the subject appears in ERA FilingIDs **1782387** (November 22, 2023), **1834697** (March 27, 2024) and **1869875** (June 27, 2024); the last is also in IA. Each reports **Chief Investment Officer**, acquired-status **05/2023**, and **MEMBER of EntryPoint GP LLC** plus **LIMITED PARTNER of EntryPoint Partners, LP**, acquired-status **07/2023**, Code C. Code C means 25% but less than 50% in the specified relationship, not an exact combined personal stake. These dates do not settle the separate earlier-employment lead. The parent EntryPoint workstream owns registration/ERA/withdrawal chronology and its interpretation. See EMP5-C04.

## Inferent: complete identified filing extracts, bounded no-match

All Schedule A/B rows for the six specified Inferent IA FilingIDs were extracted, not merely searched for a name. Exact Base joins identify firm **292027**:

| FilingID | Date submitted | Schedule A/B records | Bleich ID/full-name matches |
|---|---|---:|---:|
| 1166838 | March 1, 2018 | 2 | 0 |
| 1212685 | April 25, 2018 | 3 | 0 |
| 1227321 | July 5, 2018 | 3 | 0 |
| 1231177 | July 30, 2018 | 6 | 0 |
| 1237606 | August 31, 2018 | 6 | 0 |
| 1278683 | March 6, 2019 | 6 | 0 |

The total is **26 rows**. The matching conditions were exact stripped OwnerID 4262671 and normalized full-name orders BLEICH MICHAEL EDWARD / MICHAEL EDWARD BLEICH. No match resulted. An independent whole ERA Base scan found **zero exact firm-CRD 292027 rows**, so that source supplied no additional Inferent ERA FilingIDs to extract. The empty ERA derivatives document that scoped result; they are not evidence of a missing firm in all regulator holdings. See EMP5-C05.

The original Form ADV instructions distinguish these owner/executive-officer schedules from a complete employee roster. Therefore the no-match **does not disprove an employee or head-of-research role**. Inferent remains a conditional affiliation branch pending direct dated evidence; this pass adds no Bleich-to-Inferent relationship. See EMP5-C07.

The filing snapshots themselves show a disclosure structure change: the first has Jose Marques and Marc Rieffel rows; the next two also have James Pak; the later three additionally list Inferent Advisory Holdings, LP as OWNER, Reflexive, LLC as its GENERAL PARTNER and Marques as OWNER in Reflexive. This is a conditional firm-record observation, not a Bleich ownership or employment finding, transaction-date proof or exact economic stake. See EMP5-C06.

## Narrow biography search and remaining gap

A targeted Parallel Search batch sought an original institutional/employer early-career biography. It returned already known professional leads and unrelated namesakes; no new primary source with explicit Chase/Lehman employment dates was obtained. Unrelated nursing biographies, personal/contact aggregators and unrelated people were excluded. No blocked individual PDF or 2015-2017 archive request was repeated. This limited result does not establish source absence. See EMP5-C08.

The parent separately recovered ADV-W records. Their BusinessCeased answers and stated reasons must be read before treating a regulatory withdrawal as a business closure or employment end; the parent owns those factual claims and independent QA. No withdrawal date is substituted for an employment departure here.

`remaining-instructions.md` specifies the exact remaining record, why it matters, allowed access and completion condition. The full career and Inferent employment questions remain open despite the completed local scans.

## Deliverables and preservation

`sources.json` is a 16-entry array preserving reused original URLs, hashes, acquisition times, archive member identifiers, verification pointers and clearly labeled derivatives. `claims.json` contains eight claims with source-specific evidence locators; `search-log.json` contains the two full local scans, the targeted Parallel search and the overlap comparison. `scan-verification.json` and `era-scan-verification.json` record counts and verified cache digests. All original and derivative hashes and claim references were checked.

No accounts, purchases, outreach, NYSCEF interaction, personal civil-record research or home/family information were used. No shared index, Git state or other worker file was changed.
