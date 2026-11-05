"""Assemble the visualization-only review package; never modify research or HTML."""
from pathlib import Path
import json

R = Path(__file__).resolve().parents[1]
snapshot = json.loads((R / 'source-snapshot.json').read_text(encoding='utf-8-sig'))
variants = [
    ('ownership', 'ownership-a', 'Ownership A — Dated hierarchies', 'Three top-down panels for comparing the disclosed intermediary chains.'),
    ('ownership', 'ownership-b', 'Ownership B — Horizontal lanes', 'Left-to-right tracing of owner-to-entity relationships. Recommended starting point for diligence review.'),
    ('ownership', 'ownership-c', 'Ownership C — Radial maps', 'Diamond and triangular arrangements emphasize direct interests alongside intermediary paths.'),
    ('timelines', 'timeline-a', 'Timeline A — Calendar lanes', 'A true calendar axis separates role, regulatory/award and administrative observations.'),
    ('timelines', 'timeline-b', 'Timeline B — Chronological reading', 'Two-column reading sequence, explicitly not to scale. Recommended starting point for narrative review.'),
    ('timelines', 'timeline-c', 'Timeline C — Firm record panels', 'Three firm panels share a calendar scale for comparison.')
]
parts = ['''# Six visualization drafts for review

Choose one ownership layout and one timeline layout for refinement. These are **layout alternatives**, not different factual scenarios: all three ownership diagrams contain the same 14 selected relationships, and all three timelines contain the same 16 selected observations.

**Suggested starting pair: Ownership B + Timeline B.** B makes the ownership paths easy to trace; the chronological timeline is easiest to read continuously. Choose Timeline A or C when elapsed time or comparison across firms matters more.

These are large-format drafts: open a PNG at full size or zoom the SVG/PDF to read the source labels. They have not been approved for final inclusion or reduced to an A4/Letter print layout.

## Review index

| Ownership alternatives | Timeline alternatives |
|---|---|
| [A — Dated hierarchies](#ownership-a--dated-hierarchies) | [A — Calendar lanes](#timeline-a--calendar-lanes) |
| [B — Horizontal lanes](#ownership-b--horizontal-lanes) | [B — Chronological reading](#timeline-b--chronological-reading) |
| [C — Radial maps](#ownership-c--radial-maps) | [C — Firm record panels](#timeline-c--firm-record-panels) |

[Visual inventory](INVENTORY.md) · [Ownership captions, alt text and source map](ownership/README.md) · [Timeline captions, alt text and source map](timelines/README.md)

The figures retain claim IDs and qualifications. Ownership panels represent separate historical disclosures; ranges are not calculated into personal downstream stakes. Timeline markers are observations, not continuous employment. Firm sanctions are not personal sanctions. Unverified early employment and Inferent affiliation remain gaps.
''']
assets = []
for family, stem, title, caption in variants:
    paths = {ext: f'{family}/{stem}.{ext}' for ext in ('svg', 'png', 'pdf')}
    parts.append(f'\n## {title}\n\n{caption}\n\n[Full-size PNG]({paths["png"]}) · [Vector SVG]({paths["svg"]}) · [PDF]({paths["pdf"]})\n\n![{title}. {caption}]({paths["png"]})\n')
    assets.append({'id': stem, 'title': title, 'caption': caption, 'files': paths,
                   'captions_and_alt_text': f'{family}/README.md', 'evidence_map': f'{family}/evidence-map.md',
                   'selected_data': f'{family}/data.json', 'source_commit': snapshot['source_commit']})
parts.append('''
## Provenance and handoff

Research cut-off: **November 4, 2026**. Visualization preparation: **November 5, 2026**. Inputs were pinned from reviewed research commit `0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb`; later housekeeping commits do not change that basis. [Source snapshot and input hashes](source-snapshot.json) identify the exact files. Copies in `inputs/` preserve the original bytes; their original relative links are not rewritten. Use the family evidence maps for working source navigation.

[Independent semantic QA](review/final-qa.md) · [Rendered review](review/render-review.md) · [Package validation](review/package-checks.json) · [Asset manifest](assets.json) · [Scoped SHA256 manifest](SHA256SUMS.txt) · [Tasks](TASKS.md)

The semantic review checks faithful representation of the selected dossier facts; it is not fresh research or a completeness finding. No dossier, source register, HTML front or investigation-level checksum manifest is edited. All deliverables and checkpoints are within this visualization folder. The scoped checksum manifest excludes itself and ignored local runtimes/caches.

The separate dossier/HTML team can embed an approved SVG, use PNG as a fallback, and reuse the supplied caption, alt text and evidence map. Editable DOT/JavaScript and Python sources are retained. No integration or deployment is performed here.

## Rebuild

From this folder, with Python and Node available:

```powershell
npm install --prefix .runtime/graphviz --cache .runtime/npm-cache --no-audit --no-fund @viz-js/viz@3.31.0
python -m pip install --target .runtime/python --cache-dir .runtime/pip-cache -r requirements.txt
node ownership/generate.mjs
python ownership/render.py
python timelines/build_timelines.py
python review/check_semantics.py
python work/package_review.py
python work/validate_package.py
```

The pinned Graphviz dependency lock is also retained in `work/graphviz-package-lock.json`. Family READMEs explain source and layout editing. Package validation regenerates the scoped checksum manifest after checks pass.
''')
(R/'README.md').write_text(''.join(parts), encoding='utf-8')
(R/'assets.json').write_text(json.dumps({'research_cutoff': snapshot['research_cutoff'], 'assets': assets}, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
p = R/'INVENTORY.md'
s = p.read_text(encoding='utf-8-sig').replace('Planned visual treatment', 'Visual treatment').replace('Compact grouped relationship view', 'Radial/diamond node-and-arrow maps')
s = s.replace('The integration package will contain', 'The integration package contains')
p.write_text(s, encoding='utf-8')
p = R/'TASKS.md'
s = p.read_text(encoding='utf-8-sig')
for n in range(3, 7):
    s = s.replace(f'- [ ] T{n}', f'- [x] T{n}')
s = s.replace('- [ ] T7 Commit only visualization files, push migration branch and verify remote bytes.', '- T7 Delivery step: commit only visualization files, push the migration branch and verify remote bytes. The final delivery response records the verified commit; checkpoint 03 records the pre-commit state.')
p.write_text(s, encoding='utf-8')
print('Review gallery, asset manifest, inventory and tasks assembled.')
