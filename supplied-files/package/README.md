# Scout and OPEH — supplied-files dossiers

This package presents **two separate dossiers**, each with a source-scoped profile and financial reconstruction. Open [the reader](presentation/index.html), then choose Scout or OPEH. Keep the package together so its evidence links continue to work.

| Dossier | Supplied basis | Occurrences / unique documents | Financial findings / calculations |
| --- | --- | --- | --- |
| Scout | Scout archive and the standalone Nasdaq PDF | 20 / 18 | 17 / 104 |
| OPEH | OPEH litigation archive | 21 / 20 | 9 / 25 |

The underlying research is historical and source limited. Nothing in this release updates employment, balances, payment status or litigation status beyond the supplied record. The independent public-record investigation is a separate project and supplies no evidence or narrative to these dossiers. Official records that were already supplied remain described as supplied copies.

## Read and use evidence

Each report contains executive findings, source boundaries, a scoped profile, chronology, financial reconstruction, discrepancies and attributed appendices. The linked record and document catalogues retain original IDs, confidence, attribution, conditions and citations. A PDF locator means a physical PDF page; it need not match a printed page number. Non-PDF citations retain their line, row or section basis. Byte-identical aliases remain visible without multiplying an event or obligation.

The supplied standalone Nasdaq PDF is a composite. Its first two physical pages contain complaint material; pages 3–13 contain acceptance/AWC material. Its filename does not establish a personal fine. The OPEH source-named maker is not silently merged with the regulated identity. An asserted debt is not an award; a payment election or discontinuance is not payment evidence.

Unsupported imported research statements and peripheral supplied material are retained in attributed appendices and evidence catalogues. Their embedded external references are unretrieved references. Mixed Scout/OPEH arguments are deferred in the coverage register; the reports contain individual boundary notes rather than a combined argument.

Search is scoped to the dossier being read. Evidence labels and qualifications remain part of the result. Basic reading and browser Find work without JavaScript. Print the report page for its complete narrative; active search filters must not remove content from print output. Detailed catalogues can be printed separately.

## Edit and rebuild

The editable narratives are [Scout](scout/dossier.md) and [OPEH](opeh/dossier.md). Generated HTML is a view of those manuscripts and the accepted analytical records; do not edit it by hand.

1. Create a local editorial branch and edit the appropriate Markdown manuscript.
2. Link every substantive conclusion to a same-dossier analytical record, using `[label](record:ORIGINAL-ID)`, or to a supplied source, using `[physical page](doc:SHA256#page=N)`. Non-PDF locators use `#line=N`, `#row=N` or `#section=body`.
3. Preserve attribution, evidentiary status, identity/capacity distinctions, confidence and scenario conditions beside the relevant statement or amount. Unsupported secondary material stays in its attributed appendix.
4. Review the manuscript diff and the cited original pages. Record substantive review in `audit/`. Do not add another dossier's sources or external research to support a conclusion.
5. Rebuild, validate and run the browser checks below. Review both the HTML and the full print output before issuing a new sealed copy.

Use the repository's accepted corpus and profile/financial analysis as read-only inputs. Do not run the old corpus renderer or reconstruction renderer merely to rebuild this presentation: those commands write earlier analytical outputs. Re-extraction and OCR are unnecessary for ordinary editing.

An analytical correction requires an explicit reviewed erratum naming the affected original record, corrected interpretation, supporting source and reason. Do not silently modify the accepted baseline or re-freeze an unexpected hash mismatch. External retrieval or integration with the independent investigation is a separate future change.

## Maintainer toolchain

Readers need only a browser. Maintainers use Python 3, MarkdownIt, Beautiful Soup and Node/Playwright, matching the broader investigation's static presentation stack. Presentation reuse provenance is recorded in [audit/reuse-provenance.json](audit/reuse-provenance.json); research data was not copied from that branch.

From this package directory, use Python 3 and Node.js 20 or newer. Create a virtual environment and install the pinned Python and Node dependencies:

```sh
python3 -m venv /tmp/reblei-dossier-venv
/tmp/reblei-dossier-venv/bin/python -m pip install -r requirements.txt
npm ci
```

The browser check prefers `/usr/bin/chromium` when present. Set `CHROMIUM_PATH` to use another existing Chromium executable. If no system Chromium is available, install Playwright's matching browser with `npx playwright install chromium`; the check then uses that browser. Managed browser policies remain in effect.

Activate the environment, then run the checks and seal from the package directory:

```sh
. /tmp/reblei-dossier-venv/bin/activate
```


```sh
python work/build_front.py --validate
python work/validate_front.py
node work/check_browser.cjs
python work/seal_package.py
python work/seal_package.py --verify
```

The builder supports `--output DIRECTORY` for isolated verification builds. See the final validation records for the exact executed commands, tool versions and outcomes. The release manifest records hashes; the input manifest records the immutable baseline. No public deployment, new retrieval, branch merge or push is part of this package.

## Structured exports and release verification

The seal command generates separate `exports/scout/` and `exports/opeh/` directories: raw scoped records (JSONL), financial findings, calculations, discrepancies and source inventories (CSV). CSV values that could execute as spreadsheet formulas receive a leading apostrophe; raw values remain unchanged in JSONL. Display results, exact results, scenario assumptions and evidentiary qualifications remain separate fields.

`audit/release-manifest.json` hashes the package, including its evidence assets and review records. `--verify` checks bytes and file membership, rejecting unexpected files, missing files, tampering and symlinks. Caches, dependencies installed locally and the manifest's own verification output are excluded as documented by the tool. After an editorial change, validate and review before creating a new manifest; a successful re-seal is not a substitute for source review.

The input freeze covers the original corpus and analytical package. The release manifest covers this new dossier package. Neither establishes authenticity of original signatures, present balances, legal enforceability or completeness beyond the supplied record.

| Dossier | Findings | Calculations | Discrepancies | Raw records |
| --- | --- | --- | --- | --- |
| Scout | [CSV](exports/scout/financial_findings.csv) | [CSV](exports/scout/calculations.csv) | [CSV](exports/scout/discrepancies.csv) | [JSONL](exports/scout/records.jsonl) |
| OPEH | [CSV](exports/opeh/financial_findings.csv) | [CSV](exports/opeh/calculations.csv) | [CSV](exports/opeh/discrepancies.csv) | [JSONL](exports/opeh/records.jsonl) |

Historical PDFs from the previous edition (not updated for these visuals): [Scout PDF](presentation/review/scout-report.pdf) and [OPEH PDF](presentation/review/opeh-report.pdf). Validation evidence is in [audit/validation-summary.json](audit/validation-summary.json). Managed Chromium blocked direct `file://` navigation during acceptance testing; HTTP operation, JavaScript-disabled reading, print visibility and relative-link integrity were checked. No managed browser policy was changed.

## Regenerate the static visualizations

The eight Scout and seven OPEH visuals use one semantic palette: blue assets, amber liabilities, teal equity, purple conditional scenarios and gray unavailable evidence. Magenta outlines and labeled callouts emphasize key findings or source differences. Color accompanies labels and patterns. Figures have no selectors, hover controls or expandable data; their captions, qualifications, source links and accessible tables are visible. Each has a normal full-size SVG link plus SVG/PNG/CSV/JSON downloads.

Use Python with the pinned plotting dependency in `requirements-visuals.txt` to regenerate the figures from this package directory:

```sh
python work/visuals/scout.py --index data/evidence-index.json --output presentation
python work/visuals/opeh.py --index data/evidence-index.json --output presentation
```

Then rebuild and validate the HTML with the pinned reader dependencies and follow the release sealing procedure above. The original accepted corpus and analytical records remain read-only. No new PDF is generated for the visualization edition; earlier PDFs are historical copies without these visuals.

Visualization edition checks: [validation summary](audit/visuals-validation-summary.json), [source review](audit/visuals-source-independent-review.md) and [frontend review](audit/visuals-frontend-independent-review.md).
