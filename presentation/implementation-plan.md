# Offline report front Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for inline implementation and one independent review of the complete result.

**Goal:** Open the reviewed report, searchable dossier and follow-up instructions offline from presentation/index.html.
**Architecture:** Generate static linked HTML pages from the reviewed Markdown and normalized index. Local CSS and one small script progressively enhance filtering, deep links and printing. Originals stay in their existing paths; there is no browser data fetch, server, storage or framework.
**Tech Stack:** Python 3 and installed markdown-it-py 4.2.0 for generation; browser HTML/CSS/JavaScript for reading.
**Spec:** offline-report-design.md, approved by the user; implementation authorized November 5, 2026.

## Global constraints
- Same research/bleich-local-migration-2026-11-04 branch and investigation folder; no main merge or hosting.
- Exact reviewed narrative, assertions, locators, metadata, qualifications and originals remain authoritative. Do not revise research.
- Offline, read-only, report-first. No network dependencies, telemetry, reviewer storage, accounts, server or runtime installation to read.
- Preserve stable c-/d-/x- dossier anchors and record IDs. Encode local paths, confine them to the investigation, and escape source text.
- Do not select an unapproved diagram. Offer the six existing drafts separately as review assets.
- Retain all current gaps and source-specific dates; no risk scores or clearance claims.

## Review focus
- Fragment navigation must reveal a claim/document even after filters hid it.
- Failed responses and unjoined sources must remain labeled; no inferred date or misleading verified count.
- Unsafe source HTML or path traversal must not become executable links.
- Keyboard/narrow-window/print behavior must remain readable with no network and no JavaScript.
- Generated output must preserve editorial corrections that are absent from raw index rows.

## Tasks
- [x] 1. Freeze input hashes and metadata at source commit 556b60ea6d21650d3105bbdb84e3821c629ba1d5; write presentation/work/validate_front.py covering page presence, source/claim/link coverage, offline resources, IDs and originals. First run must fail because the front is absent.
- [x] 2. Create presentation/work/build_front.py, requirements.txt and assets/report.css. Render reviewed report and remaining instructions; generate claims/documents from index with exact metadata and existing editorial annotations. Render current appendices into linked HTML. Generate provenance/about and opening instructions. Check source fingerprints and link targets.
- [x] 3. Add assets/report.js: progressive search and select filters; displayed record count; reset; fragment reveal; print current view. Do not store state or fetch data. Hidden records must remain excluded from filtered print, and hash links must work with JavaScript disabled.
- [x] 4. Exercise file:// with networking disabled in installed Chromium, using local Playwright. Test filters, deep links, source PDF opening, keyboard focus, mobile overflow and printed report. Save bounded screenshots and verification JSON under presentation/review. Independent reviewer checks fidelity and implementation; resolve consequential findings.
- [ ] 5. Update continuation guidance; repair package sealing to exclude Git-ignored runtimes/caches. Seal and hash the complete investigation. Commit intended paths, push same branch, verify remote blob hashes and unchanged protected refs. The complete investigation folder is the offline delivery bundle; no redundant archive copy is needed.

## Decisions and progress
- Approval already supplied; no new approval gate is needed for this implementation.
- Keep the reviewed dossier chapter order and exact prose rather than renumbering its financial/events sections to match the earlier design sketch.
- Existing visualization drafts are available through separate links, not embedded as selected findings.
- Keep generation, tests and evidence within presentation/. Preserve current raw and Markdown files byte-for-byte.

Release checkpoint: offline implementation and independent fidelity/browser checks completed. The additional modern-web-guidance, design-html and design-review pass requested later has not been performed; user instructed sealing the current package. Separate visualization/design work remains untouched and excluded from this release manifest until its owner commits it. Stage intended files, then use `python work/seal_package.py --tracked-only` to seal this shared-checkout milestone.

November 5 follow-up: requested three-skill review completed within the offline/read-only scope. Technical accessibility changes validated; substantive issues S1/S2 remain unimplemented pending approval. See review/design-audit/review.md.
