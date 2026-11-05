# Remote recovery verification and local cleanup

Prepared November 5, 2026 (user timezone). Scope: the completed investigation and dossier, their local working copies, and one known editorial-support temporary file. The retained checkout is `outputs/ReBlei-migration` on `research/bleich-local-migration-2026-11-04`.

## Remote preservation and recovery proof

A new clone fetched directly from GitHub at `0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb` passed Git object-integrity checks. All 1,023 tracked investigation files matched their complete SHA256 inventory, including the manifest itself. The clone had no shared-object dependency on either local checkout. See [remote-source-verification.json](remote-source-verification.json).

The dossier was rebuilt and validated in that fresh sparse checkout using its own sources. The manuscript hash was unchanged. The check covered all indexed source hashes, 247 claims, 444 evidence links and 26 conflicts, and passed all 2,245 local links with zero broken links. See [fresh-checkout-test.json](fresh-checkout-test.json). This proves the dossier can be edited/rebuilt and its evidence browsed from the remote package. It does not claim that every historical acquisition helper, network service or missing original is available.

Four expanded SEC CSV caches were fully decompressed from the remote compressed members and matched by SHA256 and size before removal: 956,549,660 bytes. Their compressed originals remain preserved. See [cache-verification.json](cache-verification.json).

## Additional local preservation

The [local inventory](local-inventory.json) accounts for 1,225 exact duplicate files and five older or additional support files. The latter are copied byte-for-byte into [recovered-files/](recovered-files/), under short hash-based filenames; the inventory maps each original path to its archive. These are historical support/drafts, not new research assertions or replacements for current reports. All old staged file versions are accounted for, and all old local branch tips are ancestors of the saved remote history.

The retained checkout formerly borrowed Git objects from the old clone. Its objects were repacked, its alternates dependency removed, and `git fsck --full --no-dangling` passed without that dependency. The former path is recorded in [former-git-alternates.txt](former-git-alternates.txt).

## Bounded cleanup

The deletion script requires the exact workspace, live remote-tip agreement, committed preservation copies, full source hashes, unchanged old staged work, and no symlinks/junctions. It checks every absolute target before native PowerShell deletion. It retains the canonical checkout and removes only inventoried loose outputs, old work folders, the older checkout, the temporary verification clone, and the one explicitly inventoried editorial-support file outside the workspace.

A separate active visualization task began during cleanup. Its entire folder, including active ignored runtime dependencies, is protected inside the retained checkout. Its in-progress outputs are not included in this completed-research verification; that task owns its Git delivery. To avoid archiving changing visuals or their runtime cache, this cleanup's checksum snapshot is sealed in the isolated verification clone using the existing `work/seal_package.py`.

The five additional files and this pre-deletion record must be committed and pushed before cleanup. Completion and actual removal counts are recorded in [cleanup-receipt.json](cleanup-receipt.json). No unrelated PC folders or global application caches are cleanup targets. Records not obtained during research remain listed as gaps; preservation checks do not make those records available.

## Completed cleanup

Preservation checkpoint `0cea55390695459bfc91d57a1ef9f6420b737417` was pushed and verified before deletion. All listed targets were removed. Including the four expanded caches, **3,472 files containing 2,246,770,055 bytes (2.25 GB)** were removed. Counts include the old Git store and disposable verification clone; they are file bytes removed, not a claim about net disk-space gain after creating preservation copies.

Only `outputs/ReBlei-migration` remains in this task workspace. It passed Git object-integrity checks again without alternates. All 396 indexed source hashes remain unchanged; SQLite integrity and foreign keys pass. See [final-local-verification.json](final-local-verification.json). The active visualization folder remains protected and was not cleaned or committed by this task.

The final checksum manifest retains the isolated snapshot's file set and adds cleanup records. All preceding hashes were checked before updating this report, the continuation handoff and cleanup records. It deliberately excludes the separate task's changing visualization files. Historical cleanup scripts describe this one completed operation; they must not be rerun against a changed workspace.
