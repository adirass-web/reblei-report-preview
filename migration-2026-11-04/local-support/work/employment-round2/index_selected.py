import json,pathlib
r=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');t=json.loads((r/'evidence-index.json').read_text(encoding='utf-8-sig'))['tables']
for k in t:print(k,len(t[k]),list(t[k][0]) if t[k] else [])
for k,needles in [('entities',['E034','E004']),('roles',['R002']),('claims',['C008']),('relationships',['2016','E034']),('conflicts',['MEB','combined','EntryPoint'])]:
 print('\nSELECTED',k)
 for x in t[k]:
  if any(n in str(x) for n in needles):print(json.dumps(x,ensure_ascii=True))
