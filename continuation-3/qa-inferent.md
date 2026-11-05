# Inferent continuation3 independent QA

Review date: November4,2026. Read-only source review; only this QA note is written. The initial brochure and final Part1 checks below are complete. The original-byte checks and final report/claims pass after the author corrected INF4-C008 filing-type labels.

## Initial March2018 brochure

Independently parsed the retained archive local header and seventh Jan-Apr2018 central directory, located exact member292027_288939_1_20180301.pdf, and decompressed the original preserved member bytes. The local/central headers agree on member name, compressed size302858, uncompressed size334113, CRC32=49877bfe and local offset810287495. The member request range810287495-810590410 contains exactly the header/name/extra fields and compressed payload. The reconstructed payload exactly equals the retained original PDF and matches SHA25629fced0c967b70514e0ed955f702eda9ca76ff3437ce3295c6254b488c0e3a93. The preserved EOCD central-directory size matches the retained seventh directory. The acquisition metadata records HTTP206 from the SEC archive URLhttps://www.sec.gov/files/adv-brochures-2018-jan-apr-7-7.zip.

Independently opened the original PDF:14 physical pages. Physicalp1 prints March2018; the exact March1 day comes from archive/filing provenance, not the printed cover. P1 says the firm applied expecting eligibility for Commission registration within120days. Physicalp2 explicitly calls this the initial FormADVPart2A submitted with its SEC application. Physicalp4 says the firm did not currently have client assets under management and expected sufficient client AUM within120days of the effective date of initial registration. This is not a statement of current later AUM, zero firm revenue, or a deadline measured from the brochure filing day.

Fresh extraction from every original PDF page contains neither Bleich nor Ophir, case-insensitively. Omission supports only a bounded document-text observation. It cannot establish nonemployment, an employee roster, lack of ownership, absence of a transaction, or a merger/succession. No such inference is approved by this QA.

## Final Part1 and preservation review

Final report,93-source manifest and9 claims are now reviewed. **Passed after the author corrected INF4-C008 filing-type labels; the corrected report/claim was independently rechecked.** Independently recomputed all93 file-backed source hashes; all match, source IDs are unique and all9 claim-source sets resolve. The earlier pending-review status above is superseded by this final section.

Independently reconstructed the retained BaseA local member. Its local archived name exactly equals the central-directory path, and the central record matches base-a-verification.json. The saved member is95,465,915bytes:177bytes of local header/name/extra fields plus95,465,738compressed payload bytes. General-purpose flag8 leaves local CRC/size fields zero, so the appropriate validation uses the central-directory sizes/CRC. Decompression yields533,213,713bytes, CRC32c6096a56 and SHA2562d8f0ded7ceae0587e5dc1254350edf5a1c5d351092956993f38d5d440235401, matching the recorded original payload. Independently checked all48 original range-slice hashes against the corresponding offsets in the retained combined member; all match. This confirms that consolidation preserved the original range bytes rather than changing the evidence. The expanded CSV is correctly designated a workspace cache, while the combined compressed member remains the preserved deliverable original.

Independently scanned the full expanded original using exact CRD column1E1. It returns6Inferent rows,14Ophir rows and2EntryPoint rows. Selected identity/date/succession/headcount/signatory fields independently match target-filing-history.json. The six Inferent filing dates/IDs are March1,2018/1166838; April25/1212685; July5/1227321; July30/1231177; August31/1237606; March6,2019/1278683. All name Inferent Capital LLC/SEC801-112741, Marc Rieffel as CTO/CCO signatory,4A=N and4Bblank. Item5A is3in each2018row and8in2019. These are approximate source-defined employee totals excluding clerical workers, not named employee records.

Independently decompressed the three smaller preserved member ranges and compared their expanded bytes to the retained original CSVs. FilingTypes CRC32b9efc486, ScheduleD4 CRC32e65d3882 and120Day CRC32cd62370c all match their manifests. Exact FilingID joins confirm the initial request, four other-than-annual amendments and March2019 annual update for fiscal2018. ScheduleD4 has no row for those six IDs. The120Day table has both representationsY for1166838and1212685.

Read the reused original March2019 ADV physicalp7. Item4A expressly asks about succession at the time of filing, and its instruction expressly says not to repeat a previously reported succession. INF4-C005/report preserve these limits: sixN answers and absent related rows are not proof no merger, personnel move, strategy transfer or other transaction ever occurred. No Bleich employee, owner, officer, appointment or departure inference is added from signatories, totals or omissions. Source DateSubmitted timestamps remain timezone-unspecified; capture UTC is separate.

The same-CRD EntryPoint field difference is correctly exposed. Independent original rows give313946with ENTRYPOINT CAPITAL/801-122062 onJuly12,2021 and ENTRYPOINT CAPITAL,LLC/801-130798 onJune27,2024. Independent original filing-type row1542238 marks Initial SEC Registration Request=Y and leaves Final SEC ERA blank. Row1869875 marks BOTH Initial SEC Registration Request=Y and Final SEC ERA Report=Y. The initial submitted report/INF4-C008 mislabeled the former finalERA and omitted the latter dual flags. QA reported that material label error; the author corrected both report and claim, and QA independently rechecked the saved correction. Exact row flags now remain visible without an invented corporate rename, reorganization, succession, dissolution or SEC-number-change explanation. No incomplete BaseA extract is promoted into a complete ERA history.

No original2019 brochure was newly retrieved; the available originalMarch2019Part1ADV remains distinct. New original initial-brochure and historical table facts strengthen registration context without establishing the unverified Inferent/Bleich affiliation or Ophir merger. No shared index or other-worker evidence file was edited for this review.




Corrected final snapshot digests:

- report.md:4b20f9315bc4fdaaaef5394c88a1e1bc34762bb44a6043eaa175981c81d2f192
- claims.json:71387239eb2251470141eb33589d9d8ee827742e0516e4d21d18e9a477ad0e97
- sources.json:77dfc8464d66e4beb83dd1b07bba3333acfe0f3477f7a09a27825340df7ef833
