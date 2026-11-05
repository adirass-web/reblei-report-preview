# Michael Edward Bleich — independent official-record investigation

Research cut-off: **November 4, 2026**. Subject: **CRD4262671**.

This batch establishes the official identity/entity baseline, collects accessible filing histories, records investment-management regulatory events and financial observations, and performs independent adversarial review. **The full-career investigation is not complete.** The continuations add an original Lehman contract schedule, Delaware registry details, three Cboe orders, an original Scout/Wedbush arbitration award, a Wedbush AWC, historical Inferent brochures, Scout audited annual reports, and historical SEC registration/ownership tables, original ERA/ADV-W archive members, and the additional corporate-change and litigation searches. Round 4 adds earlier ERA disclosures, three original ADV-W records, EntryPoint registration history and the NY corporate-change field explanation. Exact employment dates, Inferent linkage, ownership-ID joins and comprehensive investment-management court coverage remain open.

Repository: private `adirass-web/ReBlei`. Separate branch: `research/bleich-official-records-2026-11-04`. This investigation is confined to `investigations/2026-11-04-official-records/`.

**Existing repository material was not used as research evidence.** Existing root files are untouched. Personal civil proceedings and private home/family matters are excluded. The five referenced ChatGPT Library files were inaccessible and have not been reconciled.

## Read first

- [Latest round results](continuation-4/summary.md)
- [Separate remaining-work instructions](remaining-work-instructions.md)
- [Round 3 results](continuation-3/summary.md)
- [Round 2 results](continuation-2/summary.md)
- [Previous continuation results](continuation/summary.md)
- [Findings and gaps](findings-and-gaps.md)
- [Decisions and scope](decisions-and-scope.md)
- [Document index](evidence-index.md)
- [Independent QA](independent-qa.md)
- [Remaining-work instructions](remaining-work-instructions.md)
- [Visualization planning instructions](presentation/visualization-instructions.md)
- [Next-stage retrieval queue](next-stage-queue.md)

## Evidence and structured records

- [Original records and explicitly labelled result captures](evidence/)
- [Normalized JSON index](evidence-index.json)
- [Relational SQLite database](evidence-index.sqlite)
- [Table exports](tables/): persons, entities, identifiers, roles, relationships, documents, claims, claim_evidence, financial_observations, events, event_claims, search_logs, conflicts, conflict_claims, retrieval_attempts and source aliases.
- [Database schema](schema.sql)
- [Validation results](validation.json)
- `SHA256SUMS.txt` verifies all files in this folder except itself. The originals are immutable captured responses; derived text and analysis are separate files.

The index contains **396 captured source representations**, **247 source-linked assertions**, **37 entity entries**, **67 financial observations**, **9 events (five firm regulatory matters, one arbitration and three administrative withdrawal filings)** and **342 search-log entries**. Counts include unresolved names/candidates, transformed captures, archive ranges and access logs; they are not unique filings or verified affiliations. The Scout arbitration identity join remains a labeled inference. Original assertions, allegations, award outcomes and payment/collection remain separate.

## Specialist reports and process records

[Identity](specialist-identity.md) · [SEC entities and filings](specialist-sec.md) · [Investment-management regulatory events](specialist-events.md) · [Corporate candidates](specialist-corporate.md) · [Financial observations](specialist-financial.md)

The corresponding `*-sources.json`, claim/observation JSON and search logs preserve specialist provenance. `work/` retains acquisition, indexing and documentation scripts. The index can be rebuilt from this folder with `python work/build_index.py .` using Python's standard library. Acquisition scripts record this session's working paths; do not bulk rerun them without checking their paths and source limits.

Search providers: native web discovery initially; **Parallel Search** following the user's provider instruction. Direct HTTPS retrieved originals from SEC, FINRA, Nasdaq and government open-data endpoints. Firecrawl's initial requests did not run because credits were exhausted; no subsequent use. No Tavily tool/plugin was available. Interactive browser searches are recorded separately; later collection did not depend on Chrome.

## Evidence interpretation

Official filings are attributed **as filed**, not independently certified financial or legal conclusions. RAUM, private-fund gross assets, FormD cumulative sales and Form13F reportable holdings are distinct. Registration/status dates do not establish complete employment periods. Ownership bands are not exact economic entitlements. Missing results do not establish absence of misconduct.

Independent review checked the core original claims and a bounded second pass over the normalized index. The continuation has cross-specialist provenance review, independent review of all eight Cboe-order pages, and an additional bounded normalized-index review. It did not audit every holding, every filing's arithmetic, all offshore registers or all court systems. Original discrepancies and access gaps remain visible.

## Latest continuation

Round 4 recovers EntryPoint's ERA reporting sequence and the three firms' distinct ADV-W explanations, adds an earlier Ophir role disclosure, and narrows the MEB change-field question. The source-specific limits remain explicit. No new target litigation case was established; this is not a court clearance. Source and normalized-index QA are linked in the latest round report. The separate instruction sheet gives the exact missing records and completion tests.
