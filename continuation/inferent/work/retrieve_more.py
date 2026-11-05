import requests,pathlib,json,hashlib,datetime,concurrent.futures
root=pathlib.Path('continuation/inferent');sources=json.loads((root/'sources.json').read_text(encoding='utf-8'))
items=[('INF-D-XML','https://www.sec.gov/Archives/edgar/data/1750250/000175025018000002/primary_doc.xml','inferent-qe-formd.xml'),('INF-D-RENDERED','https://www.sec.gov/Archives/edgar/data/1750250/000175025018000002/xslFormDX01/primary_doc.xml','inferent-qe-formd-rendered.html'),('INF-SUB-1769569','https://data.sec.gov/submissions/CIK0001769569.json','inferent-plenary-submissions.json')]
def run(item):
 ident,url,name=item; t=datetime.datetime.now(datetime.timezone.utc).isoformat();rec={'document_id':ident,'url':url,'retrieved_at_utc':t,'source_class':'official_filing_or_record'}
 try:
  r=requests.get(url,headers={'User-Agent':'Public-record due-diligence research (noncommercial)'},timeout=35);rec['http_status']=r.status_code
  if r.ok:
   p=root/'raw'/name;p.write_bytes(r.content);rec.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest()); print(ident,r.status_code,len(r.content),'Bleich text:',('bleich' in r.text.lower()))
  else:rec['error']='HTTP '+str(r.status_code); print(ident,rec['error'])
 except Exception as e:rec['error']=str(e)
 return rec
sources.extend(list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(run,items)))
(root/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
p=root/'raw'/'inferent-plenary-submissions.json'
if p.exists():
 d=json.loads(p.read_text(encoding='utf-8'));print(d['name'],d['filings']['recent'])
