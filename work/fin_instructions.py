import requests,pathlib,hashlib,datetime,json,fitz
p=pathlib.Path('outputs/financial-sources.json');meta=json.loads(p.read_text());s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
for name,url in [('fin-form13f-instructions.pdf','https://www.sec.gov/files/form13f.pdf'),('fin-form13f-faq.html','https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f')]:
 r=s.get(url,timeout=30);rec=dict(document_id='FIN-13F-INSTRUCTIONS' if name.endswith('.pdf') else 'FIN-13F-FAQ',url=url,final_url=r.url,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status_code=r.status_code,content_type=r.headers.get('Content-Type'),bytes=len(r.content),file=None,sha256=None)
 if r.status_code==200:
  path=pathlib.Path('outputs/evidence')/name;path.write_bytes(r.content);rec.update(file=str(path).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest())
  if r.content.startswith(b'%PDF'):
   d=fitz.open(stream=r.content,filetype='pdf');rec['pdf_pages']=len(d);pathlib.Path(str(path)+'.txt').write_text('\n'.join(f'PHYSICAL PDF PAGE{i+1}\n'+pg.get_text() for i,pg in enumerate(d)),encoding='utf8')
 meta.append(rec);print(name,r.status_code,len(r.content))
p.write_text(json.dumps(meta,indent=2),encoding='utf8')
