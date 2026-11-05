from pathlib import Path
import csv,json
r=Path('outputs/ReBlei/investigations/2026-11-04-official-records');o=r/'continuation-4/entrypoint-history';cache=Path('work/round4-era-cache')
with (cache/'ERA_ADV_Base_20111105_20241231.csv').open(encoding='latin-1',newline='') as f:
 reader=csv.DictReader(f);print('BASE KEYS',reader.fieldnames);rows=[dict(csv_record_ordinal=i+2,**x) for i,x in enumerate(reader) if x.get('1E1')=='313946']
(o/'entrypoint-era-base-selected.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');ids={x['FilingID'] for x in rows};print('ROWS',len(rows))
for x in rows: print(json.dumps({k:v for k,v in x.items() if v and not any(q in k.lower() for q in ['street','phone','fax','postal','address','zip','city','contact','email'])},ensure_ascii=True))
with (cache/'ERA_Schedule_A_B_20111105_20241231.csv').open(encoding='latin-1',newline='') as f:
 rd=csv.DictReader(f);print('AB KEYS',rd.fieldnames);ab=[dict(csv_record_ordinal=i+2,**x) for i,x in enumerate(rd) if x.get('FilingID') in ids]
(o/'entrypoint-era-ab-selected.json').write_text(json.dumps(ab,indent=2),encoding='utf-8')
for x in ab: print(json.dumps(x,ensure_ascii=True))
with (r/'continuation-3/inferent/raw/ADV_Filing_Types_20111105_20241231.csv').open(encoding='latin-1',newline='') as f:ft=[x for x in csv.DictReader(f) if x.get('FilingID') in ids]
(o/'entrypoint-era-filing-types.json').write_text(json.dumps(ft,indent=2),encoding='utf-8')
print('TYPES',json.dumps(ft))
