# Michael Edward Bleich — independent official-record investigation

Research cut-off: **November 4, 2026**. Subject: **CRD4262671**.

This batch establishes the official identity/entity baseline, collects accessible filing histories, records investment-management regulatory events and financial observations, and performs independent adversarial review. **The full-career investigation is not complete.** Early career, Inferent linkage, original corporate ownership records and comprehensive investment-management court coverage remain open.

Repository: private `adirass-web/ReBlei`. Separate branch: `research/bleich-official-records-2026-11-04`. This investigation is confined to `investigations/2026-11-04-official-records/`.

**Existing repository material was not used as research evidence.** Existing root files are untouched. Personal civil proceedings and private home/family matters are excluded. The five referenced ChatGPT Library files were inaccessible and have not been reconciled.

## Read first

- [Findings and gaps](findings-and-gaps.md)
- [Decisions and scope](decisions-and-scope.md)
- [Document index](evidence-index.md)
- [Independent QA](independent-qa.md)
- [Next-stage retrieval queue](next-stage-queue.md)

## Evidence and structured records

- [Original records and explicitly labelled result captures](evidence/)
- [Normalized JSON index](evidence-index.json)
- [Relational SQLite database](evidence-index.sqlite)
- [Table exports](tables/): persons, entities, identifiers, roles, relationships, documents, claims, claim_evidence, financial_observations, events, event_claims, search_logs, conflicts, conflict_claims, retrieval_attempts and source aliases.
- [Database schema](schema.sql)
- [Validation results](validation.json)
- `SHA256SUMS.txt` verifies all files in this folder except itself. The originals are immutable captured responses; derived text and analysis are separate files.

The index contains **47 captured source representations**, **104 source-linked assertions**, **31 entity entries including unresolved candidates**, **26 relationships**, **50 financial observation rows** and **55 search-log entries**. These are counts of records, not counts of independently verified facts, unique filings, unique funds, people or events. One representation may support multiple claims. Duplicate specialist references resolve through document aliases.

## Specialist reports and process records

[Identity](specialist-identity.md) · [SEC entities and filings](specialist-sec.md) · [Investment-management regulatory events](specialist-events.md) · [Corporate candidates](specialist-corporate.md) · [Financial observations](specialist-financial.md)

The corresponding `*-sources.json`, claim/observation JSON and search logs preserve specialist provenance. `work/` retains acquisition, indexing and documentation scripts. The index can be rebuilt from this folder with `python work/build_index.py .` using Python's standard library. Acquisition scripts record this session's working paths; do not bulk rerun them without checking their paths and source limits.

Search providers: native web discovery initially; **Parallel Search** following the user's provider instruction. Direct HTTPS retrieved originals from SEC, FINRA, Nasdaq and government open-data endpoints. Firecrawl's initial requests did not run because credits were exhausted; no subsequent use. No Tavily tool/plugin was available. Interactive browser searches are recorded separately; later collection did not depend on Chrome.

## Evidence interpretation

Official filings are attributed **as filed**, not independently certified financial or legal conclusions. RAUM, private-fund gross assets, FormD cumulative sales and Form13F reportable holdings are distinct. Registration/status dates do not establish complete employment periods. Ownership bands are not exact economic entitlements. Missing results do not establish absence of misconduct.

Independent review checked the core original claims and a bounded second pass over the normalized index. It did not audit every holding, every filing's arithmetic, all offshore registers or all court systems. Original discrepancies and access gaps remain visible.
