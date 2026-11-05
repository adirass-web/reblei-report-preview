import requests,pathlib,json,hashlib,datetime
p=pathlib.Path('outputs/evidence');rows=[]
q="upper(current_entity_name) like '%MEB NY%' OR upper(current_entity_name) in ('FINCH LLC','FINCH, LLC','NAYS LLC','NAYS, LLC','SCOUT TRADING, LLC','SCOUT TRADING LLC','OPHIR PARTNERS, LLC','OPHIR PARTNERS LLC','ENTRYPOINT CAPITAL, LLC','ENTRYPOINT CAPITAL LLC','ENTRYPOINT PARTNERS, LP','ENTRYPOINT PARTNERS LP','ENTRYPOINT GP LLC','EP FUND GP LLC','INFERENT CAPITAL, LLC','INFERENT CAPITAL LLC')"
url='https://data.ny.gov/resource/7xex-7g3w.json';params={'$select':'dos_id,current_entity_name,initial_dos_filing_date,jurisdiction,entity_type','$where':q,'$limit':100}
t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(url,params=params,timeout=30);row={'filename':'parent-ny-entity-name-candidates.json','url':r.url,'retrieved_at_utc':t,'http_status':r.status_code,'note':'Name-only candidate records from official open dataset; no ownership linkage or current legal status established. Selected fields omit addresses.'}
if r.ok:
 (p/row['filename']).write_bytes(r.content);row['sha256']=hashlib.sha256(r.content).hexdigest();print(r.text)
else:print(r.status_code,r.text[:400])
f=pathlib.Path('outputs/parent-sources.json');a=json.loads(f.read_text());a.append(row);f.write_text(json.dumps(a,indent=2),encoding='utf8')
