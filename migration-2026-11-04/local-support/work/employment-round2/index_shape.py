import json,pathlib,sqlite3
r=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');a=json.loads((r/'evidence-index.json').read_text(encoding='utf-8-sig'));print('KEYS',list(a));
for k,v in a.items():
 if isinstance(v,list):print(k,len(v),v[0] if k in ['roles','entities','documents','relationships','conflicts'] else list(v[0]) if v else [])
 elif isinstance(v,dict):print(k,'DICT',list(v)[:25])
 else:print(k,str(v)[:500])

