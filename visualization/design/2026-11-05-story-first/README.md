# Story-first visualization design — review proposal

Status: design only, November 5, 2026. No chart generators, rendered charts, dossier or HTML-front files changed. This proposal responds to the user's clarification: show relationships between entities and dates, events or money; tell one story at a time; allow as many useful charts as needed; separate design from coding.

## What changes

The six initial drafts organize a selected inventory into alternative layouts. They preserve evidence, but ask readers to discover the point themselves. Each ownership figure combines three historical structures. Each timeline combines roles, regulatory events and administrative filings. Source identifiers and caveats compete with the relationships being explained, and large page dimensions make ordinary report reading difficult.

The next collection will be designed around reader questions. A chart is admitted only when its relationship and supported takeaway can be stated in one sentence. The unit of work is a story, not a chart type or an arbitrary target count. Twenty or more useful figures are welcome; duplicated views without a separate purpose are not.

The first drafts remain available as reference views. They are not templates that every new story must fit.

## Three editorial approaches

| Approach | Benefit | Cost / risk |
|---|---|---|
| **Question-led story collection — recommended** | A short explanatory chart answers a diligence question; related charts form a chapter. Lets readers stop after an answer or follow evidence. | Requires careful selection and ordering; repeats a few entity labels across charts. |
| Firm-by-firm mini-dossiers | Familiar grouping, useful for specialists assigned one entity. | Cross-firm relationships and distinct legal capacities can become harder to compare. |
| One master network and master timeline | Useful as an appendix or reference index. | Overloads the main narrative; proximity and connecting lines can imply unsupported continuity. |

Use the first approach for the main report, with firm tags for navigation and reference views in the appendix. A sequence of related charts is not a single giant chart.

## How each chart will be designed

Before selecting a tool or writing rendering code, complete a story card:

1. **Reader question and decision:** What does an in-house diligence reader need to understand, and why?
2. **Supported takeaway:** A plain-language sentence, qualified to the strength of the source. This becomes the working headline.
3. **Relationship:** State subject, verb, object and any measure/date: person owns an interest in firm; manager manages fund; panel orders respondent to pay claimant; entity reports a measure at a date.
4. **Evidence and limits:** Claim IDs, source class, date basis, units, uncertainty, relevant conflicts, and what the reader must not infer.
5. **Minimum content:** Only entities and observations needed for this question. Start with roughly 3–6 nodes or observations; larger sets require an explicit comprehension reason.
6. **Visual specification:** Reading order, marks, arrows, scales, labels, focal point and annotation. Choose the form after defining the relationship.
7. **Text equivalent:** A short narrative and a table conveying the same relationship and qualification; full claim/source locators remain in the evidence map.
8. **Reader test:** A question the reader should answer from the chart alone, plus the false inference they should reject.

The [catalogue](story-catalogue.md) proposes distinct stories. The [three detailed storyboards](storyboards.md) show how this works before coding. [Guide notes](guide-notes.md) record the four requested design references and their applications.

## Shared visual grammar

- **Headline:** A supported finding, not a topic label such as “Ownership.” Subtitle states entity, source period and measurement basis.
- **One focal relationship:** Use a single accent to direct attention; supporting elements stay neutral. Colour is not a risk score or a finding of wrongdoing.
- **Entities:** Explicit type labels — person, adviser, fund, regulator or tribunal — where needed. Stable display names; full legal names/IDs in a compact key or source strip. Do not use the same visual role for a firm and a person merely because their names appear in one document.
- **Edges:** Label the verb directly: “holds disclosed interest,” “investment manager,” “signed for,” “ordered to pay,” or “reported repayment.” Uniform arrow widths unless a genuine comparable magnitude is deliberately encoded. An ownership edge is never styled as cash movement.
- **Evidence status:** A documented edge may be solid. An inference, when essential to the story, is dashed and explicitly labelled “inference.” An unverified relationship is generally omitted and described as a gap; no suggestive dotted bridge to Inferent.
- **Dates:** Identify whether a date measures assets, records filing, accepts a settlement or reports acquired status. A snapshot is not a tenure bar. Calendar axes encode elapsed time; editorial sequences explicitly say they do not.
- **Money:** Attach every figure to its entity, measure and time basis. Use a common zero baseline for comparable bars. Keep incompatible measures in separate cards or charts, without a total or subtraction bridge. No Sankey unless actual flow quantities are established.
- **Annotations:** Place the essential qualifier next to the relevant mark. Move detailed evidence identifiers into numbered source notes and an adjacent source map, retaining traceability without turning the figure into a register.
- **Reading size:** Design first for an ordinary report column, approximately 720–960 screen pixels, with a separate print proof at intended size. Main labels should be comfortable at normal view; do not solve crowding by requiring zoom. Split the story when it does not fit.
- **Accessibility:** Direct labels, meaningful reading order, sufficient contrast, non-colour cues and a text narrative/table. Test in monochrome. Meaning must not depend on hover or interaction.

## Design-to-code handoff

| Stage | Output and completion condition |
|---|---|
| 1. Editorial design — current | Proposed stories, takeaways, evidence scope and low-fidelity composition descriptions. No rendering implementation. |
| 2. Storyboard review | Review a small representative set: ownership/control, obligations, comparable observations over time. Agree on story and hierarchy before polished production. |
| 3. Production specification | Freeze selected labels, relationships, source mappings, reading size and acceptance criteria. Only then choose the most efficient renderer for each design. |
| 4. Coding and rendering | Implement approved designs as reproducible static assets. Tool choice may differ between network, temporal and quantitative stories. |
| 5. Separate reviews | Semantic reviewer checks what is asserted; visual reviewer checks what a reader will understand. A factual pass alone is not a clarity pass. |
| 6. Handoff | Approved figures, captions, text equivalents, source maps and editable assets go to the separate dossier/HTML team. |

No implementation is requested from the other team during this phase. The current task is complete when the design proposal is concrete enough to review; implementation awaits storyboard selection.

## Acceptance criteria

A reader unfamiliar with the investigation should be able to identify the subject, relationship and main takeaway quickly, then find the supporting value/date and qualification without searching the dossier. Use this as a qualitative reader exercise, not a claimed test result or scientific timing threshold.

Each eventual chart must pass these checks:

- Can the headline be justified by the selected evidence, including material contradictory context?
- Does every connecting line have an explicit, supported meaning?
- Are party, metric, unit and date basis clear?
- Does the picture imply a transaction, employment interval, causal link, exact ownership stake or payment that the evidence does not establish?
- Can the chart be read at its intended report size without zoom, with no colour-dependent meaning?
- Can an independent reviewer answer its one reader question and reject the named false inference?
- Is there a concise equivalent narrative and traceable source map?

## Assumptions and decisions

No blocking ambiguity prevents design work. Defaults: English, static figures; readers are the in-house diligence team; Nov 4 reviewed research snapshot remains the evidence basis; source interpretation is preserved. Some readers need an overview and others an audit trail, so the chart carries the central story and its nearby source material carries the detail. A chart count is not a quota.

The user decision is which stories and storyboard direction to take into production. Final placement, report width and print requirements can be agreed with the separate HTML/dossier team at handoff; this chat does not edit their work.

Source input commit: `0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb`; initial visualization delivery: `556b60ea6d21650d3105bbdb84e3821c629ba1d5`. All new design work stays under visualization/. Existing source hashes and charts remain unchanged.
