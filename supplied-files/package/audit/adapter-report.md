# Supplied-source adapter audit

The adapter is complete for baseline commit `40e77bd1e57c0fce62a3a962d977c05b54724e8a`. It reads only the original `corpus/` and `analysis/bleich-profile-financial/data/` inputs; no broader-research data, new extraction, OCR, or recalculation is used. Original inputs remain unchanged.

## Reproduction

From the repository root:

```sh
python -m unittest discover -s dossiers/supplied-files/work -p test_adapter.py
python -m unittest discover -s tests -v
python dossiers/supplied-files/work/adapter.py --freeze
```

The final command creates a freeze only when absent. An existing freeze must verify before any generated data is rewritten. It writes `data/evidence-index.json`, `data/coverage.json`, and `data/dispositions.json` deterministically. The Python API is `build_index(repo_root)`, `validate_index(index, repo_root)`, `freeze_inputs(repo_root, output)`, and `verify_inputs(repo_root, manifest)`.

`audit/input-manifest.json` freezes all **1,814** files beneath the complete original `corpus/` and `analysis/` trees, including source bytes, reviewed pages, reports, and earlier audit inputs. Each relative path has an exact byte length and SHA256. Verification rejects added files, missing files, and changed bytes. No timestamp or runtime-dependent path enters the generated index.

## Allocation and coverage

| Dossier | Original occurrences | Unique documents | Findings | Calculations | Assertions | Profile-financial links | Discrepancies |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Scout | 20 | 18 | 17 | 104 | 34 | 25 | 16 |
| OPEH | 21 | 20 | 9 | 25 | 11 | 14 | 23 |
| Deferred | 0 | 0 | 0 | 0 | 2 | 3 | 1 |
| Acceptance totals | 41 | 38 | 26 | 129 | 47 | 42 | 40 |

Every acceptance record has exactly one disposition. All canonical phase2 data collections are included, with evaluated calculations joined by exact canonical ID and lane obligation exports recognized as verified aliases. Every corpus analytical record is also retained; this includes all 201 source-owned raw entity mentions. Nothing is discarded merely because it is peripheral to the main financial narratives. The index has **3,879** records: Scout 3,455, OPEH 418, deferred 6. Scoped metadata explains why six mixed entities produce twelve lane entries.

Document ownership comes from supplied archive container identity; filenames inside an archive cannot move a document to another lane. The standalone `Nasdaq $3 mm fine to Bleich.pdf` is explicitly assigned to Scout. Unknown standalone sources or containers fail closed. Duplicate occurrences are preserved, and sources with separate SHA256s remain distinct even when their native text agrees.

## Mixed statements and entity scope

The following original statements are retained as `dossier_id=deferred`, `appendix_only=true`, with audit dispositions explaining their exclusion from dossier findings:

- `prof-secondary-current-role`
- `prof-regulatory-litigation-unresolved`
- `pflink-profile-identity-crd-01`
- `pflink-profile-regulatory-litigation-unresolved-01`
- `pflink-profile-regulatory-litigation-unresolved-02`
- `issue-prof-regulatory-litigation-unresolved`

Shared entities are metadata, not evidence permission. Mixed entity IDs receive `--scout` and `--opeh` scoped variants, preserve `canonical_id`, narrow operational citations and source mentions to the correct lane, and retain the untouched original object in `canonical_record` solely for provenance audit. **The renderer must not display that audit object as a scoped assertion or scoped evidence list.** It must use the operational `source_citations`, `supporting_record_ids`, and `dependencies` instead. All scoped entities are appendix-only metadata. Other entity IDs and related-assertion references remain visible as metadata references without importing their entire source-citation sets.

Canonical IDs are otherwise unchanged. Primary canonical records preserve every original field. The 33 lane-export aliases are checked for exact record equality against `obligations` and `obligation_events`, then recorded in `canonical_provenance.aliases`. A conflicting ID or namespace collision raises an error; it never silently overwrites original provenance. The actual accepted baseline has no conflicting IDs.

## Typed evidence and arithmetic

The index records **8,869 typed evidence edges**. Support records, source records, normalized facts, operands, source comparison targets, instrument/family references, calculations, and source mentions close within their source lane. A missing typed dependency or an unexpected source crossing fails the build. Metadata references are separately recorded and do not recursively import unrelated entity assertions.

The canonical `comparison_basis` controls target traversal: `normalized_source` targets are dependency IDs; all five `literal_zero` targets are values. No artificial record named `0` is required. All 129 evaluations are joined to the canonical calculation records by ID; the exact results, displayed results, original flags, assumptions, residuals, missing inputs, and source lineage are retained unchanged. The known Scout 2011 common-sector residual remains `-1`. No calculation is performed by this adapter.

## Source classifications and citation validation

The original reviewed document classifications are retained alongside original document metadata. The unattributed advocacy narrative and supplied research synthesis are explicitly secondary. Search indexes, paper placeholders, unexecuted draft, summons transcription, and incomplete text extraction are classified as appendix-only peripheral sources. Records supported solely by secondary/peripheral sources remain appendix-only with their original attribution.

Validation inspected the syntax, source ownership, and physical locator of **8,192 operational record citations**, including the typed dependencies' underlying records. PDF locators must be physical page numbers within that source's original page count. Non-PDF locators must use valid CSV rows, text lines, or the canonical `section=body`; CSV row bounds use a CSV reader so quoted newlines do not fabricate extra rows. Non-PDF page locators and PDF line locators are rejected.

This is a structural citation audit, not a new substantive source reading. The adapter did not manufacture human source inspections. The separate dossier-author reports must identify the exact source text/images they rechecked for new prose conclusions. The original all-pages-reviewed corpus remains frozen and reused.

`validate_index` also reconstructs the complete canonical adapter output and checks exact equality, so altered confidence, attribution, evaluation, document metadata, missing records, and omitted dispositions cannot pass merely by retaining the expected totals. Independent acceptance count checks remain additional checks, not substitutes for closure and citation validation. The full original input freeze is checked before success.

## Verification results

- Test-first baseline: **14 expected failures** before `adapter.py` existed, each explicitly reporting the missing source-adapter implementation.
- Final adapter suite: **16 tests passed**. Covered all acceptance dispositions, exact source counts, deferred mixed statements, source-restricted shared metadata, all raw entity mentions, canonical-field preservation, canonical evaluation join, all dependency closure, literal-zero versus source-target semantics, verified aliases, secondary/peripheral classifications, missing-citation rejection, wrong-lane rejection, invalid physical/non-PDF locators, removed acceptance record rejection, deterministic rebuild, and frozen input change/addition/removal rejection.
- Existing repository suite: **56 tests passed** using `python -m unittest discover -s tests -v`. The pipeline duplicate-archive fixture emits its existing `UserWarning: Duplicate name: 'same.pdf'`; no test failed.
- `python -m pytest -q` was attempted first, but the system Python has no `pytest` module. The repository tests use `unittest`, so its native discovery ran the complete suite successfully without installing dependencies.
- Final adapter generation and all-input hash verification passed with the acceptance totals shown above. No commits were made by this implementation agent.

## Round 1 review fix: conservative mixed-entity field projection

Independent review identified a field-level source partition defect: although `ent-scout--opeh` and `ent-ophir-partners-llc--opeh` had correct OPEH-only operational citations, their `identifiers` still contained CRD151990 and CRD164729/SEC801-77121 respectively, copied from Scout regulatory sources. The existing generic metadata label did not justify displaying these unsupported identifiers. Original mixed `rationale`, `flags`, attribution, confidence and entity-reference fields had the same projection risk.

The adapter now constructs all twelve mixed-entity lane variants from an explicit whitelist of neutral canonical indexing name/type fields, lane-filtered citations, source mentions, supporting IDs, and adapter bookkeeping. It clears **all mixed identifiers in both lanes** instead of attempting to infer field-level support. No original analytical prose, original mixed flags, original confidence/attribution, or entity-reference metadata remains in these operational projections. The status is explicitly `indexing_metadata_only`; the scope note states that names and types are indexing labels rather than cross-source identity joins. Source-owned supporting records retain their own original assertions and attribution. Every original mixed field remains byte-for-byte equivalent as parsed JSON inside the unchanged `canonical_record`, which remains excluded from renderer/browser projections.

Two meaningful regression tests were added before the fix and observed failing: one reproduced the unsupported identifier leak, including the named Scout and Ophir examples; the other rejected original analytical prose and non-whitelisted fields across all twelve mixed projections. Both now pass. The tests additionally verify that identifiers cannot occur anywhere in the operational versions of the two reported entity families and that the complete original canonical entities remain intact in audit provenance.

Commands and results:

```sh
python -m unittest discover -s dossiers/supplied-files/work -p test_adapter.py
# 18 tests passed (the two new regressions first failed before implementation)
python dossiers/supplied-files/work/adapter.py --freeze
# Complete canonical validation, citation/edge/count checks and existing freeze passed.
```

`data/evidence-index.json`, `coverage.json` and `dispositions.json` were regenerated. All record IDs, lane counts, acceptance dispositions and typed evidence edges remain unchanged. A second regeneration was byte-identical; the revised evidence index SHA256 is `2e9333eacd21ae7b8955fb8846e73632f42a95346dff988744b631fa34f23852`. All 1,814 original input hashes verify against the original freeze; `audit/input-manifest.json` remains unchanged with SHA256 `98f1166f348ee80bbe77e81d51a45c9e9b38b5ef43338e024ee00ee43a0dfaaa`.

The front-end implementer was notified before and after the index change. No original data, narratives, renderer code, or commits were changed by this fix.

The complete original repository suite was rerun after this fix with `python -m unittest discover -s tests -q`: **56 tests passed**. Its existing duplicate-archive fixture again emitted only `UserWarning: Duplicate name: 'same.pdf'`.
