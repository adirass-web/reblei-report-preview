import pathlib,json,hashlib
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');b=root/'continuation-4/employment-inferent';s=json.loads((b/'sources.json').read_text());c=json.loads((b/'claims.json').read_text());logs=json.loads((b/'search-log.json').read_text());ids={x['document_id'] for x in s};assert len(ids)==len(s)==16
for x in s:
 p=root/x['file'];assert p.resolve().is_relative_to(root.resolve());assert hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256'],x['document_id']
for x in c:
 assert all(i in ids for i in x['source_ids']);assert [e['document_id'] for e in x['evidence']]==x['source_ids'];assert len(x['locators'])==len(x['evidence'])
assert len({x['claim_id'] for x in c})==len(c)==8
assert len(logs)==4;assert not list(b.rglob('*.csv'));assert (b/'report.md').exists() and (b/'remaining-instructions.md').exists()
print('All16sourcehashes,8claims/source-specificevidence,4logs and requiredoutputs verified; no expandedCSV inpacket.')
