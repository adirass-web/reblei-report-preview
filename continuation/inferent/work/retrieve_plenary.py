import requests,pathlib,json,hashlib,datetime
root=pathlib.Path('continuation/inferent'); src=json.loads((root/'sources.json').read_text(encoding='utf-8'))
u='https://www.sec.gov/Archives/edgar/data/1769569/000094562119000100/0000945621-19-000100.txt';t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(u,headers={'User-Agent':'Public-record due-diligence research (noncommercial)'},timeout=35)
a={'document_id':'INF-D-1769569-20190305','url':u,'retrieved_at_utc':t,'http_status':r.status_code,'source_class':'official_filing_or_record','filing_date':'2019-03-05','accession_id':'0000945621-19-000100'}
if r.ok:
 p=root/'raw'/'inferent-plenary-formd.txt';p.write_bytes(r.content);a.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest());print('Bleich:',('bleich' in r.text.lower()))
else:a['error']='HTTP '+str(r.status_code)
src.append(a);(root/'sources.json').write_text(json.dumps(src,indent=2),encoding='utf-8');print(a)
