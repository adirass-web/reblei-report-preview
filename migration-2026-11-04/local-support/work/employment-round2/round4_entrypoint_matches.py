import pathlib,json
b=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-4/employment-inferent');a=json.loads((b/'raw/exact-ownerid-4262671-all-ia-schedule-ab.json').read_text())
for r in a:
 if r['FilingID']=='1869875':print(json.dumps(r))
