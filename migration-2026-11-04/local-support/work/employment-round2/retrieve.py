import requests,json,hashlib,datetime,pathlib,concurrent.futures
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records')
base=root/'continuation-2/employment'
items=[('EMP3-FINRA-API','https://api.brokercheck.finra.org/search/individual/4262671','json','public_regulator_api'),('EMP3-SEC-DATA','https://www.sec.gov/foia-services/frequently-requested-documents/form-adv-data','html','official_government_data_catalog'),('EMP3-FINRA-ABOUT','https://www.finra.org/investors/investing/working-with-investment-professional/about-brokercheck','html','official_regulator_methodology'),('EMP3-FINRA-CATALOG','https://developer.finra.org/catalog','html','official_regulator_api_catalog')]
def get(t):
 i,u,ext,cl=t;p=base/'raw'/f'{i}.{ext}';tm=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(u,timeout=45);p.write_bytes(r.content)
  return dict(document_id=i,url=u,file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_at_utc=tm,source_class=cl,status='retrieved' if r.status_code==200 else 'access_failure',http_status=r.status_code,content_type=r.headers.get('content-type'),size_bytes=len(r.content))
 except Exception as e:return dict(document_id=i,url=u,status='request_failure',error=str(e),retrieved_at_utc=tm,source_class=cl)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:rs=list(ex.map(get,items))
(base/'sources.json').write_text(json.dumps(rs,indent=2),encoding='utf-8')
print(json.dumps(rs,indent=2))
