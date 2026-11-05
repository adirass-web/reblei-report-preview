# Packaging report

Release tooling is ready. The final package has not been sealed; final generation and verification await coordinator review of the adapter and frontend changes.

## Contract

The canonical input is package-root `data/evidence-index.json`. Each of `exports/scout/` and `exports/opeh/` receives `records.jsonl`, `financial_findings.csv`, `calculations.csv`, `discrepancies.csv`, and `sourceinventory.csv`. No deferred combined statement is exported as a scoped finding. Deferred coverage remains in the canonical root index.

Raw accepted strings and values in the source-scoped projection remain unchanged in records.jsonl. The audit-only canonical_record cross-source original is omitted from every scoped record export; full canonical data/evidence-index.json remains unchanged. No arithmetic is recomputed. Calculations export joined evaluation display_result, exact_result and status, while retaining the complete evaluation and other accepted record fields. CSV columns preserve confidence, attribution, assumptions, flags, source citations and any identity/capacity qualifications. Cells starting `=`, `+`, `-` or `@` receive a leading apostrophe in CSV to prevent spreadsheet formula execution. JSONL retains those raw strings.

The manifest includes all package files using sorted package-relative POSIX paths, SHA-256 hashes and byte sizes. It excludes its own `audit/release-manifest.json`, `audit/release-verification.json`, directories `.git`, `__pycache__`, `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `node_modules`, `.venv`, `venv`, and Python `.pyc`/`.pyo` bytecode. Exclusions apply at any directory depth. Symlinks in included paths are rejected; absolute paths and path traversal in manifest entries are rejected. Manifest generation adds no timestamp. Exports and audit writes use same-directory temporary files and atomic replacement.

Verification rejects altered bytes, missing included files and unexpected included files. Integrity verification establishes package bytes and membership; source correctness, portable source links and browser behavior are covered by separate adapter/frontend reviews. No external data or services are used by this tooling.

## Tooling verification

Executed 2026-11-05 from `/workspace/ReBlei-dossiers`:

- `python -m unittest discover -s dossiers/supplied-files/work -p test_seal.py`: 4 tests passed. The tests first failed because release tooling did not exist.
- `python -m unittest discover -s tests`: 56 tests passed. The existing duplicate ZIP-member fixture emitted a `Duplicate name: 'same.pdf'` warning.
- `/tmp/reblei-dossier-venv/bin/python -m unittest discover -s dossiers/supplied-files/work -p 'test_*.py'`: 24 tests passed. An earlier system-Python run produced two frontend import errors because `markdown_it` was not installed in that interpreter; the configured venv run passed.

Fixture coverage checks deterministic complete hashes, changed/missing/unexpected-file rejection, symlink/path-escape rejection, scoped JSONL, evaluated-result export, retained qualifications and spreadsheet escaping.

## Usage

From the repository root:

```sh
python dossiers/supplied-files/work/seal_package.py
python dossiers/supplied-files/work/seal_package.py --verify
```

The first command regenerates scoped exports and seals the package. The second verifies the existing seal without regenerating exports and returns a nonzero exit status on failure. From the package root, the equivalent commands are `python work/seal_package.py` and `python work/seal_package.py --verify`. Any subsequent included-file edit requires a fresh seal. Sealing preserves this authored report byte-for-byte. It writes only factual generated counts, input/export hashes and projection metadata to audit/release-export-metadata.json; that file is included in the release manifest. The seal does not run tests or generate claims about test outcomes.

## Task 5 review fixes — 2026-11-05

Scoped JSONL and CSV projections now omit the adapter's audit-only `canonical_record` field so mixed-source original entity identifiers and prose cannot leak into dossier exports. The full canonical index is unchanged. A new regression fixture adds a cross-source CRD identifier and statement to that field and confirms their absence from every scoped export while checking that the input object remains unchanged.

`seal()` now preserves author-written `audit/packaging-report.md` rather than replacing it with hardcoded test claims. The generated `audit/release-export-metadata.json` contains only factual source-index hash, scoped record counts, omitted-field names and export hashes/sizes. A new regression test confirms authored review text survives sealing and generated audit files contain no invented test-pass statements.

Both regression tests were observed failing before the fixes. After implementation, the following exact commands were run from the repository root:

- `python -m unittest discover -s dossiers/supplied-files/work -p test_seal.py`: 6 tests passed.
- `/tmp/reblei-dossier-venv/bin/python -m unittest discover -s dossiers/supplied-files/work -p 'test_*.py'`: 28 tests passed.
- `python -m unittest discover -s tests`: 56 tests passed; the existing duplicate ZIP-member fixture emitted its `Duplicate name: 'same.pdf'` warning.

These are recorded executions, not assertions generated by sealing. Final package sealing remains pending coordinator review.
