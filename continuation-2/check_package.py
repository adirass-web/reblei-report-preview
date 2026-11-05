from pathlib import Path
import json,hashlib
root=Path('.'); t=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))['tables']
print('Files',sum(p.is_file() for p in root.rglob('*')),'MiB',round(sum(p.stat().st_size for p in root.rglob('*') if p.is_file())/1048576,2))
for b in ['employment','inferent','ownership','litigation']:
 for name in ['sources.json','claims.json','search-log.json']:json.loads((root/'continuation-2'/b/name).read_text(encoding='utf-8-sig'))
for p in (root/'continuation-2').rglob('*.md'):
 s=p.read_text(encoding='utf-8-sig');assert '\ufffd' not in s,('UTF8 replacement',p)
for x in t['documents']:assert hashlib.sha256((root/x['file_path']).read_bytes()).hexdigest()==x['sha256']
assert len([e for e in t['events'] if e['event_type']=='regulatory_firm_event'])==5
ar=next(e for e in t['events'] if e['event_id']=='LIT3-E001');assert ar['fine_amount'] is None and ar['claimant_entity_id']=='E001' and ar['respondent_entity_id']=='E020'
print('Current source hashes and critical outcome distinctions pass')
print('QAindex exists',(root/'continuation-2/qa-index.md').exists())
