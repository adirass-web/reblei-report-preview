# Independent frontend visualization review

Reviewed 2026-11-05 against `.superpowers/visuals/contract.md` (including the binding static/no-new-PDF clarification), the implementation plan, `.superpowers/visuals/integration-review.diff`, current integration code, the 8 Scout / 7 OPEH manifests, generated reports/galleries, and representative mobile gallery screenshots. Source-semantic chart approval was treated as a separate completed review.

## Verdict

Approved for the reviewed frontend/static presentation contract. The sole material P2 SVG-validation finding is resolved by the final bounded correction and focused independent revalidation below. No unresolved material frontend findings remain. No unsafe resource was observed in the generated figures.

## Material finding — resolved

**P2 — SVG resource validation is incomplete** (`work/build_front.py:106–114`; missing coverage in `work/test_visuals.py`). The checker rejects selected active elements and external-resource attributes, but does not inspect `<style>` text, retains no processing instructions, and allows SVG animation elements. With an otherwise valid real Scout manifest and existing asset paths, an in-memory replacement of the parsed SVG tree accepts each of:

- `<style>@import url(https://example.invalid/style.css);</style>`.
- `<style>@font-face{font-family:x;src:url(https://example.invalid/f.woff)}</style>`.
- `<?xml-stylesheet href="https://example.invalid/style.css" type="text/css"?>` before the SVG root (ElementTree discards the instruction).
- `<a href="#ok"><set attributeName="href" to="https://example.invalid/" begin="0s"/></a>`.

Because full-size SVGs are opened as documents, this violates the requested safe-static-SVG/resource boundary even though image embedding constrains SVG behavior. Use a supported static-element vocabulary or otherwise reject animation and stylesheet instructions; validate stylesheet text/resource constructs as well as attributes. Add meaningful rejection tests. These reproductions do not modify the checked-in figures or contact external addresses.

## Passing review evidence

- The current complete static validator returned `True` on `presentation/` and its index.
- Manifest loading requires the 8/7 counts, unique lane-prefixed IDs, five inline entries, nonempty titles/summary/limitations/alt text/data, same-lane record IDs, exact owned artifact paths and no escaped or symlinked artifact destinations.
- The shared renderer emits visible summaries, limitations, source record links, data tables, and ordinary full-size SVG links plus SVG/PNG/CSV/JSON downloads. Null/missing table values render as `Unknown`. Figure content has no new selector, tooltip or expandable data mechanism; JavaScript remains the existing record/print reader behavior.
- The two reports contain five inline figures each; the two galleries contain all eight/seven. All palette entries use the agreed six colors. Labels accompany color, and the Scout $1 source difference is visible in its summary/limitation and labeled magenta SVG callout without a materiality conclusion. OPEH rounding/calendar qualifications remain visible and conditional.
- Financial table cells carry asset/liability/equity classes with explicit text legend and solid 4px category borders in the actual stylesheet. Existing browser acceptance additionally checks their computed colors.
- Inspected `presentation/review/scout-visuals-mobile.png` and `opeh-visuals-mobile.png`: gallery headings/cards reflow within 375px, figures retain their full composition, and a normal full-size link follows each figure for small chart labels. The reviewer did not change managed browser policy or use blocked direct file navigation.
- `work/check_browser.cjs` contains no PDF generation call. The existing browser log records managed `file://` blocking, successful HTTP/no-JavaScript checks, visible limitations/data, loaded SVGs, source/data links, and mobile overflow checks for both galleries. Historical PDFs are labeled previous-edition copies in README.

No feature expansion is requested. Final build/test/seal evidence belongs to the coordinator/integration report.

## Focused correction rereview

The initial correction rejects the original CSS import/font-face, animation and stylesheet-instruction fixtures, including UTF-16 input; independently rerunning `python -m unittest discover -s work -p test_visuals.py` passed all 7 tests and positive validation of all 15 figures. The static-element/attribute/reference restriction is bounded to the generated vocabulary.

However, the same P2 remained reproducible because `work/build_front.py:127` checks only `style.text`, ignoring child-element tails. A supported child element splits CSS into unchecked tail content:

```xml
<style>*{stroke-linejoin: round; stroke-linecap: butt}<g/>@font-face{font-family:foo;src:url(http://127.0.0.1:8923/font.woff)}text{font-family:foo}</style>
<text x="10" y="30">test</text>
```

The corrected validator accepted this payload using an in-memory byte replacement and the valid real manifest/assets. A separate managed Chromium HTTP-route reproduction parsed the external font-face rule and requested the local font URL; the request was intercepted and aborted, with no policy change. Rejecting child elements within the fixed stylesheet (plus a regression fixture) closes this bypass without changing generated figures.

The same focused rereview confirmed a second CSS resource syntax not covered by the `url(...)` filter: a root `style="background-image:image-set(&quot;http://127.0.0.1:8923/bg.png&quot; 1x)"` attribute. The validator accepted it; managed Chromium requested the local image URL (intercepted and aborted). Restrict inline declarations to the small generated static-property vocabulary and local paint-reference syntax, rather than accepting arbitrary CSS properties and resource functions. This remains part of the original P2 boundary correction.

## Final focused revalidation — approved

The final correction rejects stylesheet child elements and restricts inline CSS to the eleven properties observed in the frozen chart output, simple literal values, and a same-document `fill:url(#id)` reference. This closes both demonstrated follow-up resource-loading routes without changing figure assets or presentation behavior. The changes stay within the original safe-static-SVG validation requirement.

Independently reran `/tmp/reblei-dossier-venv/bin/python -m unittest discover -s work -p test_visuals.py`: **7 tests passed**, including all original attack fixtures, UTF-16, mixed stylesheet-tail and inline image-set cases, plus positive validation of all 15 current figures. Independently repeated the two follow-up in-memory payload checks against the final validator: mixed stylesheet-tail rejected with `Unsupported SVG stylesheet`; inline image-set rejected with `Unsupported SVG CSS property`; real manifest loading returned **15 valid figures**. The final code/fixture review found no material regression within the fix scope. The screenshot naming mismatch is corrected to `financial-legend-desktop.png` in the browser checker and artifact.

Final verdict: **P2 addressed; no unresolved material frontend/spec-quality finding.** The coordinator retains final full-build, test, seal and deployment responsibility.
