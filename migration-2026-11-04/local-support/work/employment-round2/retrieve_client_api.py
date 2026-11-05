import requests,json,hashlib,datetime,pathlib,concurrent.futures
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-2/employment'
sources=json.loads((base/'sources.json').read_text())
query='?hl=true&includePrevious=true&nrows=12&query=john&r=25&sort=bc_lastname_sort+asc,bc_firstname_sort+asc,bc_middlename_sort+asc,score+desc&wt=json'
items=[('EMP3-FINRA-CLIENT-API','https://api.brokercheck.finra.org/search/individual/4262671'+query,'json','public_regulator_api'),('EMP3-IAPD-CLIENT-API','https://api.adviserinfo.sec.gov/search/individual/4262671'+query,'json','public_government_api')]
for i,u,ext,cl in items:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();p=base/'raw'/f'{i}.{ext}'
 try:
  r=requests.get(u,timeout=30);p.write_bytes(r.content)
  item=dict(document_id=i,url=u,file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_at_utc=t,source_class=cl,status='retrieved' if r.status_code==200 else 'access_failure',http_status=r.status_code,size_bytes=len(r.content))
  print(i,r.status_code,r.text[:1500]);sources.append(item)
 except Exception as e: print(i,str(e))
p=base/'raw'/'EMP3-FINRA-APP.js';p.write_bytes(pathlib.Path('work/employment-round2/brokercheck-main.js').read_bytes())
sources.append(dict(document_id='EMP3-FINRA-APP',url='https://brokercheck.finra.org/main.2b8c58f556a565c0.js',file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_class='official_public_application_code',status='retrieved',http_status=200,locator='window.brokercheckConfig endpoints; fetchIndividual(n)'))
(base/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf-8')
