# OPEH visual implementation report

Implemented seven static source-scoped figures with `work/visuals/opeh.py`. The public `build(index, output)` function and CLI consume the accepted evidence index and write only `presentation/figures/opeh/`. Each figure has searchable text SVG, PNG, CSV, JSON and a shared manifest entry. No PDF was generated and no accepted financial/source record was changed.

| Figure ID | Family | Placement |
| --- | --- | --- |
| opeh-one-obligation | One collective note / named makers / predecessor capacity | Parties, capacity and collateral |
| opeh-procedural-timeline | 2018 procedural timeline with separate 2020 administrative correction inset | Instrument and procedural chronology |
| opeh-creditor-request | Creditor principal / asserted interest / unknown fees | Source amounts and component arithmetic |
| opeh-rounding-day-count | Conditional day-count and rounding matrix | Interest boundaries and rounding |
| opeh-calendar-branches | Three aligned September 1–27 conditional calendar lanes | Calendar and rate-switch scenarios |
| opeh-contract-notice-gaps | Separate contractual triggers and unresolved notice evidence | Appendix/gallery |
| opeh-coverage-status | Source occurrence / document and calculation-status counts | Appendix/gallery |

The calendar uses aligned date positions and distinct due, cure-end, switch and filing markers. Branch A leaves due/cure unknown; B shows September 3/17/18/27; C shows September 4/18/19/27. Exact accepted interest values appear beside each lane. The existing $310.14 one-day sensitivity appears as a labeled attention callout. Every branch remains conditional, with common assumptions visible and full qualifications in the manifest summary/limitation and downloadable data.

The shared semantic palette is preserved. Attention accent `#A61B50` outlines the one collective principal and the conditional $620.35/$0.07 differences; neither difference is labeled an overcharge. Unknown cash funding and later payment status remain explicit unknowns. The timeline treats December 2020 as an administrative correction, with no reopening or new monetary accrual inferred. The creditor's $155,070 is consistently an assertion and no individual maker share or second predecessor principal is introduced. Figures require no browser arithmetic or interaction.

## Actual verification

Regeneration command passed with system Python/Matplotlib 3.10.8:

```sh
python dossiers/supplied-files/work/visuals/opeh.py \
  --index dossiers/supplied-files/data/evidence-index.json \
  --output dossiers/supplied-files/presentation
```

An independent in-process verification run imported `build`, generated all outputs a second time into a temporary directory, and confirmed byte-for-byte equality of all 29 files (28 assets plus manifest). The final calendar-lane revision was included in this comparison.

- Seven manifest entries; five primary and two appendix figures; all 28 referenced assets exist and are nonempty.
- All manifest record IDs and recursively followed accepted dependencies exist and belong to the OPEH lane. Source/dependency counts respectively: 5/12, 12/46, 8/18, 10/17, 13/25, 4/29 and 45/64 in manifest order.
- Cross-lane/deferred-source rejection was exercised by changing the note-principal record's lane to `deferred` in an in-memory test copy; it raised `ValueError` as intended. Accepted OPEH peripheral document classifications can be appendix-only and remain valid for provenance counts; they are not deferred-lane records.
- Build-time accepted-value checks bind the displayed principal, asserted interest, per diem, rounding gaps, rounding scenarios, implied-day diagnostic and six rate-switch outputs to existing accepted index strings. The demand addition reconciles exactly. Notice-dependent timing and later-balance results remain null/not testable.
- Accepted counts independently reproduced from the index: 21 occurrences, 20 unique documents; 25 calculations = 2 reconciled, 21 conditional, 2 not testable. Counts are explicitly not confidence or corroboration measures.
- All seven SVGs parsed successfully, retained real text at 11pt or larger, and passed checks excluding scripts, foreign objects, event handlers and external resource references.
- Every figure JSON table equals its manifest table; each CSV has the expected row count. JSON retains exact accepted results, source record IDs, date bases, assumptions, status and dependency IDs.
- All seven PNGs were visually inspected at their generated 160dpi size; the revised calendar lanes and the corrected timeline inset were inspected. No clipped text or overlapping amounts were observed. Currency is literal because `text.parse_math=False` is set globally. Mobile HTML presentation and source-link rendering are integration-worker checks.

No commit, external research, source-data mutation or subagent was used for this work.
