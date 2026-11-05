import json,pathlib
p=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-3/inferent/part1bulk-directory.json');d=json.loads(p.read_text())
for e in d['entries']:
 if 'Schedule_A' in e['member'] or 'Schedule_B' in e['member']:print(d['url'],e)
