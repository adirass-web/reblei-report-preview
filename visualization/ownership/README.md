# Ownership layout alternatives — draft selection assets

Three static node-and-arrow alternatives show the **same 14 selected ownership relationships**, with the same role annotations, dates, claim IDs and caveats. These are choices of layout, not different factual scenarios. Pinned research cut-off: **2026-11-04**. Source commit: `0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb`.

| Draft | Preview / print / vector | Layout trade-off |
|---|---|---|
| A | [PNG](ownership-a.png) · [PDF](ownership-a.pdf) · [SVG](ownership-a.svg) | Three side-by-side top-down hierarchies. Best compact overview and comparison of intermediaries. Densest Scout panel has smaller type than Ophir. |
| B | [PNG](ownership-b.png) · [PDF](ownership-b.pdf) · [SVG](ownership-b.svg) | Three left-to-right lanes. Clearest tracing of owner-to-entity chains, with additional vertical space for branch labels. |
| C | [PNG](ownership-c.png) · [PDF](ownership-c.pdf) · [SVG](ownership-c.svg) | Three radial/diamond relationship maps with fixed node positions. Uses the same font scale in all panels and emphasizes direct interests alongside the intermediary path. Taller page. |

## Shared caption

Selected ownership disclosures for Michael Edward Bleich (individual CRD 4262671), reproduced from separate historical Scout FINRA disclosures, Ophir's March 30, 2017 Form ADV, and EntryPoint Capital's October 15, 2026 Form ADV. Arrows run from owner to owned entity. Bands are ranges, and control and professional roles are reported separately. These panels are not one current ownership structure. Acquired-status months do not establish transaction or employment dates. Research cut-off November 4, 2026.

## Alt text

**A:** Three separate dated ownership panels arranged side by side. Scout shows Bleich to MEB NY INC to Finch to Scout, plus his below-five-percent direct Scout interest; Dror Niv to NAYS to Finch forms a second branch. Ophir shows Bleich to MEB NY INC to Finch to Ophir and a below-five-percent direct interest. EntryPoint shows Bleich's separate 25-to-below-50-percent interests in GP and Partners, Partners' 75-percent-or-more interest in Capital, and his below-five-percent direct Capital interest. Each edge includes its claim ID and acquired-status month.

**B:** The same fourteen disclosed ownership edges appear in three separately dated horizontal lanes, with arrows pointing from each owner to the entity owned. The Scout NAYS branch runs below the Bleich/MEB branch. Direct small interests bypass the intermediary chains. Professional roles, control declarations and the detached GP filing note sit outside the ownership arrows.

**C:** The same fourteen edges appear in three separate radial/diamond network panels. Scout and Ophir show a diamond linking Bleich, MEB NY INC, Finch and the firm; the NAYS/Dror Niv branch extends from Finch only in Scout. EntryPoint places Capital, Bleich and Partners in a triangle, with GP as a separate Bleich-owned branch. Directions reflect ownership disclosures, not flows of money. All panels preserve dates, ownership bands and source claim IDs.

## Facts and scope

- Scout: ID-C003, ID-C004, ID-C005, ID-C006, ID-C007, ID-C008.
- Ophir March 30, 2017: ID-C012, ID-C013, ID-C014, ID-C015.
- EntryPoint October 15, 2026: SEC-C002, SEC-C003, SEC-C004, SEC-C005.
- SEC-C006 appears as a detached Schedule A role note. No GP-to-partnership edge is inferred from a name or role title.
- Control is yes/Y for every selected ownership row. This remains separate from percentage ownership.
- The historical FINRA report is not assigned a fabricated filing date. Its displayed months are acquired-status fields from individual rows. The Scout dates/bands and other historical narratives are not reconciled by the figure.
- MEB INC is not joined to MEB NY INC. Regulatory ownership entities receive no provisional registry IDs. The same labels across dated panels do not establish unchanged stakes between snapshots.
- Ophir's combined CEO/CCO acquired-status field does not independently establish when CCO duties began.
- Inferent remains unverified and unconnected. Other owners, funds, trustees, historical extended chains and candidate registry matches are outside this deliberately selected core. The diagrams do not imply completeness.
- Ownership bands are never multiplied into an exact downstream personal stake.

## Sources and editable assets

[data.json](data.json) is the single selected-facts input, including nodes, edges, snapshot dates and claim IDs. [evidence-map.md](evidence-map.md) maps every displayed claim and caveat to the pinned dossier and exact retained source locator. The source classification and qualifications are retained.

[generate.mjs](generate.mjs) uses the local `@viz-js/viz` instance and `renderString` APIs: Graphviz `dot` for A/B and `neato` with pinned positions for C. Each of the nine `ownership-{a,b,c}-{scout,ophir,entrypoint}.dot` files is an editable panel source; matching `.graph.svg` files are intermediate assets. The generator composes the three panels into each complete SVG. Edit selected facts in `data.json` or layout in `generate.mjs`, then regenerate; direct edits to generated DOT files are overwritten.

From the investigation directory:

```powershell
node visualization/ownership/generate.mjs
python visualization/ownership/render.py
```

[render.py](render.py) uses installed PyMuPDF to make PNG/PDF exports and checks SVG IDs, PDF text bounds, required claim IDs and minimum font size. [render-check.json](render-check.json) records the check results; [layout-metrics.json](layout-metrics.json) records panel geometry.

## Rendering and review

All three PNGs were opened for visual inspection. The final versions use distinct node-and-arrow layouts. No clipped or overlapping node/text labels were observed. Automated export checks find no text outside PDF page boundaries and no missing selected claim IDs. Final minimum PDF type sizes are A 12.12 pt, B 15.30 pt, C 14.68 pt.

PDFs use a common 1684-point large-format width with proportional height: A is landscape; B is nearly square; C is taller. Print at actual size or maintain at least 10 pt after scaling. SVGs are the preferred responsive integration assets. Colours distinguish dated panels only; arrow direction and text carry the meaning independently of colour. Every complete SVG includes an accessible title and description.

These checks establish rendering and source transcription within the selected scope. They are not user selection, visual approval, a new fact check, publication or a claim that unresolved identity questions have been closed.
