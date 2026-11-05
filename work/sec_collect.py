import requests, pathlib, hashlib, datetime, json, fitz, time
base=pathlib.Path('outputs/evidence')
targets=[('ADV-313946','https://reports.adviserinfo.sec.gov/reports/ADV/313946/PDF/313946.pdf','sec-313946-adv.pdf'),('BROCHURE-1061309','https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=1061309','sec-brochure-1061309.pdf')]
for cik,acc in [(2016250,'000201625026000001'),(2016251,'000201625126000001'),(1555295,'000155529512000002')]:
 targets.append((f'D-{cik}-{acc}',f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/primary_doc.xml',f'sec-{cik}-{acc}.xml'))
for cik in [1992519,2016250,2016251,1555295]:
 targets.append((f'SUBMISSIONS-{cik}',f'https://data.sec.gov/submissions/CIK{cik:010d}.json',f'sec-submissions-{cik}.json'))
meta=[]
s=requests.Session();s.headers['User-Agent']='Public financial-regulatory research; original records preservation'
for id,url,name in targets:
 try:
  r=s.get(url,timeout=40); at=datetime.datetime.now(datetime.timezone.utc).isoformat(); raw=r.content
  rec=dict(document_id=id,url=url,final_url=r.url,retrieved_at_utc=at,status_code=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(raw),file='outputs/evidence/'+name,sha256=hashlib.sha256(raw).hexdigest())
  if r.status_code==200:
   (base/name).write_bytes(raw)
   if raw.startswith(b'%PDF'):
    d=fitz.open(stream=raw,filetype='pdf');rec['pdf_pages']=len(d)
    (base/(name+'.txt')).write_text('\n'.join(f'\n--- PHYSICAL PDF PAGE {i+1} ---\n'+p.get_text() for i,p in enumerate(d)),encoding='utf8')
  else:rec['file']=None;rec['sha256']=None
  meta.append(rec);print(id,r.status_code,len(raw),rec.get('pdf_pages',''))
 except Exception as e:meta.append(dict(document_id=id,url=url,error=str(e)));print(id,str(e))
 time.sleep(0.4)
pathlib.Path('outputs/sec-sources.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
