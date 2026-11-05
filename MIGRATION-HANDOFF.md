# ReBlei migration and continuation handoff

**November 5 HTML release:** open [presentation/index.html](presentation/index.html) for the offline, read-only report and evidence dossier. Copy the whole investigation folder to preserve evidence links. See [opening instructions and validation](presentation/README.md). The requested design review and technical refinements are recorded in [the review](presentation/review/design-audit/review.md); two substantive presentation choices await approval.

**November 5 cleanup update:** remote recovery and the dossier rebuild were verified, then redundant local originals and the old checkout were removed. Continue in `outputs/ReBlei-migration`, which now has its own complete Git object store, or clone the migration branch. See [cleanup completion and preservation proof](cleanup-2026-11-05/README.md). Statements below that local originals remain retained describe the earlier migration checkpoint. A separate visualization task may have work in progress under `visualization/`; preserve it when syncing.

Migration date: November 4, 2026 (user date). Repository: private adirass-web/ReBlei.
Continue on **research/bleich-local-migration-2026-11-04**, based on commit 96a6bc2becc90d026dcaafce6490fc76798738e4.
Scope: investigations/2026-11-04-official-records/ only. Local originals remain retained. Other repository content was not reviewed or used as research evidence.

## Continue here
Use the local Git checkout at V:/Codex/2026-11-04/referenced-chatgpt-conversation-this-is-an-3/outputs/ReBlei-migration, or a fresh clone of the same repository and branch. Do not continue in the older loose outputs/work folders.
At each session start verify origin equals https://github.com/adirass-web/ReBlei.git, the active branch is research/bleich-local-migration-2026-11-04, and local/remote commit and working-tree status are understood. Do not overwrite a dirty checkout or force a divergent history. Sync a clean branch by fast-forward only.
Keep evidence, analysis, scripts, QA and planning inside the investigation folder. At every completed stage validate and reseal, commit only intended investigation paths, push this branch and verify remote HEAD equals the local commit. Report any unsynced work explicitly.
Do not merge or change main, the previous research branch, repository visibility or other work. GitHub is the shared continuation record; the checkout is the editing environment.

## Read first
- [Current research results](continuation-4/summary.md)
- [Separate remaining-work instructions](remaining-work-instructions.md)
- [Current evidence index](evidence-index.json) and [document guide](evidence-index.md)
- [Independent research QA](independent-qa.md)
- [Migration inventory and exclusions](migration-2026-11-04/inventory.json)
- [Migration validation](migration-2026-11-04/validation.json)
- [Supporting-work archive guide](migration-2026-11-04/README.md)

The source checkpoint contained earlier research. This transfer adds local round-four material and unique external supporting work; it does not claim new research findings. Preserve IDs, date/metric qualifications, firm-versus-person distinctions and unresolved joins. The new branch supersedes old branch names in historical notes and scripts.

## Preservation and QA
All indexed originals are unchanged and SHA256-verified. All 17 JSON tables equal SQLite; integrity and foreign-key checks pass. All claims have evidence links. The whole-package checksum manifest is SHA256SUMS.txt; its own bytes are verified against the committed blob.
Unique files were copied with original mtimes; Git stores bytes and the inventory separately preserves timestamps. Exact duplicate locations and four SEC CSV cache exclusions are individually recorded. Every excluded CSV was decompressed from its retained ZIP member and matched by full SHA256 and size.
archive-manifest.json is a HISTORICAL BASELINE with outdated counts (47 documents, 104 claims, 5 events). Retain it as provenance, not the current manifest. Current normalized totals are 396 documents, 247 claims, and 9 events; the events include administrative withdrawals, not nine sanctions.
Late corporate and registration QA notes were captured before final sealing. Their bounded passes and the independent normalized-index review are retained. No missing round-four QA note remained at finalization. These checks do not certify exhaustive employment, corporate or court coverage.

## Remaining work and limits
Follow the separate instructions for early employment, alleged Inferent affiliation, corporate ownership/identity bridges, adviser histories, award follow-up, financial/date discrepancies, missing originals, and unavailable Library documents.
**NYSCEF remains an accepted access gap.** No retry or CAPTCHA request is authorized. No PACER account, paid records, outreach, public release or default-branch merge was undertaken.
The full-career investigation remains incomplete. Hash integrity does not establish the truth of filed statements or a clean litigation/regulatory history.
Plan the simple internal HTML report and dossier with the user subsequently. No HTML implementation, hosting or deployment is included in this transfer.

## Migration completion
Verify the pushed branch equals local HEAD, the original research and main refs remain unchanged, all committed file hashes match, and the checkout is clean. Report the final commit and file totals in the user handoff; do not claim completion if verification fails.

## Isolated continuation checkout
The original checkout received source-author updates while migration checks ran. The migration was finalized in a separate checkout, outputs/ReBlei-migration, to avoid concurrent-write races. The original checkout and its pending/staged files remain untouched after copying; it is not the canonical continuation checkout. Late revisions are recorded in the migration inventory. Read the remote branch or the isolated checkout for the verified migration snapshot.
