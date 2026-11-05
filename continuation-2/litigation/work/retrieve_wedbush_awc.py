import requests,pathlib,json,hashlib,datetime,fitz
root=pathlib.Path('continuation-2/litigation');src=json.loads((root/'sources.json').read_text(encoding='utf-8'))
u='https://www.nasdaqtrader.com/content/marketregulation/NASDAQ/DisciplinaryActions/WEDB_NQ_2016.pdf';t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(u,timeout=40);x={'document_id':'LIT3-NASDAQ-WEDBUSH-AWC','url':u,'retrieved_at_utc':t,'http_status':r.status_code,'source_class':'official_regulatory_settlement_original','case_number':'20100243866-02'}
if r.ok and r.content.startswith(b'%PDF'):
 p=root/'raw'/'nasdaq-wedbush-20100243866-02.pdf';p.write_bytes(r.content);d=fitz.open(p);x.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),pdf_pages=len(d));txt='\n'.join('PHYSICAL PAGE '+str(i+1)+'\n'+pg.get_text() for i,pg in enumerate(d));(root/'work/nasdaq-wedbush-20100243866-02.txt').write_text(txt,encoding='utf-8');print('Pages',len(d));print(txt[:11000]);print(txt[-6500:])
else:x['error']='Original PDF unavailable'
src.append(x);(root/'sources.json').write_text(json.dumps(src,indent=2),encoding='utf-8')
