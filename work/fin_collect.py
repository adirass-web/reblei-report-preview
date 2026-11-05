import requests,pathlib,hashlib,datetime,json,time
base=pathlib.Path('outputs/evidence');meta=[];s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
j=json.loads((base/'sec-submissions-1992519.json').read_text());f=j['filings']['recent']
for i,acc in enumerate(f['accessionNumber']):
 nodash=acc.replace('-','');existing=base/f'sec-1992519-{nodash}-{acc}.txt'
 if existing.exists():continue
 name=f'fin-1992519-{acc}.txt';url=f'https://www.sec.gov/Archives/edgar/data/1992519/{nodash}/{acc}.txt'
 try:
  r=s.get(url,timeout=35);rec=dict(document_id=f'FIN-SUB-{acc}',url=url,final_url=r.url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status_code=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(r.content),file=None,sha256=None,accession_id=acc,filing_date=f['filingDate'][i],report_date=f['reportDate'][i],form=f['form'][i],claim_links=[])
  if r.status_code==200:
   (base/name).write_bytes(r.content);rec.update(file='outputs/evidence/'+name,sha256=hashlib.sha256(r.content).hexdigest(),preserved_format='original complete SEC submission text/SGML with embedded XML',source_class='official filing')
  meta.append(rec);print(acc,r.status_code,len(r.content))
 except Exception as e:meta.append(dict(document_id=f'FIN-SUB-{acc}',url=url,error=str(e),accession_id=acc));print(acc,str(e))
 time.sleep(.3)
pathlib.Path('outputs/financial-sources.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
