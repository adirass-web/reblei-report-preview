import json,pathlib
r=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records')
for name in ['identity-sources.json','sec-sources.json']:
 a=json.loads((r/name).read_text(encoding='utf-8-sig'))
 for x in a if isinstance(a,list) else a.get('sources',[]):
  if 'id-sec-ophir-164729-adv.pdf' in str(x):print(json.dumps(x))
