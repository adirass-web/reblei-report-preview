import json,pathlib
p=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/inferent/sources.json')
a=json.loads(p.read_text())
print(type(a));
for x in a:
 if 'mapping' in str(x).lower() or 'part2-archive' in str(x):print(json.dumps(x))
