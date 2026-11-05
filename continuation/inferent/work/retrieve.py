import requests,pathlib,json,hashlib,datetime,fitz
root=pathlib.Path('continuation/inferent')
items=[('INF-BRO-549848','https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID=549848','inferent-brochure-549848.pdf'),('INF-SUB-1750250','https://data.sec.gov/submissions/CIK0001750250.json','inferent-qe-fund-submissions.json')]
records=[]
for ident,url,name in items:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(url,headers={'User-Agent':'Public-record due-diligence research (noncommercial)'},timeout=45)
 rec={'document_id':ident,'url':url,'retrieved_at_utc':t,'http_status':r.status_code,'source_class':'official_filing_or_record'}
 if r.ok:
  p=root/'raw'/name;p.write_bytes(r.content);rec.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content))
  if r.content.startswith(b'%PDF'):
   d=fitz.open(p);rec['pdf_pages']=len(d);s='\n'.join('PHYSICAL PAGE '+str(i+1)+'\n'+pg.get_text() for i,pg in enumerate(d));(root/'work'/(name+'.txt')).write_text(s,encoding='utf-8');print(s[:1600]);print('BLEICH MATCHES',[(i+1,pg.get_text()) for i,pg in enumerate(d) if 'bleich' in pg.get_text().lower()])
 records.append(rec);print(json.dumps(rec))
(root/'sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
