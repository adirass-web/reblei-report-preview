import pathlib,json,csv,hashlib
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-3/employment';hist=json.loads((root/'continuation-3/inferent/target-filing-history.json').read_text());ophir=[x for x in hist if x['1E1']=='164729'];ids={x['FilingID'] for x in ophir};dates={x['FilingID']:x['DateSubmitted'] for x in ophir}
rows=[]
with pathlib.Path('work/employment-round2/schedule-cache/IA_Schedule_A_B_20111105_20241231.csv').open(encoding='latin-1',newline='') as f:
 for index,row in enumerate(csv.DictReader(f),start=1):
  if row['FilingID'] in ids:rows.append(dict(csv_record_ordinal=index,**row))
(base/'raw/ophir-schedule-ab-selected.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
selected=[{k:x[k] for k in ['FilingID','DateSubmitted','1A','1B1','1D','1E1','Signatory','Execution Date','Title']} for x in ophir]
(base/'raw/ophir-filing-history-selected.json').write_text(json.dumps(selected,indent=2),encoding='utf-8')
print('Target records',len(rows),'filings',len(ophir))
for row in rows:
 if 'BLEICH' in row['Full Legal Name'].upper():print(json.dumps(dict(submitted=dates[row['FilingID']],**row)))

