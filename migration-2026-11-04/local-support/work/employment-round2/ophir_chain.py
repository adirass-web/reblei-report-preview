import json,pathlib
b=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-3/employment/raw');r=json.loads((b/'ophir-schedule-ab-selected.json').read_text())
for fid in ['663868','884710','993846','1019291','1070803']:
 print('\nFILING',fid)
 for x in r:
  if x['FilingID']==fid:print({k:v for k,v in x.items() if k not in ['csv_record_ordinal','FilingID','SchA-3','PR']})
