# Independent offline-front review

Reviewed 2026-11-05. Scope: presentation/work/build_front.py, assets/report.js, assets/report.css, nine generated HTML pages, build.json, the approved offline-report-design.md and the corresponding current dossier/index inputs. No web research, browser operation, HTML regeneration, evidence edits or commits were performed. Only this review file was written.

## Finding resolved on re-review

**P2, resolved: Supplemental direct source links bypassed the retained-HTML download guard.** In presentation/work/build_front.py line 216, claim details construct retained-file anchors manually with target=_blank. Unlike Markdown links handled by render() at lines 111-115, these anchors receive no download attribute for HTML/HTM/JS source files. The generated CORP2-ENTITY-3458887 claim has an ordinary link to ../continuation/corporate-ownership/evidence/CORP2-BROWSER-3.html in its Filing identifiers and direct source links detail. That preserved response contains script markup (including /Ecorp/JS/jquery-1.7.1.js). A reader can therefore navigate to and execute preserved response HTML in another document, outside the report document CSP. This contradicts the implementation's own guard and the requested safe handling of retained source responses. Apply a common source-link policy to both generated and Markdown evidence links: download executable response types, or offer an escaped text preview. Retain original evidence bytes. Verification: all supplementary HTML/HTM/JS source anchors should have the same safe behavior as their document-catalogue links. No source script was executed during review.

Resolution check: The updated builder now adds download for HTML/HTM/JS at lines 221-222 and states that these responses download. Re-read regenerated claims.html: all 106 retained executable-type anchors have download; zero omissions. The nine generated HTML pages contain zero inline style attributes, and table alignment uses local CSS classes. No remaining actionable source/code defect was identified in this bounded review.

## Verified fidelity and preservation

- All 247 generated claim articles contain their exact current index statement, evidence_status and review_status: zero missing exact-field comparisons.
- Independently recomputed SHA256 for all 396 indexed retained files; all match the index. This verifies preservation, not the truth of filed assertions.
- All ten input hashes recorded in presentation/build.json match current input files.
- Checked consequential claim records: EVT-C001; INF3-C005; EP5-C003, C004, C005, C006, C010 and C011; CORP5-C005. Exact qualification/status wording is retained, including firm versus personal responsibility, conditional Inferent affiliation, the three administrative withdrawals, procedural-inference limits, MEB identity uncertainty, financial discrepancy and unknown measurement date.
- The claims HTML preserves the later qualification for ID-C012. Conflicts HTML preserves current-reading notes for EVT-X001 and EVT-X002, preventing historical missing-original text from replacing the later recovered-order interpretation.
- Document detail retains source classification, authority, filing/period information, retrieval time, hash, source URL, local file and escaped metadata. All 396 entries remain representations, including failed responses and derivatives, rather than a purported unique-filing count.

## Code assessment against design

The report is the entry page. Existing reviewed narrative and follow-up prose are rendered rather than rewritten. Draft diagrams remain separate and explicitly awaiting selection. Claim/document navigation uses the existing stable SHA256-derived anchors. Claim facets preserve all exact statuses and clearly label UI topic groups and linked date basis. Null subjects display as No assigned subject. No confidence scores, overall risk rating or career/litigation clearance are added.

The application has local assets and static pre-rendered content, no network fetches, service worker, reviewer storage or mutable decisions. Markdown text is escaped; only explicit dossier anchors and line breaks are admitted as raw HTML. Generated local links are resolved inside the investigation package and checked for existence at build time. The supplemental executable-source navigation exception identified above has been corrected and rechecked.

Filter code combines search terms and selected facets, reports displayed-record counts, retains a clear zero-result state, and clears filters when a deep-linked target is hidden. Native HTML remains usable without JavaScript. Print code opens details and restores their prior state afterward. Print CSS keeps hidden records hidden, repeats table headers and removes navigation/filter controls. Visible source IDs, complete locators and qualifications remain in record content. Physical PDF page fragments are created only from an explicit recognized physical-page pattern and a valid page range; other locator wording stays visible. No invented CSV-row convention is introduced.

## Verification limits

This was an independent source and generated-output review. Actual file:// opening, disabled-network behavior, keyboard/narrow-window use, PDF-viewer behavior and printed layout must be judged from the parent's separate real-browser checks. The review does not certify runtime behavior from code inspection alone. Build-time path validation protects this complete snapshot; a later user deletion of a source file still produces the browser's missing-file behavior rather than a custom in-page unavailable-record message.

