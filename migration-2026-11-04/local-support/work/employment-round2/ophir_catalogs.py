import requests,pathlib,datetime,hashlib,json
from bs4 import BeautifulSoup
base=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-3/employment');root=base.parents[1]
logs=[]
for i,u in enumerate(['https://www.sec.gov/foia/docs/form-adv-archive-data.htm','https://www.sec.gov/foia/form-adv-part-2-data-archive']):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(u,timeout=30);p=base/'raw'/('official-catalog-'+str(i)+'.html');p.write_bytes(r.content);logs.append(dict(document_id='EMP4-CATALOG'+str(i),url=u,file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_at_utc=t,status='retrieved' if r.status_code==200 else 'access_failure',source_class='official_government_catalog',http_status=r.status_code));print(r.status_code,u)
 if r.status_code==200:
  for a in BeautifulSoup(r.content,'html.parser').find_all('a',href=True):
   if any(x in a['href'].lower() for x in ['mapping','2015','2016','2017']):print(a.get_text(' ',strip=True),a['href'])
(base/'sources.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
