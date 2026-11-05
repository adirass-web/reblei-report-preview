# Offline report and evidence dossier: design for review

Date: November 4, 2026. Audience: the in-house diligence team. Status: the user has approved offline delivery, read-only operation and the report-first structure. This document specifies the proposed first version for written review. No HTML application, final diagrams, hosting or deployment has been implemented.

## Confirmed decisions

| Decision | Agreed direction |
|---|---|
| Delivery | An offline folder containing the report and bundled evidence; no hosting for the first version. |
| Review workflow | Read-only browsing, search, filtering and printing. Team comments stay in the existing review process. |
| Starting view | The narrative research report, with the evidence dossier one click away. |
| Research boundaries | Professional public-record findings only; official-record inference explicitly labeled; personal civil proceedings excluded; NYSCEF remains an access gap. |
| Source authority | The reviewed normalized register and preserved originals. Legacy repository material and unavailable Library files are not silently imported. |

The existing [visualization instructions](visualization-instructions.md) are a separate draft for diagrams. This design records the delivery and comment-workflow decisions that have now been made; it does not approve every proposed diagram or diagram style.

## Approaches considered

1. **Portable static HTML folder — selected.** Opens locally, preserves a review snapshot, works without an account or hosting, and keeps evidence with the report. Each distributed copy has a clear version and cut-off; later updates require a new package.
2. **Private hosted static site.** Provides one shared version but requires an approved hosting/access-control arrangement. It can reuse the same content later.
3. **Collaborative review application.** Adds shared comments and assignments but requires storage, user identity and conflict/version handling. It is outside the agreed first version.

The selected approach needs only a small static presentation layer over the existing research package. The normalized register remains authoritative; the browser view does not become a second manually maintained database.

## Reader journey and page structure

### 1. Report: the starting page

Lead with the investigation scope, subject CRD, research cut-off, coverage limits and a short account of what is established and what remains unresolved. Present the following sections in order:

- Key findings and their practical evidence limits.
- Career chronology, using point observations when actual employment intervals are unknown.
- Advisers, employers, funds and ownership intermediaries, grouped into dated Scout/Ophir and EntryPoint views.
- Financial observations, with each metric and measurement-date basis visible.
- Investment-management events, separating firm regulatory matters, arbitration and administrative withdrawals.
- Open questions and the follow-up instruction sheet.

Each substantive finding links to its claim record in the dossier. The first view should be readable as a report without requiring a user to operate a graph or inspect raw tables. Do not manufacture an overall risk rating or confidence percentage.

### 2. Dossier: claims and sources

Provide two main lists: **Claims** and **Documents**, with record detail links. Use plain text search plus a small set of useful filters: entity/person, topic, evidence status, source class and date basis. A filtered count describes the displayed records, not a count of verified facts.

A claim detail shows the exact statement, subject, evidence status, supporting document links, filing/accession/docket identifier, page or table-field locator, and linked conflict or limitation. Display the difference between a filed assertion, official-record inference, unresolved proposition and access observation.

A document detail shows authority, document/source class, original URL, filing/period information, UTC retrieval time, SHA256 and the retained local file. Label derivatives, compressed members, failed responses and unjoined leads as such. Search/failure records remain available for coverage review but must not look like responsive official case evidence.

Use human-readable entity names alongside stable identifiers. Preserve historical name placeholders and rejected namesake status. Administrative-event subjects resolve through linked claims, without labeling the firm a disciplinary respondent.

### 3. Follow-up instructions

Render the separate [remaining-work instructions](../remaining-work-instructions.md), retaining the missing record, exact identifiers, access condition and completion test. Keep NYSCEF's accepted gap prominent. Distinguish work that needs a new record from work that requires changed access or authorization.

No notes, ratings, assignments or saved reviewer decisions are stored in this version. Reviewers can refer to stable claim/document IDs in their existing process.

## Evidence presentation invariants

- A firm sanction is not a personal sanction; a withdrawal is not enforcement; an award is not proof of collection.
- Inferent stays visibly conditional until a direct subject affiliation is established.
- Employment, registration, acquired-status, filing, signature, asset-measurement and cessation dates remain distinct. Unknown dates display as unknown; isolated records do not create continuous tenure bars.
- Ownership bands remain bands. Control, management, general-partner roles, trusteeship and service-provider roles are not interchangeable.
- The report preserves discrepancies and source-specific versions. No silent arithmetic correction, name merge, current-ownership assumption or combined financial metric.
- Every report finding and diagram element must lead to a stable claim and the cited original. Page links use physical PDF page numbers; the page number is also visible because browser PDF handling varies.
- Missing or inaccessible evidence is labeled explicitly. A broken local path must show an understandable unavailable-record message, not an empty panel.
- Essential labels and uncertainty do not depend on color, hovering or animation.

## Portable folder and implementation boundary

Keep the investigation's existing original files and relative paths intact. Put the presentation files under `presentation/`, with `presentation/index.html` as the documented entry point. Distribute the complete investigation folder so local evidence links continue to work. A short opening instruction tells the team which file to double-click.

Use plain HTML, CSS and a small amount of JavaScript for filtering and navigation. Bundle all required assets locally. Generate a compact browser-readable projection from the reviewed index at packaging time; do not require a local server, runtime installation, network fetch, service worker or external font/CDN. Load original PDFs and large archive members only when a reviewer opens them.

Escape source text and restrict generated local links to the package. External official URLs remain explicit user-operated links. Keep every original's bytes unchanged. The presentation version records the input research commit, cut-off, build time and manifest reference so an offline copy can be identified.

The entire archive can be large. The browser should load only the report and compact dossier metadata initially. Large SEC bulk members remain downloadable evidence, not browser-parsed startup data.

## Visual and print direction

Start with a restrained document layout: a short contents navigation, readable text, compact comparison tables and clear evidence links. Use a small number of static, legible diagrams if their separate plan is accepted. The visual inventory should select the minimum useful chronology and dated ownership views; the report remains understandable through accompanying text and tables.

Provide a report print stylesheet with visible source/claim references, sensible page breaks and repeated table headers. Dossier records should also be printable without relying on hidden hover content. Use semantic headings and tables, visible keyboard focus and text labels for status.

## Build sequence after written-design approval

1. Freeze the reviewed data snapshot and produce the small presentation projection with link validation.
2. Build the report, dossier lists/details and follow-up instructions using existing evidence paths.
3. Add only the diagrams accepted in the separate visual plan; retain editable sources and accessible text equivalents.
4. Verify the actual offline workflow and print output; independently check displayed claims, dates, identities and source links.
5. Package and hash the deliverable, commit and push on the active user-approved ReBlei continuation branch, and verify the remote bytes. No default-branch merge or public release.

## Smallest sufficient acceptance checks

- Open the packaged entry point using file:// in an available desktop browser with network access disabled. Report navigation, search, filters and local evidence links work without installation.
- Every displayed claim/document ID resolves; every generated evidence path exists; indexed original SHA256 values remain unchanged.
- Check representative high-consequence examples: Scout firm versus Bleich, the conditional Inferent branch, the three withdrawals, the June 2024 dual flags, MEB naming uncertainty, ownership bands and financial discrepancies.
- Confirm unknown dates and unsupported affiliations remain visible, including in print.
- Inspect keyboard navigation, a narrow window and a printed report sample. Check PDF page links and the visible page fallback.
- Confirm no interface claims that the full career or all litigation has been cleared.

## Decisions still open for the next planning discussion

The delivery model, read-only workflow and report-first structure are settled. The remaining presentation choice is the visual inventory and report depth: which few static diagrams most help this team's first review. Styling can follow a restrained default unless the team supplies an internal template.

The written design above is ready for user review. Implementation is a later action; this research stage delivered the evidence package, independent QA and separate follow-up instructions.

## Editorial standard

Use the [dossier editorial standard](dossier-editorial-standard.md) for narrative drafting and review. Plain English and Humanizer guide clarity and concision; evidence qualifications, legal meanings, quotations and source links remain protected.
