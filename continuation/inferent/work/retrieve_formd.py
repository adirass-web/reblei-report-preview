import requests,json,pathlib,hashlib,datetime,fitz
root=pathlib.Path('continuation/inferent'); records=json.loads((root/'sources.json').read_text(encoding='utf-8'))
u='https://www.sec.gov/Archives/edgar/data/1750250/000175025018000002/0001750250-18-000002.txt'
t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(u,headers={'User-Agent':'Public-record due-diligence research (noncommercial)'},timeout=40)
rec={'document_id':'INF-D-1750250-20180817','url':u,'retrieved_at_utc':t,'http_status':r.status_code,'source_class':'official_filing_or_record','accession_id':'0001750250-18-000002','filing_date':'2018-08-17'}
if r.ok:
 p=root/'raw'/'inferent-qe-fund-2018-formd.txt';p.write_bytes(r.content);rec.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest());print('saved D',len(r.content),'Bleich',('bleich' in r.text.lower()));print(r.text[1500:5400])
records.append(rec)
(root/'sources.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
for n in ['parallel-discovery-01.json','parallel-brochure-549848.json','parallel-discovery-02.json']:
 obj=json.loads((root/'raw'/n).read_text(encoding='utf-8-sig'));print('valid JSON',n)
