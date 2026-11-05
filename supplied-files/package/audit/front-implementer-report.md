# Reader implementation review

The source-scoped catalogs render the adapter's original fields and IDs, with references to retained originals, physical page images and generated text locators. Deferred mixed records are omitted from rendered catalogs. The reader index projects the adapter output: deferred records retain disposition only, and audit-only canonical records are excluded. Source citations and substantive narrative conclusions are authored and reviewed separately; this implementation introduces no research conclusions.

The static presentation reuses the code/assets of the broader investigation, without its research text, facts, status labels or data. SHA-256 of reference `assets/report.css`: `41754a5b7bafa35fd8e9b50509e274e6d2365681ddfe4c72ade59a6729b3aa1a`; adapted CSS: `6e17ffcb396cb371f13a55c2ce8e61ef194a7a4af9a7c8e9c9f1787266f53c39` (adds print visibility, table wrapping and reader layout adaptations). SHA-256 of reference and reused `assets/report.js`: `0e822065c8d8457814929cb7fe500afc676b5a9d2fd3e437e2379b66cdec1407`.

Browser and static verification output appears under `presentation/review`. The printed reader includes all records regardless of filters; the browser test blocks external network requests.

Final verification: 26 Python tests passed; two builds produced 1,203 files with identical SHA-256 hashes excluding volatile browser review artifacts. Static validation of the final reader passed. The HTTP browser review passed search, filters, print visibility, keyboard interaction, mobile reflow and evidence-link presence; a JavaScript-disabled view displayed records. Both narrative A4 PDFs and desktop/mobile screenshots were generated, and the Scout desktop and mobile screenshots were inspected. The local Chromium policy blocks `file://` with `ERR_BLOCKED_BY_ADMINISTRATOR`, so actual file-opening behavior could not be browser-tested in this environment; static validation checks relative assets and local links, and no network fetch is used by the reader.

Final documentation and keyboard-check update:

- `node --check dossiers/supplied-files/work/check_browser.cjs` — passed.
- `node dossiers/supplied-files/work/check_browser.cjs dossiers/supplied-files/presentation` — passed the HTTP checks, including asserted focus on the collection filter and Tab navigation to Clear filters; JavaScript-disabled reading and both A4 report PDFs also passed. Direct `file://` navigation was blocked by managed Chromium policy and remains unverified.
- `npm ci --no-audit --no-fund --cache /tmp/reblei-npm-cache --prefix /tmp/reblei-bootstrap-check` — passed using the package's copied `package.json` and `package-lock.json` (two packages installed).
- `/tmp/reblei-dossier-venv/bin/python -m pip check` — no broken requirements; pip noted that its default cache was not writable. `node --version` returned `v24.22.1`.
