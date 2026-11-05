import json,pathlib,csv
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');t=json.loads((root/'evidence-index.json').read_text(encoding='utf-8-sig'))['tables'];docs={x['document_id']:x for x in t['documents']};aliases={x['alias_id']:x['document_id'] for x in t['document_aliases']}
for cid in ['EMP4-C05','EMP4-C07','EMP4-C08','EMP4-C09','INF4-C008','LIT3-C07']:
 print('\nCLAIM',cid)
 for e in t['claim_evidence']:
  if e['claim_id']==cid:
   d=docs[e['document_id']];print(d['document_id'],d['file_path'],d['official_url'],e['locator'])
print('\nEVENTS')
for e in t['events']:print(json.dumps(e))
print('\nORIGINAL FILING TYPES SELECTED ROWS')
p=root/'continuation-3/inferent/raw/ADV_Filing_Types_20111105_20241231.csv'
print('exists',p.exists())
if p.exists():
 with p.open(encoding='latin-1',newline='') as f:
  for r in csv.DictReader(f):
   if r['FilingID'] in ['1542238','1869875']:print(json.dumps(r))
