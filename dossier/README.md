# Michael Edward Bleich dossier

Start with the [full dossier](full-dossier.md). It presents the reviewed research as a standalone account for the in-house diligence team, with a November 4, 2026 evidence cut-off. The written dossier is complete; the specified employment, corporate and court-record gaps remain open.

## Evidence appendices

- [All 247 claims and 444 evidence links](claims.md)
- [All 396 retained source representations](documents.md)
- [People, entities, identifiers, roles and relationships](entities-and-roles.md)
- [Nine events, including three administrative withdrawals](events.md)
- [All 67 financial observations](financial-observations.md)
- [All 26 conflicts and qualifications](conflicts-and-gaps.md)
- [Separate remaining-work instructions](../remaining-work-instructions.md)

## Review and preservation

[Independent fidelity review](review/independent-fidelity-review.md), [career and entity cross-review](review/career-entities-cross-review.md), and [events and finance cross-review](review/events-finance-cross-review.md) record the checks and corrections. Review was bounded; it does not establish exhaustive career or court coverage.

[Coverage](coverage.json) maps narrative references and appendix entries. [Release verification](release.json) records the input commit, source integrity and local-link checks. Original records, the evidence index, historical research notes and the remaining-work instructions have not been rewritten.

The manuscript and appendices are Markdown files. HTML layout and print rendering are separate future implementation work under the [agreed design](../presentation/offline-report-design.md).

## Editing and rebuilding

The current authored text is in `sections/`. The generator `work/build_dossier.py` expands exact claim references and builds appendices from the unchanged evidence index. The JSON narrative input and correction files in `work/` retain drafting history; they are not the current manuscript and must not overwrite reviewed sections.

After an authorized narrative edit, rebuild from the investigation root with `python dossier/work/build_dossier.py`, obtain review of changed consequential passages, and run `python dossier/work/validate_dossier.py`. That command creates the versioned dossier release record. Then reseal and preserve the authorized branch. Do not rerun historical migration scripts as a new release check.
