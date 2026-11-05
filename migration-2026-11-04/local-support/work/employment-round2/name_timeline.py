import json,pathlib,datetime
b=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-3/employment/raw');r=json.loads((b/'ophir-schedule-ab-selected.json').read_text());h=json.loads((b/'ophir-filing-history-selected.json').read_text());h.sort(key=lambda x:datetime.datetime.strptime(x['DateSubmitted'],'%m/%d/%Y %I:%M:%S %p'))
for f in h:
 rows=[x for x in r if x['FilingID']==f['FilingID']];bleich=next(x for x in rows if x['Schedule']=='B' and x['OwnerID']=='4262671');meb=next(x for x in rows if x['Full Legal Name'].startswith('MEB'))
 print(f['FilingID'],f['DateSubmitted'],meb['Full Legal Name'],meb['Ownership Code'],bleich['Entity in Which'],'NAYS',any(x['Full Legal Name']=='NAYS LLC' for x in rows))
