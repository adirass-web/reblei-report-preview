# Offline deliverable review — November 5, 2026

Status: DONE_WITH_CONCERNS. Technical refinements complete; substantive presentation choices await approval.

## Scope and skill application
Reviewed all nine HTML pages at 375, 768, 1024 and 1440 pixels, offline. Applied modern-web-guidance accessibility/typography/responsive guides, design-html native implementation principles, and design-review rendered usability checks. The supplied guidance skill version is old; current guides were retrieved through the latest CLI and preserved in modern-web-guidance.md. No global skill/config update was made.

The approved report-first plan and existing screenshots supplied the design context (evolve mode). This is an evidence reader, not marketing. Native browser text flow is retained: the skill's Pretext, contenteditable, remote-font/CDN and local-server defaults conflict with the approved read-only/offline/no-runtime design or add unnecessary machinery. Existing Playwright replaced unavailable gstack binaries. Repo-only artifact storage follows the user's explicit preservation instruction. Separate visualization/design work was not inspected or changed. No telemetry, broad framework installation or unrelated configuration was introduced.

## Rendered baseline
The first impression is a sober professional document. My eye goes first to the subject's name, then scope, then the dossier action. The report/claims/documents/follow-up areas have identifiable purposes. Navigation is consistent across pages. Search is explicit within the dossier; narrative pages use browser Find. Long raw status strings and the opening page's delay before the findings remain usability concerns requiring editorial decisions.

App-UI classification: calm, text-led, one accent, no ornamental imagery/motion. Record containers group individually addressable source records; they are not decorative feature cards. No unsupported risk score was introduced. Subjective design baseline B; final B+ after accessibility refinements. Decorative-pattern assessment A before/after. These are review judgments, not measured quality scores or compliance certification.

## Technical findings and fixes
| Finding | Before | Fix and evidence |
|---|---|---|
| Mobile text | 15px body | 1rem, 16px at default browser size; preserves user scaling. before/after.json |
| Navigation targets | 35px height | Minimum 44px standalone navigation targets; all four viewport checks pass. |
| Input boundary contrast | #a6b8b0 on panel, approx. 1.81:1 | #73877e, darker boundary; no meaning or fields changed. |
| Table semantics | Header scope absent | Column-header scope emitted by generator. Zero missing after checks. |
| Keyboard table traversal | Every table added a tab stop and same landmark name | Only overflow containers focusable; names derive from record/section heading; dedicated desktop/mobile regression passes. |
| Label associations | Nested labels only | Explicit for/id pairs added without changing visible labels. |
| Visited evidence links | No distinction | Dedicated muted plum visited-link color, existing underline retained. |
| Long text | 88ch paragraphs; unbalanced headings | 80ch paragraph measure, font-relative fluid headings and native balanced wrapping with normal wrapping fallback. |

Before/after screenshots: before-index-375.png / after-index-375.png; before-index-768.png / after-index-768.png; before-claims-1440.png / after-claims-1440.png. Additional index/claims captures cover all three widths. Audit has 36 page/viewport observations with no page-level horizontal overflow. Wide evidence tables retain contained scrolling. Offline interactions and no-JavaScript reading pass. No automatic network requests or console errors. All research statements, citations, 396 original hashes and 26 conflicts remain intact.

Independent consistency review additionally identified the input boundary and redundant table-focus issues, both addressed. Actual screen-reader sessions, Safari and Firefox rendering were not exercised. Browser privacy prevents a reliable script-level assertion of visited-link color; the stylesheet supplies it. No new broad visual redesign or factual verification is claimed.

## Substantive issues requiring approval

**S1: Opening emphasis.** At mobile width the scope and register counts precede the principal findings. Recommend moving the existing “What the records establish” block directly after the subject and cut-off, while keeping its full caveats/citations, and moving count statistics below that block. This changes prominence and ordering, not findings. Do not implement until approved.

**S2: Evidence-status language.** The exact 120 status strings are preserved but difficult to scan. Recommend preparing a reviewed plain-English label mapping, keeping exact statuses visible beside the labels. Examples for approval: `official_entity_confirmed_subject_affiliation_unresolved` → “Entity confirmed; Bleich affiliation unresolved”; `clearly_labeled_official_record_procedural_inference` → “Procedural inference from official records”. Do not collapse them into verified/unverified buckets. Prepare the complete mapping for approval before applying labels.

Recommendation: approve S1 and preparation of the S2 mapping. No shortening of research qualifications, classification changes, selected diagrams or risk ratings is authorized by this review.

## Approved follow-up
The user approved S1 and preparation of S2. The complete existing principal-findings block now precedes the count statistics, without changing its text or citations. All 120 proposed status labels, covering 247 claims, are in ../status-label-proposal.md and JSON. They remain proposals and have not been applied to the reader.
