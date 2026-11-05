import requests,pathlib,json,datetime,hashlib,time
from bs4 import BeautifulSoup
root=pathlib.Path('continuation/corporate-ownership');sources=json.loads((root/'sources.json').read_text());url='https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx';session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
for idx,name in enumerate(['ENTRYPOINT GP LLC','EP FUND GP LLC','ENTRYPOINT PARTNERS LP','FINCH LLC','NAYS LLC']):
 try:
  r=session.get(url,timeout=30);soup=BeautifulSoup(r.text,'html.parser');form=soup.find('form',id='aspnetForm');data={i.get('name'):i.get('value','') for i in form.find_all('input') if i.get('name') and i.get('type')=='hidden'};data.update({'ctl00$ContentPlaceHolder1$frmEntityName':name,'ctl00$ContentPlaceHolder1$frmFileNumber':'','ctl00$ContentPlaceHolder1$btnSubmit':'Search','email_confirm':''});r=session.post(url,data=data,timeout=35)
  at=datetime.datetime.now(datetime.timezone.utc).isoformat();path=root/'evidence'/f'de-search-result-{idx}.html';path.write_bytes(r.content);text=BeautifulSoup(r.text,'html.parser').get_text(' ',strip=True);record=dict(document_id=f'CORP2-DE-QUERY-{idx}',url=url,method='POST',search_name=name,retrieved_at_utc=at,http_status=r.status_code,bytes=len(r.content),file=str(path).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),final_url=r.url)
  record['access_limitation']='CAPTCHA or challenge present' if ('captcha' in text.lower() or 'verify you are' in text.lower()) else None;sources.append(record);print(name,r.status_code,r.url,'\n',text[-9000:]);
  if record['access_limitation']:break
 except Exception as e:sources.append(dict(document_id=f'CORP2-DE-QUERY-{idx}',url=url,search_name=name,error=str(e),retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print(name,str(e))
 time.sleep(.5)
(root/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf8')
