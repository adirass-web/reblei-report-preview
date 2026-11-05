# Inferent continuation 3: original initial brochure and historical registration rows

Research date: November 4, 2026. This stage recovered Inferent's initial March 2018 brochure and original historical Form ADV tables. The new records document an initial SEC application and six historical filing snapshots. They do not identify Michael Edward Bleich as an Inferent employee, owner or officer, and they do not establish an Ophir-to-Inferent merger.

## Original initial brochure

The official January-April 2018 archive, part 7, contains member `292027_288939_1_20180301.pdf`. Its 14-page original prints March 2018 on physical page 1; the exact day is supplied by the archive filename and, independently, the historical filing row for March 1, 2018. Item 2, physical page 2, expressly describes the firm's initial Part 2A submitted with its registration application. Item 4, physical page 4, reports no current client assets under management and anticipates sufficient assets within 120 days **of the effective date of initial registration**. This is not a 120-day period measured from the brochure filing date. [INF4-C001/C002]

The entire freshly extracted original contains neither Bleich nor Ophir. This is a bounded document-text result, not an employee roster or proof of nonemployment. The brochure names Marc Rieffel as CCO on physical page 1. It supplies no affirmative Bleich role or transaction evidence. [INF4-C003]

## Historical Part 1 filing evidence

The SEC's historical Part 1 archive contains an original `IA_ADV_Base_A_20111105_20241231.csv` table. Matching the exact CRD field, `1E1`, to `292027` produces six Inferent rows. Joining by the exact `FilingID` to the original filing-type table gives:

| Filing date as submitted | FilingID | Recorded type | Item 4A | Item 5A employees |
|---|---:|---|---|---:|
| March 1, 2018 | 1166838 | Initial SEC registration request | N | 3 |
| April 25, 2018 | 1212685 | Other-than-annual amendment | N | 3 |
| July 5, 2018 | 1227321 | Other-than-annual amendment | N | 3 |
| July 30, 2018 | 1231177 | Other-than-annual amendment | N | 3 |
| August 31, 2018 | 1237606 | Other-than-annual amendment | N | 3 |
| March 6, 2019 | 1278683 | Annual updating amendment, fiscal year 2018 | N | 8 |

All six identify Inferent Capital, LLC, SEC file 801-112741, CRD 292027, with Marc Rieffel as signatory titled CTO/CCO. Item 4B is blank throughout. This is the retrieved Base A table's coverage, not a claim that every filing type, withdrawal or regulatory event appears in that table. The source's submission timestamps have no timezone designation; they are retained exactly without conversion to UTC. Capture timestamps are separately recorded in UTC. [INF4-C004]

The original Schedule D section 4 table has no row matching those six FilingIDs. Crucially, Item 4A asks whether the adviser is succeeding to another registered adviser's business **at the time of this filing**. The reused original March 2019 ADV, physical page 7, also instructs filers not to repeat a succession already reported on an earlier filing. Therefore these N answers and missing Schedule D rows establish only the absence of a succession disclosure in these six retrieved filing snapshots. They do not prove that no corporate agreement, personnel move, strategy transfer or other transaction occurred. No Ophir merger or legal succession is inferred. [INF4-C005]

The original 120-day representation table has entries for Inferent FilingIDs 1166838 and 1212685, each with both representation fields marked Y. This supports the initial-registration context alongside the initial brochure. The employee totals in the table identify no employees and cannot supply Bleich's hiring or departure dates. [INF4-C006/C007]

## Coordinated target rows and a separate EntryPoint ambiguity

As authorized, the same original Base A table was filtered for Ophir CRD 164729 and EntryPoint CRD 313946 without a second bulk retrieval. The resulting 14 Ophir rows and two EntryPoint rows are preserved in a clearly labeled derivative extract. Ophir professional-role interpretation was handed to the employment worker; it is not substituted for an Inferent employment join here.

The two EntryPoint rows retain the **same CRD 313946**, but differ in legal-name and SEC-file-number fields: July 12, 2021 reports ENTRYPOINT CAPITAL / 801-122062; June 27, 2024 reports ENTRYPOINT CAPITAL, LLC / 801-130798. The original filing-type table marks Initial SEC Registration Request=Y for both FilingIDs. For the June 2024 row, it additionally marks the separate Final SEC ERA Report field Y; the July 2021 row leaves that final-ERA field blank. Those dual 2024 flags are retained without choosing an interpretation. Those are exact database-field facts. This stage does not establish a corporate rename, reorganization, succession, dissolution or a reason for the SEC-number change. The table is not a complete ERA filing history. The discrepancy is explicitly retained for further official record comparison. [INF4-C008]

## Original-byte preservation and efficient retrieval

The exact official archive links came from the previously preserved original SEC archive HTML. Initial 65,536-byte suffix requests returned HTTP 206 headers but stalled during body reads; those failure logs remain preserved. Using the server-declared archive sizes, explicit absolute 22-byte end-record requests and central-directory ranges succeeded for all seven January-April archives. Only part 7 contained a CRD 292027 PDF member. The PDF's local/central member name, CRC32, uncompressed size and SHA256 are verified. No entire brochure archive was downloaded.

For the historical Part 1 data, two tiny archive end records/directories located the needed members. Three small original CSV payloads were retained directly: filing types, Schedule D section 4 and the 120-day representation table. Each passed CRC32 and size verification.

The Base A original is larger: 95,465,915 bytes as an exact ZIP local member and 533,213,713 bytes expanded. Its exact compressed local member is preserved under `raw/`, below 100MiB; redundant range chunk binaries were replaced by that byte-identical concatenated member, with range offsets and chunk hashes retained in request logs. The local-header path equals the central-directory path; the saved local artifact uses its basename for convenience. Deterministic reconstruction verifies CRC32, size and uncompressed SHA256. The expanded CSV is a work cache outside this investigation, not a deliverable or proposed ordinary Git file. The target-only JSON extracts are derivatives, not original SEC responses. [INF4-C009]

No 2019 brochure archives were retried. No NYSCEF, accounts, purchases, private litigation, outreach or shared Git/index modifications were used. `sources.json`, `claims.json`, `search-log.json`, request logs and `checksums.json` preserve provenance and limitations.
