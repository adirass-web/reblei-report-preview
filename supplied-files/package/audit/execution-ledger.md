# Supplied dossiers — execution and decisions

Approved design: two supplied-file dossiers by source; editable repository files rebuilt to static HTML using the broader investigation's presentation stack. No independent research evidence, new retrieval, publication or integration.

## Checkpoints

- C1 input/provenance: 1,814 corpus/analysis files frozen; all source and analytical records accounted for. Commit22c83c1.
- C2 authoring: Scout and OPEH reports with source rechecks and scoped financial narratives. Commit67e2e6a.
- C3 source challenge: independent reviewer found unsupported regulatory identifiers in shared OPEH metadata projections. Fixed by conservative indexing projections; accepted baseline unchanged. Commit076d73f. Scoped re-review approved spec and quality.
- C4 presentation: adapted static stack, portable originals/images, source/record navigation, search and print views; release tooling. Commit9ac31f0.
- C5 coordinator verification: 28 dossier tests and56 original tests passed;1814 original hashes verified;1203 generated file hashes identical across two builds; static local-link/fragment/safety checks passed. Both report PDFs generated normally (Scout8A4pages/OPEH6).
- C6 final branch review and release seal: see final-independent-review.md, validation-summary.json and release-verification.json for final recorded outcomes.

## Rulings and implementation defaults

1. Run disjoint adapter, Scout/OPEH authoring and presentation tasks in parallel, as expressly authorized by the approved user plan. Coordinator alone commits to avoid shared-index races. Risk if wrong: coordination rework; contained by disjoint file ownership and independent reviews.
2. Keep the full accepted mixed records in the internal audit index. Reader data projects deferred records to IDs/dispositions/reasons only, and scoped exports omit audit-only canonical_record. No combined argument enters either dossier. Risk if wrong: a future consumer could mistake internal audit data for a scoped reader export; the contract, naming and export metadata explain the distinction.
3. Shared entities are indexing labels, not identity joins. Mixed operational projections omit unsupported identifiers and original mixed prose; original metadata remains audit-only. This is conservative and can omit a same-lane identifier until separately supported. Risk if wrong: reduced convenience, rather than unsupported attribution.
4. Leave the managed Chromium policy intact. Direct file navigation is explicitly blocked, not passed. Use permitted HTTP/no-JavaScript and static offline-asset checks; normal headless PDF generation succeeds. Risk if wrong: direct-file runtime behavior remains unverified in this environment and is disclosed in the delivery.

## Delivery state

Implementation remains on isolated branch feat/supplied-dossiers in /workspace/ReBlei-dossiers. The original checkout and supplied baseline are unchanged. No merge, push, public deployment or environment publication is performed. Build artifacts and evidence remain available for review; local dependency caches are excluded from sealing.

## Final review and handoff

Final independent whole-branch specification and quality review approved. Both nonblocking minors were addressed in one scoped fix wave: reproducible maintainer setup and asserted keyboard focus/navigation. The focused re-review found no unresolved findings or new breakage. HTTP browser checks and report PDFs were refreshed; direct file navigation remains policy-blocked.

Coordinator verified the portable copies: all38 original files have SHA-256 equal to their canonical document IDs; all1116 copied page assets match the immutable corpus. Source isolation, typed closure, qualifiers, raw export projections, static links and repeat-build equality were independently checked. Final sealing and verification are recorded in release-verification.json. The chosen finish is keep-as-is: no merge, push, deployment or environment publication.
