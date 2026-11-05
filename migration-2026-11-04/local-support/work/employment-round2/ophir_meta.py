import json,pathlib
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records')
for p in [root/'continuation-3/inferent/base-a-verification.json',root/'continuation-3/employment/raw/EMP4-SCHEDULE-AB-verification.json']:
 d=json.loads(p.read_text());print(p.name,{k:v for k,v in d.items() if k!='requests'})
