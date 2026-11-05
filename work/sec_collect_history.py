import requests,pathlib,hashlib,datetime,json,time,re,xml.etree.ElementTree as E
base=pathlib.Path('outputs/evidence');mp=pathlib.Path('outputs/sec-sources.json');meta=json.loads(mp.read_text()); s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
for cik in [2016250,2016251,1992519]:
 j=json.loads((base/f'sec-submissions-{cik}.json').read_text()); f=j['filings']['recent']; idx=range(len(f['accessionNumber'])) if cik!=1992519 else [0,1,2,len(f['accessionNumber'])-1]
 for i in idx:
  acc=f['accessionNumber'][i];nodash=acc.replace('-','');name=f'sec-{cik}-{nodash}-{acc}.txt';url=f'https://www.sec.gov/Archives/edgar/data/{cik}/{nodash}/{acc}.txt'
  if (base/name).exists():continue
  r=s.get(url,timeout=35);rec=dict(document_id=f'SUBMISSION-{acc}',url=url,final_url=r.url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status_code=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(r.content),file=None,sha256=None,accession_id=acc,filing_date=f['filingDate'][i],report_date=f['reportDate'][i],form=f['form'][i])
  if r.status_code==200:
   (base/name).write_bytes(r.content);rec.update(file='outputs/evidence/'+name,sha256=hashlib.sha256(r.content).hexdigest())
  meta.append(rec);print(acc,r.status_code,len(r.content));time.sleep(.3)
mp.write_text(json.dumps(meta,indent=2),encoding='utf8')
