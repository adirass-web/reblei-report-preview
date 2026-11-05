from pathlib import Path
import sys,json,csv
r=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records');o=r/'continuation-4/entrypoint-history/raw';sys.path.insert(0,str(r/'continuation-3/inferent'));sys.dont_write_bytecode=True
from range_zip import member
items=json.loads((o/'advw-entries.json').read_text(encoding='utf-8'));url='https://www.sec.gov/files/advw-20001019-20241231.zip'
for i,item in enumerate(items):
 p,logs=member(url,item,o,'advw-'+str(i));(o/('advw-'+str(i)+'-verification.json')).write_text(json.dumps({'url':url,'member':item,'requests':logs,'crc32_verified':True,'uncompressed_size_verified':True,'file':p.name},indent=2),encoding='utf-8')
 with p.open(encoding='latin-1',newline='') as f:
  rd=csv.DictReader(f);print(p.name,'KEYS',rd.fieldnames)
  selected=[dict(csv_record_ordinal=j+2,**x) for j,x in enumerate(rd) if any(x.get(k) in ['313946','164729','292027'] for k in ['1D','CRDNumber','CRD','CRD Number','1D1','FirmCRD','Organization CRD#'])]
 (o/(p.stem+'-selected.json')).write_text(json.dumps(selected,indent=2),encoding='utf-8');print('SELECTED',len(selected),json.dumps(selected,ensure_ascii=True)[:2000])
