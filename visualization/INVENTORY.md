# Visual inventory: six review drafts

Prepared November 5, 2026. Research cut-off November 4, 2026. Input: reviewed dossier and normalized register at commit 0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb. Hashes match dossier/release.json; see source-snapshot.json.

## Review purpose

Choose the clearest ownership layout and the clearest timeline layout for the separate dossier/HTML team. These are layout alternatives using the same selected facts within each family. They are not competing factual scenarios or a complete rendering of every registered entity/event.

| Draft | Audience question | Visual treatment | Evidence scope | Output |
|---|---|---|---|---|
| Ownership A | How does each disclosed ownership chain connect? | Separate top-down hierarchies | Scout historical FINRA disclosures; Ophir March 2017; EntryPoint October 2026 | DOT/source, SVG, PNG, PDF |
| Ownership B | Which intermediaries sit between a person and a firm? | Left-to-right relationship lanes | Same selected nodes and relationship set as A | DOT/source, SVG, PNG, PDF |
| Ownership C | What exactly is disclosed at each relationship? | Radial/diamond node-and-arrow maps | Same selected nodes and relationship set as A | DOT/source, SVG, PNG, PDF |
| Timeline A | When were the selected roles and firm events disclosed? | Date-scaled lanes | Selected 2009-2026 observations, with date basis retained | Python/source, SVG, PNG, PDF |
| Timeline B | Can a reviewer read the sequence without following a crowded axis? | Vertical chronological editorial view | Same selected observations as A; spacing explicitly not elapsed time | Python/source, SVG, PNG, PDF |
| Timeline C | How do the separate firm histories compare? | Firm-oriented small multiples | Same selected observations as A; scale convention stated | Python/source, SVG, PNG, PDF |

Final draft names, point counts, captions and layout tradeoffs appear in each family's README after rendering. Shape, spacing and orientation can change during legibility review without changing the selected facts.

## Evidence rules

Every depicted relationship/event carries a stable selected-item ID and supporting claim ID. Family data.json and evidence-map.md identify the exact dossier claims, date meaning and source locators. Claims are attributed as filed, not independent legal findings. The provenance source is the reviewed dossier/index, not fresh web research.

Ownership relationships are directed owner-to-entity and labeled by their actual capacity and range. Role/control-only information is visually separate. Different historical snapshots are never joined into one current ownership graph. Registry candidates, MEB INC/MEB NY equivalence and Inferent employment remain unresolved. Ownership ranges are not multiplied into a calculated personal stake.

Timelines distinguish acquired-status months, filed dates, signature dates, effective dates and reported cessation. A role observation does not establish continuous tenure. Firm settlements remain attributed to firms; administrative withdrawals are not sanctions. An award does not prove payment. Unverified early employment and Inferent affiliation are stated as gaps rather than plotted as confirmed employment.

## Production and integration

Parent owns inventory, checkpoints, comparison guide, scoped validation and Git delivery. Ownership specialist owns ownership/. Timeline specialist owns timelines/. Independent reviewer owns review/. Only visualization/ is staged and committed.

Graphviz is run locally via @viz-js/viz 3.31.0. Matplotlib 3.11.2 generates timeline graphics. Local runtimes/cache are excluded from Git; pinned version instructions and editable generators make the artifacts reproducible. All assets are static. No HTML front is created or edited.

The integration package contains an image per variant, an editable source, a caption and alt description, a source map, the input commit and a visual-fidelity review. The separate HTML author chooses where to embed an approved variant. The user's preferred layout remains an open review decision.
