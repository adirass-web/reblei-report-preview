
from pathlib import Path
import json,re
root=Path('.')
obj=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'));t=obj['tables'];c={k:len(v) for k,v in t.items()}
p=root/'README.md';s=p.read_text(encoding='utf-8')
s=re.sub(r'The index contains \*\*200 captured source representations\*\*.*?payment/collection remain separate\.',f"The index contains **{c['documents']} captured source representations**, **{c['claims']} source-linked assertions**, **{c['entities']} entity entries**, **{c['financial_observations']} financial observations**, **6 events (five regulatory matters and one arbitration)** and **{c['search_logs']} search-log entries**. Counts include unresolved names/candidates, transformed captures, archive ranges and access logs; they are not unique filings or verified affiliations. The Scout arbitration identity join remains a labeled inference. Original assertions, allegations, award outcomes and payment/collection remain separate.",s,flags=re.S)
p.write_text(s,encoding='utf-8')
lines=['# Preserved document index','','SHA256 identifies retained bytes, not truth of filing assertions. Source classes distinguish original responses, compressed archive members/ranges, derivative extracts, discovery leads and access logs. Physical PDF pages are 1-based. Full locators and claim links are in JSON/SQLite/CSV.','','|Document ID|Source class|Date/period|Local file|Source URL|SHA256|','|---|---|---|---|---|---|']
for d in t['documents']:
 path=d['file_path'];url=d['official_url'];label=Path(path).name
 values=[d['document_id'],d['source_class'],d['filing_date'] or d['period_end'] or '',f'[{label}]({path})',f'[source]({url})' if url else '',f"`{d['sha256']}`"]
 lines.append('|'+'|'.join(str(v or '').replace('|','&#124;') for v in values)+'|')
(root/'evidence-index.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=root/'independent-qa.md';s=p.read_text(encoding='utf-8')
s += """
## Round 3 independent review

See [Scout annual originals](continuation-3/qa-scout.md), [Inferent original brochure and bulk tables](continuation-3/qa-inferent.md), [Ophir historical role/ownership tables](continuation-3/qa-employment.md), [award follow-up](continuation-3/qa-award-followup.md), and [normalized index](continuation-3/qa-index.md).

Corrections include Scout FINRA page locators and nonmembership context, and the material EntryPoint filing-type classification. Exact original flags now state Initial SEC Registration Request=Y in both2021/2024 rows; Final SEC ERA Report is blank in2021 and Y in2024. No reason for dual2024flags is inferred. The derivative table joins were faithful; narrative labels were corrected. Original bytes were unchanged.

The new historical Ophir evidence qualifies the shared04/2012 acquired-status date: it does not independently date the later-added CCO label. MEB INC is a disclosed-name placeholder with unresolved equivalence to MEB NY INC, not an asserted separate incorporated company. Ownership filing snapshots do not become legal transaction dates or exact personal wealth.
"""
p.write_text(s,encoding='utf-8')
p=root/'continuation-3/summary.md';s=p.read_text(encoding='utf-8')
s+=f"\nThe normalized snapshot generated {obj['generated_at_utc']} contains {c['documents']} preserved representations, {c['claims']} source-linked assertions, {c['roles']} role observations, {c['relationships']} relationship observations, {c['financial_observations']} financial observations and six events. All {c['documents']} indexed source hashes and database foreign keys passed the parent build check. Counts include access logs, archive ranges and unresolved candidates, not just original filings.\n"
p.write_text(s,encoding='utf-8')
print(json.dumps(c,indent=2))

