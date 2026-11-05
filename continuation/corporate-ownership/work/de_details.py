import requests,pathlib,json,datetime,hashlib,time,re
from bs4 import BeautifulSoup
root=pathlib.Path('continuation/corporate-ownership');sources=json.loads((root/'sources.json').read_text());url='https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx';session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
def fields(html):
 form=BeautifulSoup(html,'html.parser').find('form',id='aspnetForm');return {i.get('name'):i.get('value','') for i in form.find_all('input') if i.get('name') and i.get('type')=='hidden'}
def save(r,id,query,phase):
 at=datetime.datetime.now(datetime.timezone.utc).isoformat();path=root/'evidence'/f'{id}.html';path.write_bytes(r.content);rec=dict(document_id=id,url=url,method='POST',search_name=query,retrieval_phase=phase,retrieved_at_utc=at,http_status=r.status_code,bytes=len(r.content),file=str(path).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),final_url=r.url);sources.append(rec);return BeautifulSoup(r.text,'html.parser')
for idx,name in enumerate(['"ENTRYPOINT GP LLC"','"ENTRYPOINT PARTNERS, LP"','"EP FUND GP, LLC"','"FINCH LLC"','"NAYS, LLC"']):
 try:
  r=session.get(url,timeout=30);data=fields(r.text);data.update({'ctl00$ContentPlaceHolder1$frmEntityName':name,'ctl00$ContentPlaceHolder1$frmFileNumber':'','ctl00$ContentPlaceHolder1$btnSubmit':'Search','email_confirm':''});r=session.post(url,data=data,timeout=35);soup=save(r,f'CORP2-DE-EXACT-{idx}',name,'quoted exact-name result');links=[a for a in soup.find_all('a') if 'lnkbtnEntityName' in a.get('href','')];print('QUERY',name,'MATCHES',[(a.get_text(' ',strip=True),a.parent.parent.get_text(' ',strip=True)) for a in links])
  for k,a in enumerate(links[:3]):
   target=re.search(r"__doPostBack\('([^']+)'",a['href'])[1];data=fields(r.text);data.update({'__EVENTTARGET':target,'__EVENTARGUMENT':'','ctl00$ContentPlaceHolder1$frmEntityName':name,'ctl00$ContentPlaceHolder1$frmFileNumber':'','email_confirm':''});rr=session.post(url,data=data,timeout=35);ss=save(rr,f'CORP2-DE-DETAIL-{idx}-{k}',name,'entity detail selected from matching result');tx=ss.get_text(' ',strip=True);print('DETAIL',name,rr.status_code,rr.url,'\n',tx[-7000:])
   if 'captcha' in tx.lower():print('CHALLENGE stop detail');break
 except Exception as e:sources.append(dict(document_id=f'CORP2-DE-EXACT-{idx}',url=url,search_name=name,error=str(e),retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print(name,str(e))
 time.sleep(.6)
(root/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf8')
