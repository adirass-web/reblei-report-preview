# Timeline draft comparison

These are visualization-only drafts from the pinned dossier at commit `0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb`, research cut-off **4 November 2026**. All three show the **same 16 selected observations**, spanning 2009–2026; the axis extends to 2027 to give the last record space. They are a selection, not a complete career history or a clearance.

| Draft | Caption and layout trade-off |
|---|---|
| [A — Calendar lanes](timeline-a.svg) · [PDF](timeline-a.pdf) · [PNG](timeline-a.png) | Dated observations on a true calendar axis, grouped into role, regulatory/award, and firm/administration lanes. Best for elapsed-time comparisons and separating types of records. Requires a wide page and reading across to the aligned labels. |
| [B — Chronological reading](timeline-b.svg) · [PDF](timeline-b.pdf) · [PNG](timeline-b.png) | Two-column editorial chronology; read down the left, then the right. Best for uninterrupted narrative reading. Equal vertical spacing is explicitly **not to scale** and does not convey duration. The May 2009 status observation is a month-level observation; its exact order relative to May 20 formation is unknown. |
| [C — Firm record panels](timeline-c.svg) · [PDF](timeline-c.pdf) · [PNG](timeline-c.png) | Three small multiples with the same full calendar axis: Scout/related matters, Ophir and EntryPoint. Best for firm-by-firm review with common temporal context. Panel heights follow observation counts; blank years do not establish inactivity. Scout context includes a distinctly labeled Wedbush action and the arbitration. |

Shared visual language: teal role disclosures, rust regulatory/award records, indigo firm/administration. Colors are reinforced by text labels and grouping. A diamond marks month precision and approximate axis placement; circles use the stated day basis. No tenure bars, implied job transitions or continuity connectors are drawn.

## Alt text

**A:** A calendar dot plot of 16 selected observations from May 2009 through October 2026. Five role disclosures sit in a teal lane, five regulatory or award observations in a rust lane, and six firm or administrative observations in an indigo lane. The role records cover Scout, Ophir and EntryPoint. Firm sanctions are attributed to their respondents; a Scout/Wedbush award is an obligation rather than proof of payment. A legend and reading limits explain uncertain employment dates.

**B:** A numbered two-column sequence of the same 16 observations, starting with Scout's May 2009 acquired-status disclosure and ending with EntryPoint's October 2026 Form ADV. The middle records distinguish Ophir title disclosures, Scout firm settlements, a separate Wedbush settlement, the November 2016 arbitration record and distinct adviser withdrawal circumstances. Equal spacing is explicitly not a time scale.

**C:** Three stacked firm panels with identical horizontal year scales from 2009 to 2027. Scout and related matters contain eight observations through November 2016; Ophir contains three filing observations from 2012 to 2017; EntryPoint contains five from 2021 to 2026. All labels include observation and claim identifiers. Empty time spans convey no employment or operational finding.

## Evidence and interpretation

[Machine-readable observations](data.json) include claim IDs, exact date basis, precision, full pinned claim text, source classes and page/row locators. [Evidence map](evidence-map.md) reproduces each selected claim's supporting records and exact locators outside the figures. The governing inputs are `../inputs/full-dossier.md`, `claims.md` and `evidence-index.json`. No new external research was performed.

Acquired-status months are not exact hiring dates. Ophir's March 2015 combined title does not establish an April 2012 CCO appointment. Withdrawal dates, stated cessation dates and signature dates remain separate. EntryPoint's June 2024 dual flags are one filing, not two events or evidence of approval. Scout's USD3m fine is a firm sanction; no separate personal sanction is inferred. The award is served/indexed November 18, 2016, signed November 16; it proves awarded obligations, not collection, and its Scout CRD join is an official-record inference. The June 26/July 3, 2013 Cboe date discrepancy is not plotted because that matter is outside this selected subset. Early Chase/Lehman/Barclays dates and the Inferent role remain unresolved and are not assigned to the axis.

## Rebuild and review

Run `python build_timelines.py`. The script loads the parent-local `.runtime/python` matplotlib installation and writes only this folder; `MPLCONFIGDIR` and temporary PDF renderings use ignored `.cache/`. Fonts remain text in SVG; PDF uses embedded TrueType fonts. The outputs are large-format vector drafts; print at native page size or use zoom for the full labels.

All three PNG figures were opened and inspected. The first C panel spacing was expanded after inspection to remove overlapping claim lines. Literal currency text, month precision, figure-edge bounds and the service/signature distinction were checked. PDFs were independently rendered for a second visual pass. Final acceptance of a layout remains with the user.
