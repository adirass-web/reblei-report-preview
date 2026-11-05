from pathlib import Path
p=Path('outputs/decisions-and-scope.md')
p.write_text('''# Decision and assumption register

Research cut-off: November 4, 2026, Asia/Jerusalem. Full investment-career mandate, executed in sequential stages. Evidence statements describe records as filed; they do not certify the truth of every filer assertion.

## Binding user decisions

- Subject: Michael Edward Bleich, CRD4262671. Keith Michael Bleich CRD2372764 is excluded.
- All historical employers, investment roles, advisers, broker-dealers, funds, SPVs, ownership intermediaries, investment-management regulatory events and litigation are in scope.
- Official public records support findings. Third-party and corporate material are leads only unless a specific official evidentiary provenance is authenticated.
- Litigation is limited to **investment-management conduct**. Personal civil proceedings are excluded. Naming an investment firm in a business-contract case is insufficient by itself.
- No private home, family or unrelated personal investigation. Source originals may incidentally contain public contact fields; analytical outputs omit them.
- Independent specialist research and second-pass adversarial QA are required.
- Search through Parallel Search; stop Firecrawl because credits are exhausted. Tavily discovery returned no available tool/plugin; no claim of Tavily use.
- Preserve all new evidence and work in private repository adirass-web/ReBlei on separate branch `research/bleich-official-records-2026-11-04`, folder `investigations/2026-11-04-official-records/`.
- **Do not use existing repository files for research.** Existing root files are untouched and excluded as sources.

## Consolidated pre-execution defaults, retained with later updates

| Issue | Proposed/applied default | Blocking effect |
|---|---|---|
| Identity | Exact CRD/full name plus cross-source corroboration; no name-only merge | None for verified core identity |
| Prior identifiers | Leads until original record matched | Only unsupported assertions remain blocked |
| Time range | Full documented career through cut-off; no assumed start year | None |
| Geography | US regulators/courts first; follow documented offshore relationships | None |
| Entity perimeter | Legal entities separate; include predecessor/renamed entities only when documented | None |
| Ownership | Direct/indirect ownership, control and employment separate; retain disclosed bands and dates | None |
| Fund structures | Separate master, feeders and each GP; no double counting | None |
| Source standard | Official repositories as evidence; attributed as-filed claims; leads separated | None |
| Regulatory events | Respondent, allegations, settlement, findings and sanction fields separate | None |
| Litigation | Investment-management conduct only, per subsequent user clarification | Nexus must be established before inclusion |
| Negative results | Record query and scope; no-results is not clearance | None |
| Financial metrics | Distinguish RAUM, gross assets, NAV, offering sales,13F holdings, revenue and personal income | None |
| USD999157153 | Quarantined until original ADV obtained | Resolved: original Oct15 2026, measurement Sept30 2026 |
| Inferent | Candidate affiliation, no official role join yet | Blocks treating role as verified |
| Library archive | Attempt accessible retrieval; continue independent official research | Reconciliation blocked; user confirms no local copies |
| Preservation | Original response bytes, URL, identifier, locator, periods, UTC timestamp, SHA256, claim links | None for accessible originals |
| Paid/restricted access | Free authorized access first; no new purchases/accounts | Blocks only paid/new access |
| Outreach | None authorized | Blocks external contact |
| Completeness | Bounded completed stages with search log and gaps; no exhaustive-clearance claim | None |
| Sequence | Identity/entities, filing/ownership history, investment-management events, financial observations, QA/index | Applied in stages; specialists may work independently inside stage |
| Models/tiers | Inherited model on bounded tasks; no claim of cheaper model or tier switching | Model/tier not independently overridden |
| Repository | Separate branch and folder; no merge or deployment | Branch push authorized by preservation instruction; no default-branch changes |

## New ambiguities discovered during execution

1. Scout and Ophir disclose different MEB/Finch ownership bands and status dates. Keep source-specific snapshots; no exact timeless beneficial stake or wrongdoing inference.
2. Ophir Beaufort fund name appears under two private-fund IDs. Treat the mapping as ambiguous, not a confirmed single legal vehicle or proven separate vehicles.
3. EP Third Moment International name and brochures say LP; Forms D select Corporation. Preserve both, obtain Cayman formation evidence before deciding legal form.
4. EntryPoint ScheduleA status acquiredMay2023 differs from a third-party October2020 CIO-career lead. Status-acquired dates are not proof of complete employment history.
5. International/domestic FormD amendments report cumulative offering sales and issuer investor counts; these are neither NAV nor unique people nor period flows.
6. The2024Q3 EntryPoint13F original cover conflicts with its information table. Preserve original values; quarantine comparison; separately label derived reconciliation.
7. The2024Q2 NEW HOLDINGS amendment filed2026 belongs to2024. It is not a2026 period or a replacement full-period total.
8. March2025 and March2026 brochures are preserved; missing October brochure1061309 remains a separate gap.
9. Performance allocation summary states20%, but its sentence is incomplete; hurdles, high-water marks and precise fee computation cannot be reconstructed.
10. NY open-data corporate IDs are provisional name matches, without original owner-linked registry documents or current-status proof.
11. Individual report PDFs returned403; actual FINRA/IAPD searches returned no result. Saved negative-result captures record researcher-supplied query provenance and do not independently capture the input value. None establishes absence of sanctions.

No unresolved decision blocks continued free official-source work. Paid access, outreach and any change to the binding litigation scope require a specific user instruction; elapsed time is not approval.
''',encoding='utf8')
