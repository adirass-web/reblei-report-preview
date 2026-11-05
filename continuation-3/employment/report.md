# Ophir historical roles, ownership disclosures and brochure gap

Research date: November 4, 2026. Subject: Michael Edward Bleich, CRD 4262671; firm: Ophir Partners LLC, CRD 164729 / SEC 801-77121. Historical firm filings are professional self-reports hosted by the regulator; they are not independent findings that each reported fact was verified by the SEC.

**Newly recovered historical Form ADV data identifies Bleich by his full name and CRD and supplies dated Ophir role and ownership disclosures from 2012 through 2017.** An original Ophir Part 2A/2B career biography was not obtained. The earlier Chase, Lehman and Barclays employment-date gaps remain open.

## Original historical data and exact joins

The Inferent workstream retrieved the official SEC historical Part 1 ZIP's Base A member once. It identifies fourteen Ophir filings through exact field `1E1=164729`, from FilingID **663868**, submitted August 30, 2012, through **1070803**, submitted March 30, 2017. Its original compressed member was reused without downloading it again.

This workstream retrieved the **IA_Schedule_A_B_20111105_20241231.csv** member once using bounded public byte ranges. Joining the fourteen FilingIDs produced **93 Schedule A/B records**, including **BLEICH, MICHAEL, EDWARD**, individual OwnerID **4262671**. Full original compressed member bytes, exact archive/member identifiers, local/central member-name equality, per-range hashes, reconstruction offsets, CRC32, uncompressed size and SHA-256 are preserved. The expanded 337 MB CSV is only in the workspace work cache; the investigation contains compressed source bytes and target-record derivatives.

No EDGAR accession is implied: these are Form ADV historical FilingIDs within an SEC bulk archive. Dates submitted, execution dates, acquired-status dates and employment intervals remain separate.

## Role chronology: what the filings actually say

| Dated disclosure | Schedule A, Bleich CRD 4262671 | Limit |
|---|---|---|
| August 30, 2012, FilingID 663868 | CEO; acquired-status field 04/2012 | Month/year reported for this title/status; not a complete employment history. |
| February 20, 2015, FilingID 863218 | CEO; acquired-status field 04/2012 | A filing snapshot, not proof of when every duty began or ended. |
| March 25, 2015, FilingID 884710 | CEO, CCO; acquired-status field still 04/2012 | The shared date does not separately date the later-added CCO label. |
| December 23, 2015 through March 30, 2017, selected later filings | CEO, CCO; same acquired-status field | The combined role remains disclosed. No departure date is established. |

The Base A execution fields show MICHAEL BLEICH signing the March 25, 2015 filing as CEO and the December 23, 2015 filing as CCO; later selected filings also use CCO. That signature capacity does **not** show that he stopped being CEO: the corresponding Schedule A rows disclose both titles. The first retrieved filing with the combined title is a disclosure boundary, not necessarily its actual start date. See EMP4-C04/C05/C06.

## Ownership snapshots and unresolved names

The already preserved original March 2017 Ophir PDF, physical pages 19-20, supplies the code legends: **C = 25% but less than 50%; D = 50% but less than 75%; E = 75% or more**. Schedule A **NA = less than 5%**. These are ranges for the specified entity/relationship. They do not establish an exact stake or personal wealth, and indirect ownership is not converted into an exact combined percentage.

In the earlier retrieved filings, Finch LLC is the direct managing member with Code E. The intermediate MEB entity's interest in Finch is Code D, and NAYS LLC's is Code C. Bleich's OWNER row in the MEB entity is Code E. On March 18, 2016, FilingID **993846** still discloses the D/C intermediate-owner pattern. On June 17, 2016, FilingID **1019291** discloses MEB NY INC's interest in Finch as Code E; no NAYS LLC or Dror Niv row occurs among that filing's Schedule A/B records. The March 2017 filing repeats that later pattern.

This establishes **dated disclosure differences**, not a proved purchase, sale, consideration, exact transaction date or the end of every possible economic interest. The older 04/2012 and 05/2009 acquired-status values persist; they must not be relabeled as dates of a 2016 transaction. See EMP4-C07/C08.

There is also an **as-filed naming mismatch**. From the October 30, 2014 filing **844380** through the March 18, 2016 filing **993846**, the Schedule B entity row says **MEB NY INC** in Finch, while Bleich's OWNER row says **MEB INC** as the entity in which he owns an interest. Earlier retrieved filings say MEB INC in both places; the June 2016 and March 2017 filings say MEB NY INC in both places. No correction, legal rename, same-entity equivalence or corporate succession is assumed. The paired spellings are preserved. See EMP4-C09.

## Historical brochure route and access gap

The exact 2015-2017 archive links came from the original SEC Part 2 catalogue already preserved by the Inferent workstream. It was reused with its original hash/time. New catalogue downloads returned HTTP 403; original failure response bodies are retained.

All ten listed **2017** archive links returned HTTP 403 on their first bounded range requests. Five samples also returned 403: 2016 parts 1 and 3 of 8; 2015 January-February; March-September part 1 of 7; and October-December part 1 of 2. Other 2015/2016 parts were not tested. No central directory or brochure member was obtained from these requests. These failures do not establish absence from the archives.

Two Parallel Search batches and official catalogue extracts did not identify a usable 2015-2017 brochure mapping CSV or another original Ophir biography. The existing March 2017 Part 1 PDF, physical page 20, explicitly lists brochure **247246**, **OPHIR PARTNERS ADV PART 2**, type **Private funds or pools**. This verifies the filing's brochure listing, not its text or version date; that brochure's contents remain unretrieved.

The bulk Schedule A/B request initially returned 403 with a generic research-client identifier. The exact shared public helper/client configuration then succeeded with HTTP 206, without credentials or an account. The failed request is preserved separately. The blocked brochure archives were not retried after the parent directed a stop. No absence conclusion is drawn from either request format's failure.

## Preservation and limits

`sources.json` contains **25 entries**, `claims.json` **9 bounded claims**, and `search-log.json` **60 search/extraction/request records**. `raw/ophir-schedule-ab-selected.json` preserves all 93 target professional rows with CSV record ordinals; `raw/ophir-filing-history-selected.json` preserves the fourteen corresponding firm/date/signatory rows. Derived extracts are labeled and linked to original compressed sources. UTF-8 parsing failed on unrelated non-ASCII rows; Latin-1 was used as a reversible byte-preserving decoder, and all selected Ophir field values were checked to be ASCII. No selected name or identifier was repaired.

The compressed original can be expanded using the preserved local-header length and raw-deflate method; expected uncompressed SHA-256 is `f14378fedd7d5023bb41ab374c6ddd2ddc4361f7e6ab64c8290a53a7e9417e9e`, size 337,743,129 bytes, CRC32 4005770932. Independent source/claim QA is assigned separately.

No FINRA/IAPD individual search was repeated, no NYSCEF interaction occurred, and no accounts, purchases, outreach or private personal cases were used. Legacy repository root PDFs/ZIPs were not read. Shared indexes and Git were not changed. The next remaining career-history source is an actual brochure supplement or historic individual employment record with explicit earlier-employer dates; the new firm-status chronology does not substitute for it.
