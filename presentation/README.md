# Offline report and evidence dossier

Open **[index.html](index.html)** in a desktop browser. No installation, server or internet connection is needed. The first page is the reviewed report; the dossier, follow-up instructions and version details are in the top navigation.

When sharing, copy the **complete `investigations/2026-11-04-official-records` folder**, preserving its subfolders. Do not send only `presentation/`: source evidence remains in its original relative locations. A clone or download of the research branch contains the complete folder. Nothing is hosted or published by this deliverable.

The reader is read-only. Searches and filters affect the current view and save no notes or decisions. Use stable claim/document IDs in the team's existing review process. Clear filters to return to the full catalogue. “Print this view” prints the current page and, on dossier lists, the displayed records and their details.

## Included

- The complete reviewed narrative, with links to the supporting claims.
- All 247 registered claims, 444 evidence links, 396 source representations and 26 conflicts/qualifications.
- Searchable claim/document catalogues, exact evidence-status filters, entity/source/date-basis filters and stable detail anchors.
- Linked entities, roles, financial observations, events and separate follow-up instructions.
- Local retained evidence links, original online URLs, exact locators, dates, retrieval times, identifiers and SHA256.
- Separate links to six unselected visualization drafts. No draft has been silently promoted into an approved report figure.

Counts include conditional assertions, access observations, derivatives and failed responses. They are not counts of verified facts or unique filings. Research cut-off: November 4, 2026. All research inputs and indexed evidence bytes are unchanged.

## Source and print behavior

Online source links are marked “online” and require a connection only when selected. Preserved HTML/JavaScript responses download as source files rather than run within this reader. Some binary records are compressed members; read their preservation metadata before use.

Physical PDF page links are added only where the locator explicitly supplies physical page numbers. The full locator stays visible because PDF viewers differ. Headless Chromium retrieves PDFs as downloads; the acceptance check verified the downloaded bytes against the original. Desktop browsers may display them in a PDF viewer.

Printing retains source IDs and qualifications. The report print sample is 16 A4 pages; local printer settings and browser pagination may differ. Text and evidence links remain usable with JavaScript disabled; browser Find replaces the interactive filters.

## Maintenance and checks

The HTML is a generated view, not a second research database. Do not edit generated pages by hand. `work/build_front.py` reads the reviewed Markdown and normalized index; it pins and checks ten inputs against source commit `556b60ea6d21650d3105bbdb84e3821c629ba1d5`, then checks all indexed source hashes. A deliberate future research revision needs an updated reviewed input commit and renewed validation.

From the investigation folder, using Python 3 with `markdown-it-py==4.2.0`:

```text
python presentation/work/build_front.py
python presentation/work/validate_front.py
python work/seal_package.py
```

Validation additionally uses Beautiful Soup. Browser acceptance uses Playwright (`node presentation/work/check_browser.cjs` with a locally installed Playwright module, or `PLAYWRIGHT_MODULE` pointing to it). These are maintainer tools; readers need only a browser. The script runs `file://` with networking disabled, checks navigation, filters, fragment reveal, keyboard access, all nine pages at a narrow viewport, no-JavaScript reading and print output. It does not fetch official sites.

Evidence: [build metadata](build.json), [static checks](review/static-validation.json), [offline browser checks](review/browser-validation.json), [independent review](review/independent-review.md), [report print sample](review/report-print-sample.pdf) and [filtered claim print sample](review/claim-print-sample.pdf).

The complete checksum manifest is [../SHA256SUMS.txt](../SHA256SUMS.txt). Package sealing includes all tracked and non-ignored deliverables; ignored local visualization runtimes and caches are not distributable source evidence.

## Evidence-status wording

Plain-English labels are reviewed presentation aids beside the unchanged recorded status. The evidence-status filter uses those labels but retains exact original values; statuses are never merged. The evidence review, independent check and withheld exceptions are preserved under `review/status-label-*`. The earlier automatic proposal is historical drafting material and must not be applied directly. Build metadata pins the reviewed mapping hash.
