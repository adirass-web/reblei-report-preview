import requests,pathlib,hashlib,json,datetime
root=pathlib.Path('continuation/corporate-ownership');p=root/'sources.json';sources=json.loads(p.read_text());s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
urls=[('CORP2-SEC-CIK1977777','https://data.sec.gov/submissions/CIK0001977777.json'),('CORP2-NY-STATUS-METADATA','https://data.ny.gov/api/views/3gg2-jgnp.json'),('CORP2-NY-NAME-METADATA','https://data.ny.gov/api/views/ekwr-p59j.json')]
for id,url in urls:
 try:
  r=s.get(url,timeout=35);rec=dict(document_id=id,url=url,http_status=r.status_code,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),bytes=len(r.content),file=None,sha256=None)
  if r.status_code==200:
   f=root/'evidence'/f'{id}.json';f.write_bytes(r.content);rec.update(file=str(f).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest());j=r.json();print(id,'name',j.get('name'),'columns',[(c.get('fieldName'),c.get('name')) for c in j.get('columns',[]) if not c.get('fieldName','').startswith(':')]);
   if '1977777' in id:print('SECmetadata',j)
  sources.append(rec)
 except Exception as e:sources.append(dict(document_id=id,url=url,error=str(e),retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print(id,e)
p.write_text(json.dumps(sources,indent=2),encoding='utf8')
