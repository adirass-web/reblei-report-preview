import requests, pathlib, hashlib, datetime, json, time
base=pathlib.Path('outputs/evidence');meta=json.loads(pathlib.Path('outputs/sec-sources.json').read_text())
s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
for cik,acc in [(2016250,'000201625026000001'),(2016251,'000201625126000001'),(1555295,'000155529512000002')]:
 for host,filename in [('www.sec.gov','xslFormDX01/primary_doc.xml'),('www.sec.gov','primary_doc.html'),('www.sec.gov',acc[:10]+'-'+acc[10:12]+'-'+acc[12:]+'.txt')]:
  url=f'https://{host}/Archives/edgar/data/{cik}/{acc}/{filename}'
  r=s.get(url,timeout=35);name=f'sec-{cik}-{acc}-{filename.replace("/","-")}'
  rec=dict(document_id=f'D-{cik}-{acc}-{filename}',url=url,final_url=r.url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status_code=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(r.content),file=None,sha256=None)
  if r.status_code==200:
   (base/name).write_bytes(r.content);rec.update(file='outputs/evidence/'+name,sha256=hashlib.sha256(r.content).hexdigest())
  meta.append(rec);print(cik,filename,r.status_code,len(r.content));time.sleep(.3)
pathlib.Path('outputs/sec-sources.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
