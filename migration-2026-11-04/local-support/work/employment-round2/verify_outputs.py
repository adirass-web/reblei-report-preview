import json,pathlib,hashlib
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-2/employment'
for f in ['sources.json','claims.json','search-log.json']:
 a=json.loads((base/f).read_text(encoding='utf-8-sig'));assert isinstance(a,list)
sources=json.loads((base/'sources.json').read_text());ids=[x['document_id'] for x in sources];assert len(ids)==len(set(ids))
for s in sources:
 if 'file' in s: assert hashlib.sha256((root/s['file']).read_bytes()).hexdigest()==s['sha256'],s['document_id']
for c in json.loads((base/'claims.json').read_text()):assert all(i in ids for i in c['source_ids'])
print('JSON arrays, unique source IDs, all local file hashes and claim references verified.')
