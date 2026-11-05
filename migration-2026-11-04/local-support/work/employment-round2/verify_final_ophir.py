import json,pathlib,hashlib
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');b=root/'continuation-3/employment'
s=json.loads((b/'sources.json').read_text());ids=[x['document_id'] for x in s];assert len(ids)==len(set(ids))
for v in s:assert hashlib.sha256((root/v['file']).read_bytes()).hexdigest()==v['sha256'],v['document_id']
a=json.loads((b/'claims.json').read_text());assert len({x['claim_id'] for x in a})==len(a)
for c in a:assert all(i in ids for i in c['source_ids'])
assert not list(b.rglob('*.csv'))
print('Verified25sourcehashes,9claimreferences,uniqueIDs; expandedCSVoutsideinvestigation.')
