# Scout static figure implementation

Implemented `work/visuals/scout.py`, exposing `build(index: dict, output: Path) -> list[dict]` and the required `--index` / `--output` CLI. Only the accepted `data/evidence-index.json` supplies factual data. Generated eight SVGs, eight PNG fallbacks, eight CSV tables, eight JSON exports and one eight-entry manifest under `presentation/figures/scout/`. No PDF, new research, source-record changes or commits were made by this worker.

| Figure ID | Composition | Placement |
| --- | --- | --- |
| scout-historical-ownership | Dated financial-note panels plus separately scoped BrokerCheck bands | Inline |
| scout-balance-snapshots | Liabilities and capital stacked to assets, with separate capital scale | Inline |
| scout-profit-operating-cash | Paired flow bars and explicit gray hatched missing years | Inline |
| scout-2011-capital-waterfall | Aggregate members' capital bridge | Inline |
| scout-regulatory-timeline | Readable vertical dated chronology with payment-evidence limits | Inline |
| scout-subordinated-debt | Three principal snapshots and source-reported repayment annotation | Appendix |
| scout-2011-regulatory-capital | Regulatory-capital waterfall and separate $1 source-difference inset | Appendix |
| scout-statement-coverage | Five-year supplied/missing statement matrix | Appendix |

The agreed blue/amber/teal/purple/gray palette is used with text, markers and hatches. The attention accent `#A61B50` labels the profit/cash **Key finding** and the **Source difference** inset; it does not replace semantic category colors or assign risk ratings. The inset preserves the eleven common-stock sector rows totaling $500,977 versus the source subtotal $500,978, with the accepted `calc-scout-2011-common-sector-total` and `fin-scout-finding-sector-one-dollar` citations. It is explicitly separate from the regulatory-capital bridge, with no balancing entry or materiality conclusion. All figures are static, contain searchable SVG text, use a white background and plotted text of at least 11 points. Summary and limitation fields carry all material chart qualifications.

## Verification performed

Commands below were run from `/workspace/ReBlei-integration` with system Python. The cache variables avoid read-only home-directory font-cache warnings; they do not alter the data or artifacts.

```sh
XDG_CACHE_HOME=/tmp/scout-cache MPLCONFIGDIR=/tmp/scout-mpl-config python dossiers/supplied-files/work/visuals/scout.py --index dossiers/supplied-files/data/evidence-index.json --output dossiers/supplied-files/presentation
XDG_CACHE_HOME=/tmp/scout-cache MPLCONFIGDIR=/tmp/scout-mpl-config python dossiers/supplied-files/work/visuals/scout.py --index dossiers/supplied-files/data/evidence-index.json --output /tmp/scout-visuals-rebuild
python -m py_compile dossiers/supplied-files/work/visuals/scout.py
```

Both generation commands exited 0 and printed:

```text
Generated 8 Scout figures with SVG, PNG, CSV and JSON; source closure and exact reconciliations passed.
```

Generation checks every selected record and its recursive accepted dependency graph for Scout lane ownership, record existence, non-deferred status and Scout source-document closure. Exact `Decimal` assertions independently verify all five assets = liabilities + capital equations, the 2011 capital bridge, the $9m − $5m = $4m debt endpoint relationship, regulatory adjusted and excess capital, and the eleven-sector sum and retained −$1 residual. Relevant accepted calculations must report reconciled zero residuals; the sector difference must retain status/result/residual evidence rather than being silently corrected.

An additional inline `python - <<'PY'` validator parsed the manifest, every CSV and JSON table and every SVG with `xml.etree.ElementTree`; checked first-five-inline/last-three-appendix placement, existing section anchors, selected source IDs and table-source membership, string-or-null numeric export types, real SVG text, absence of scripts/foreignObject/raster images/event attributes/external resource references, font sizes, and byte equality against the clean regeneration directory. Actual output:

```text
PASS: 8 manifests; 5 inline/3 appendix; 8 safe real-text SVGs; 88 export rows; exact CSV/JSON row counts; source IDs and anchors closed; all 33 files byte-identical on clean regeneration.
```

Visual inspection used `view_image` for ownership panels, regulatory chronology, both capital waterfalls, the profit/cash chart, balance chart, debt snapshots and coverage matrix. Labels, sources' qualifications, hatch distinctions and the $1 inset were readable at full resolution with no clipped content. Inspection caught paired dollar signs triggering Matplotlib math rendering in the first inset draft; `text.parse_math=False` fixed the final static output. The final regenerated regulatory-capital PNG was re-inspected.

## Evidentiary and presentation limits

Ownership panels do not multiply disclosed bands or allocate assets/distributions to Bleich. Unknown BrokerCheck capture dates remain explicit. The 2009 flow period is inception February 5–December 31; the misleading 2010 Remarks filename does not become a sixth year. Missing 2012/2013 flows are null/unavailable, never numeric zero. Earlier unnamed member notes do not identify Bleich; the $5m repayment is attributed to the note and unquantified unpaid interest remains unknown. The timeline keeps firm sanctions, representative execution, an elected payment method and payment evidence separate, with no personal fine, current balance or completion inference. Equal-spaced chronology rows do not imply elapsed-time scale. The charts use rounded millions only for selected plotted labels; downloads retain exact accepted decimal strings and raw source strings where supplied.

This worker verified figure assets and source closure; page-level static HTML, browser/mobile checks and publication integration belong to the integration/review workers. The supplied corpus, accepted analysis and original source files were preserved.
