import requests,pathlib,json,hashlib,datetime,fitz
root=pathlib.Path('continuation-2/litigation');src=json.loads((root/'sources.json').read_text(encoding='utf-8'));u='https://www.finra.org/sites/default/files/aao_documents/15-02816.pdf';t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(u,timeout=35);x={'document_id':'LIT3-AWARD-1502816','url':u,'retrieved_at_utc':t,'http_status':r.status_code,'source_class':'official_finra_arbitration_award','case_number':'15-02816','filing_date':'2016-11-18'}
if r.ok and r.content.startswith(b'%PDF'):
 p=root/'raw'/'finra-award-15-02816.pdf';p.write_bytes(r.content);d=fitz.open(p);x.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),pdf_pages=len(d));txt='\n'.join('PHYSICAL PAGE '+str(i+1)+'\n'+page.get_text() for i,page in enumerate(d));(root/'work/finra-award-15-02816.txt').write_text(txt,encoding='utf-8');print(txt)
else:x['error']='Original PDF unavailable'
src.append(x);(root/'sources.json').write_text(json.dumps(src,indent=2),encoding='utf-8')
