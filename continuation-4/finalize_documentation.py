"""Update research navigation and preserve the user's visualization planning brief."""
from pathlib import Path
import json
p=Path('.')
t=json.loads((p/'evidence-index.json').read_text(encoding='utf-8'))['tables']
f=p/'README.md';s=f.read_text(encoding='utf-8')
s=s.replace('[Latest round results](continuation-3/summary.md)','[Latest round results](continuation-4/summary.md)\n- [Round 3 results](continuation-3/summary.md)')
s=s.replace('- [Next-stage retrieval queue](next-stage-queue.md)','- [Remaining-work instructions](remaining-work-instructions.md)\n- [Visualization planning instructions](presentation/visualization-instructions.md)\n- [Next-stage retrieval queue](next-stage-queue.md)')
s=s.replace('**329 captured source representations**, **214 source-linked assertions**, **34 entity entries**, **57 financial observations**, **6 events (five regulatory matters and one arbitration)** and **265 search-log entries**','**396 captured source representations**, **247 source-linked assertions**, **37 entity entries**, **67 financial observations**, **9 events (five firm regulatory matters, one arbitration and three administrative withdrawal filings)** and **342 search-log entries**')
s=s.replace('Exact employment dates, Inferent linkage, ownership-ID joins and comprehensive investment-management court coverage remain open.','Round 4 adds earlier ERA disclosures, three original ADV-W records, EntryPoint registration history and the NY corporate-change field explanation. Exact employment dates, Inferent linkage, ownership-ID joins and comprehensive investment-management court coverage remain open.')
f.write_text(s,encoding='utf-8')
f=p/'findings-and-gaps.md';s=f.read_text(encoding='utf-8')
intro='''# Research findings and remaining gaps

## Latest reviewed additions: round 4

The [round 4 findings](continuation-4/summary.md) add the earlier Ophir ERA disclosure, distinguish Ophir's reported 2017 cessation from Inferent's stated continuing activity in 2020, and recover EntryPoint's 2021 withdrawal and 2022-2024 ERA sequence. Official instructions explain the dual final-ERA/initial-application flags as procedurally consistent with a registration transition; eligibility, approval and legal corporate history remain distinct questions.

New York's 2009 MEB record is coded as a process-address change, not proof of a rename. Historical EntryPoint ownership records add intermediaries and exact professional overlaps; they do not establish a Bleich-Inferent relationship. No new responsive litigation event was established by the bounded searches. NYSCEF remains an accepted access gap.

The exact early employment dates, Inferent role, owner-linked corporate identifiers and comprehensive court coverage remain unresolved. [Separate follow-up instructions](remaining-work-instructions.md) specify the missing originals and completion tests. The earlier findings below remain subject to these later qualifications.

'''
if not s.startswith('# Research findings and remaining gaps'):
 s=intro+s
f.write_text(s,encoding='utf-8')
(p/'next-stage-queue.md').write_text('''# Remaining retrieval queue after round 4

The current actionable queue is [Remaining-work instructions](remaining-work-instructions.md). It replaces the round 3 queue, including the now-explained EntryPoint dual filing flags.

Priorities are early employment; direct Inferent role/transaction evidence; complete registration approval and post-withdrawal history; owner-linked corporate originals; targeted investment-management litigation follow-up; missing brochures/offshore instruments; financial/date discrepancies; and reconciliation of the unavailable Library files.

NYSCEF remains an accepted access gap with no further attempt. No PACER account, new account, fee, outreach or default-branch merge is authorized. Completed scans and unchanged blocked endpoints should not be repeated without new data, access or a specific discrepancy.

For the next presentation discussion, see [visualization instructions](presentation/visualization-instructions.md). These are proposed instructions, not an approved design or implemented website.
''',encoding='utf-8')
f=p/'independent-qa.md';s=f.read_text(encoding='utf-8')
s+='''
## Round 4 independent review

See [employment/Inferent](continuation-4/qa-employment-inferent.md), [registration/withdrawals](continuation-4/qa-registration-withdrawals.md), [corporate identity](continuation-4/qa-corporate-identity.md), [litigation](continuation-4/qa-litigation.md), and [consolidated index](continuation-4/qa-index.md).

The round 3 statement that the dual 2024 flags remained unexplained is historical. Newly retrieved official instructions now support a labeled procedural interpretation; they do not adjudicate eligibility, approval, timeliness or corporate identity. The three new withdrawal records are administrative filings, with no respondent or fine assigned.

The consolidated review verified all 396 indexed document hashes, all 17 JSON/SQLite table comparisons, 247 claim evidence links and the 33 round 4 claims. This is source and integration QA within the recorded scope, not comprehensive employment, court or adverse-history clearance. The remaining work is listed separately.
'''
f.write_text(s,encoding='utf-8')
lines=['# Preserved document index','','SHA256 identifies retained bytes, not truth of filing assertions. Source classes distinguish original responses, compressed archive members/ranges, derivatives, discovery leads and access logs. Physical PDF pages are 1-based; CSV locators state their own header convention. Exact field/page locators and claim links are in JSON/SQLite/CSV.','','|Document ID|Source class|Date/period|Retrieved UTC|Local file|Source URL|SHA256|','|---|---|---|---|---|---|---|']
def clean(v):return str(v or '').replace('|','/').replace('\n',' ')
for d in t['documents']:
 path=d['file_path']
 lines.append('|'+ '|'.join([clean(d['document_id']),clean(d['source_class']),clean(d['filing_date'] or d['period_end']),clean(d['retrieved_at_utc']),f"[{Path(path).name}]({path})",f"[source]({d['official_url']})" if d['official_url'] else '', chr(96)+d['sha256']+chr(96)])+'|')
(p/'evidence-index.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
f=p/'continuation-4/employment-inferent/remaining-instructions.md'
s=f.read_text(encoding='utf-8').replace('parent claims EP5-W1 onward','parent claims EP5-C004 through EP5-C006')
f.write_text(s,encoding='utf-8')
(p/'presentation').mkdir(exist_ok=True)
(p/'presentation/visualization-instructions.md').write_text('''# Proposed instructions: visual research report and dossier

Status: instruction draft for discussion. No diagrams, HTML front, hosting or publication have been implemented. The user requested planning after the research stage and permits static visualization.

## Objective and sequence

After consolidating the research findings, completing independent QA and listing unresolved evidence gaps separately, plan a small set of clear visuals for the in-house diligence team. Use the Visualize skill for useful in-conversation previews, or a suitable static diagram tool for report-ready output. The simple HTML report and dossier are project deliverables; an inline preview is not automatically a standalone website.

First produce a visual plan for discussion, then agree the presentation structure with the user before creating the final visuals. Do not delay an accurately qualified report merely because some historical records remain inaccessible. Clearly state the research cut-off and coverage limits.

## Visuals to plan

1. **Professional chronology:** aligned lanes for documented roles, dated disclosures, and separately labeled unverified career leads. Distinguish employment dates from registration, filing, signature and acquired-status dates. Use point observations where start/end dates are unknown; do not draw continuous tenure bars from isolated filings.
2. **Corporate and fund networks:** separate dated views of the Scout/Ophir and EntryPoint structures. Label people, advisers, broker-dealers, funds, SPVs, GPs and ownership intermediaries by type and verified identifier. Label every edge by its specific relationship, ownership band and source period. Keep control, management, ownership, trusteeship and service-provider relationships distinct. Avoid a single crowded, timeless network.
3. **Registration and entity-history flowcharts:** show the verified EntryPoint application, withdrawal, ERA reporting and later application sequence. Show Ophir's reported cessation and Inferent's stated continuing activity separately. Use arrows to mean an explicitly labeled sequence or relationship; do not imply merger, succession, asset transfer or causation without supporting evidence.
4. **Investment-management events timeline:** separate firm regulatory matters, arbitration/court proceedings and administrative filings. Identify the respondent or party and the stage: allegation, settlement, award, order or later enforcement. A withdrawal is not a sanction, a firm sanction is not a personal sanction, and an award is not proof of collection.

Keep Inferent visibly conditional until a direct Bleich affiliation is established. Keep unresolved corporate candidates and rejected namesakes outside confirmed ownership chains. Exclude personal civil proceedings and private home/family details.

## Evidence and visual rules

- Use only the reviewed normalized register and preserved official records for factual content. Third-party material may appear only as an expressly labeled lead.
- Give every substantive node, relationship and event a claim ID and an accessible source reference to the document, filing/accession/docket and physical page or table field. In static exports, use a readable numbered source key; essential information must not depend on hovering.
- Distinguish **documented as filed**, **official-record inference**, **unresolved**, and **access gap** with text and line/shape conventions, not color alone. Do not invent confidence percentages or risk scores.
- Show historical snapshots and date precision explicitly. Preserve conflicting names/dates rather than silently choosing one. Ownership ranges must remain ranges; a trustee role must not become a percentage.
- Preserve the Scout firm-versus-Bleich distinction and exclude Keith Michael Bleich. Avoid visual proximity or unlabeled arrows that imply an unproved affiliation.
- If financial figures are later added, keep RAUM, ERA private-fund assets, fund gross assets, Form D sales and 13F holdings in separate, correctly labeled measures. Retain the known discrepancies and unknown measurement dates.
- Favor a few legible diagrams over a dense master graph. Use restrained styling, plain-language legends, accessible text alternatives and print-readable labels.

## Proposed report and dossier arrangement

Use the report to explain the findings, chronology, structures and material limitations. Use the dossier to let reviewers follow each claim to its source and see unresolved questions. Plan a simple read-only HTML front first; interactivity is optional and should serve a specific review need.

Static diagrams are acceptable. Retain editable diagram sources and reusable vector output, with a print-friendly export where useful. Keep source evidence unchanged. Decide offline delivery versus a private internal address with the user before choosing hosting or dependencies; do not publish publicly by default.

## Planning deliverables and review

Prepare a visual inventory stating, for each proposed diagram: its audience question, included entities/events, date scope, source claims, unresolved issues, intended placement and output format. Recommend the smallest coherent set and show how it connects the report to the dossier.

Have an independent reviewer check identity joins, arrow meanings, dates, ownership bands, event attribution and source references before finalization. Check readability on screen and in print. Save plans, editable sources, rendered visuals and QA on the existing ReBlei research branch inside this investigation folder.

Open decisions for later discussion are delivery method, report depth, whether review comments are needed, and the approved visual plan. This instruction draft does not authorize accounts, paid services, outreach, deployment or a default-branch merge.
''',encoding='utf-8')
print('Updated navigation, document index, remaining-work pointers and visualization instruction draft.')

