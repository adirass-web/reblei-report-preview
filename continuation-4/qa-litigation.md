# Independent QA: round 4 investment-litigation packet

Reviewed November 4, 2026. Scope: finalized `continuation-4/investment-litigation/` report, five claims, thirteen preserved sources, fifteen search-log records and remaining-instructions queue. This is a read-only source/claim review, not a fresh court or agency search. No browser, live query, NYSCEF session or other worker file was opened or changed. Only this QA note was written.

**Result: passed. No material source, identity or claim-scope correction requested.**

## Preservation and references

Independently recomputed SHA-256 for all **13 file-backed source entries**; every value matches its preserved file, including the search-register source. All five claims reference existing source IDs. The source count, five-claim count and fifteen-log count agree with `verification.json`.

The fifteen logs comprise seven Parallel Search batches with **21 recorded queries**, six CFTC target queries, one positive control and one NY Law Reporting Bureau access attempt. The indexed batches are retained as discovery records, not original case proof. No prior exact FINRA 15-02816 query is presented as a new search in those batches.

## CFTC native-query observations

Parsed each original saved CFTC HTML response locally and compared the query URL to its `input[name=keys]` value. Each of the six responses echoes the intended quoted phrase: Scout Trading, Ophir Partners, EntryPoint Capital, Inferent Capital, MEB NY and Michael Edward Bleich. Each displays **Displaying results 0 - 0 of 0**. Their request records report HTTP 200.

The separately preserved positive control echoes unquoted JPMorgan and displays **Displaying results 1 - 10 of 144**, also recorded as HTTP 200. It establishes that this form returned populated content-index results for the control. It does not establish completeness for other terms or equate a content-index no-hit with absence of CFTC, NFA, state or personal proceedings.

LIT5-C01 and the report retain those limits. Inferent is explicitly queried as an unverified affiliation branch, and the control is classified separately from subject evidence. No all-agency clearance or adverse-history inference is added.

## Original New York candidate screening

Independently extracted all pages of each PDF and the entire original SCIP HTML text, normalized whitespace/case and screened the seven stated target terms: Bleich, Scout, Ophir, Finch, MEB NY, EntryPoint and Inferent. No target match occurs. Every PDF page contains extractable text; the screen was not performed on empty pages or cover text alone.

| Candidate | Verified original identity | Actual scope | Result |
|---|---|---|---|
| Aalii Fund, LP v Industrial & Commercial Bank of China Financial Services LLC | 2023 NY Slip Op 31233(U), April 18, 2023, Index 652446/2022 | All 6 physical PDF pages | No stated target term; remains excluded/unjoined. |
| BEC Capital, LLC v Bistrovic | 2017 NY Slip Op 30217(U), January 27, 2017, docket 153737/2016 | All 10 physical PDF pages | No stated target term; remains excluded/unjoined. |
| Millennium Consolidated Holdings, LLC v Bluefin Capital Management LLC | 2023 NY Slip Op 31271(U), April 17, 2023, Index 656387/2022 | All 10 physical PDF pages | No stated target term; remains excluded/unjoined. |
| Citigroup Global Markets Inc. v SCIP Capital Management, LLC | 2026 NY Slip Op 00081, January 13, 2026, Appellate Division First Department | Complete original court-hosted HTML | No stated target term; remains excluded/unjoined. |

The three PDF covers expressly state that they are uncorrected and not selected for official publication. The report correctly distinguishes official court hosting from that publication designation. The SCIP original is a published-opinion response, not a challenge page or an award docket for the subject.

These exclusions support the absence of the specified terms from the retrieved original texts. They do not adjudicate every possible indirect relationship or establish that every docket attachment was screened. No candidate is promoted to the subject's history through a similar investment caption or a name-only join.

## Access and legal-status boundaries

The preserved Law Reporting Bureau interface response is for `https://iapps.courts.state.ny.us/lawReporting/Search`, reports HTTP 403, and has title **Just a moment...** with an Enable JavaScript and cookies message. The log explicitly says no name query was submitted and no results were obtained. This interface is separate from NYSCEF. The packet does not claim that the blocked interface returned no cases, and no NYSCEF/CAPTCHA attempt was repeated in this review.

The report/claims preserve that no new responsive subject proceeding was established. No firm outcome becomes a Bleich personal sanction. Keith Michael Bleich, the unlinked AC Scout/Newedge matter, unrelated namesakes and personal civil cases remain excluded. Inferent search coverage does not establish an individual affiliation.

FINRA 15-02816 confirmation, vacatur, appeal, satisfaction and payment remain unresolved. Nothing here proves the award's present legal effect or that a search exhaustively cleared later proceedings. The remaining-instructions queue requires a fresh party-linked official record and preserves distinctions between payment obligations and actual satisfaction, firm proceedings and individual sanctions, discovery leads and authenticated originals.

The completed checks support the packet's five bounded claims. They do not constitute comprehensive court, agency, registration or employment clearance. No live access was needed for this QA.
