# Cross-QA: employment and Inferent continuation 2

Reviewed November 4, 2026. Read-only review of the two workstreams; only this QA note was written. No new web research, legacy root PDFs/ZIPs, shared-index edits or other-worker edits were performed.

**Result: no blocking evidentiary or integrity issue found in the reviewed reports and claims.** The two workstreams preserve the difference between a successful public query, an original historical firm disclosure, an inference, and an unavailable individual history.

## Employment

- Independently recomputed all9 file-backed source SHA256 hashes from employment/sources.json; all matched. All5 claims reference existing source IDs, with no duplicate source IDs.
- The three preserved FINRA/IAPD API JSON files contain exactly a zero total and empty hit array. Their source records distinguish HTTP200 retrieval from the separate SEC catalog403. These records support successful bounded public-query observations, not absence of a historical CRD record or adverse-event history.
- Inspected the preserved original BrokerCheck application JavaScript. fetchIndividual(n) contains the same individual route and literal query=john parameter used in the recorded client requests. The apparently odd parameter is therefore supported by current public-client code, rather than an invented subject-name search.
- Read the preserved FINRA methodology text and checked its official HTML source hash. The policy explicitly discusses continued public inclusion for ten years after termination and listed conditions afterward. EMP3-C5 and the report make retention only a possible explanation; they do not establish the subject's departure/termination date, which condition applies, or why this subject has no public result.
- The earlier third-party September2014 date is expressly excluded as an official premise. A firm's termination date is not substituted for the individual's departure. Registration history, last-FormU4 employment history and actual employment dates remain distinct.
- The Wayback result is correctly restricted to the exact URL and stated filters. It is not generalized into absence from all archives. No employment date is upgraded.

## Inferent

- Independently recomputed all19 file-backed source SHA256 hashes from inferent/sources.json; all matched. All7 claims reference existing source IDs, with no duplicates.
- Read the original mapping CSV using its compatible Windows encoding. Its actual rows give CRD292027, SEC801-112741, brochure288939 version2 filed7/5/2018, version3 filed8/31/2018, and version4 filed3/6/2019, with the exact filenames in INF3-C001.
- Confirmed the preserved SEC archive HTML contains the relative fourth-archive link /files/adv-brochures-2018-may-december-4-4.zip. The relative link resolves to the recorded SEC URL; it is not a newly guessed archive name.
- Independently parsed all four preserved ZIP end-of-central-directory tails. The central-directory byte counts match the four separately retained directory files:262965,263691,264507,240526 bytes. The fourth directory identifies both exact mapped PDF member names and local offsets278706760 and279008713.
- Independently decompressed each preserved local-header/compressed-data range and compared the resulting bytes to the retained original PDF. Local-header and central-directory CRC32, compressed/uncompressed sizes, names and offsets agree. JulyCRC32=8f5e96dd; AugustCRC32=12133766. JulyPDF SHA256=0cce00242ba1d17c86c95a40e20a0fbe6b546bcb00f9c9cfd357445f1f81f326; AugustPDF SHA256=6727029c5b844f1a118081685f0b5641bf42517f918bf8aa49d2ef73d5ee2cbd. Acquisition manifests record HTTP206 for these supported original archive ranges.
- Independently opened both PDFs. July has14 physical pages; physicalp2 states the120-day registration update and begun regulatory-asset management; physicalp4 states approximatelyUS$31,250,250 client AUM. August has15 physical pages; physicalp2 states new funds since the previous filing; physicalp4 states approximatelyUS$62million regulatory AUM. Report/claim physical-page locators and the distinction in AUM terminology are accurate.
- Fresh text extraction from every original PDF page contains neither Bleich nor Ophir, case-insensitively. The report correctly restricts this finding to document text and does not turn brochures into complete employee rosters. No Bleich role, employment period, ownership or Ophir merger/succession is inferred.
- The2019-directory-log.json contains eleven timeout attempts. The mapping establishes the March2019 row/filename; it does not establish successful retrieval. The report and INF3-C007 correctly retain the original2019 PDF as unavailable in this pass and distinguish the earlier transformed capture.

## Evidentiary boundary

The user's permission for clearly labeled inference from official records is respected. The employment retention inference is conditional and does not use an unverified individual departure date as a factual premise. Inferent's strategy/date compatibility is not promoted into an affiliation or merger. Third-party role and merger accounts remain leads. Claims in both reviewed packages are consistent with the preserved evidence and their stated limitations.

## Narrow follow-up QA: Inferent Client/Master wording

Reviewed the new Material fund-name ambiguity report section and INF3-C008 after the worker's patch-complete notice. Independently checked both newly indexed source-file hashes: the reused original March6,2019 Part1 ADV (82e13f1df9b44887cb458b5e50b0c6b96e7311854e7422c44421486493dc1e0c) and the separately labeled derived August2018 physicalp4 render (36fc61e9a4eda3c9e4abb44bbb0b4b939ddaf05370aa433d885a57a1cd3ebcea). Both match their manifest entries.

Visually inspected the preserved August2018 p4 render. It indeed introduces Inferent QE Client, LP as the Client, followed by a paragraph beginning The Master Fund. Independently read physicalp19 of the reused2019 ADV: the private-fund block gives INFERENT QE MASTER FUND, LP, identification805-6736389159, with INFERENT QE, LLC as general partner. The cited physical pages and literal labels are accurate.

INF3-C008 correctly treats this as verified wording ambiguity with identity unresolved. It selects no drafting-error, rename, succession, separate-entity or identity-equivalence explanation, and adds no Bleich role or Ophir linkage. No evidentiary blocker found.

The original2019 retrieval gap continues to concern the **March2019 Part2A brochure**, not the separately preserved/reused March2019 Part1 ADV. Report wording in the retrieval-limit paragraph should keep that distinction explicit when quoted or summarized. INF3-C007 already identifies the brochure correctly. This follow-up checks the two added sources and claim; it does not claim a fresh complete-manifest hash audit after the prior28-file audit.
