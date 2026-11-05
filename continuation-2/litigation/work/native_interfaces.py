import requests,pathlib,json,hashlib,datetime,re,concurrent.futures
from bs4 import BeautifulSoup
root=pathlib.Path('continuation-2/litigation');
items=[('LIT3-AAO-HOME','https://www.finra.org/arbitration-mediation/arbitration-awards-online'),('LIT3-NYSCEF-HOME','https://iapps.courts.state.ny.us/nyscef/CaseSearch?task=new'),('LIT3-NJ-ACCESS','https://www.njcourts.gov/public/find-a-case/civil-and-foreclosure-public-access')]
def run(item):
 ident,url=item;t=datetime.datetime.now(datetime.timezone.utc).isoformat();rec={'document_id':ident,'url':url,'retrieved_at_utc':t,'source_class':'official_database_interface_or_access_instructions_not_subject_case'}
 try:
  r=requests.get(url,timeout=40);rec.update(http_status=r.status_code,final_url=r.url)
  p=root/'raw'/(ident+'.html');p.write_bytes(r.content);rec.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content))
  soup=BeautifulSoup(r.content,'html.parser');forms=[]
  for f in soup.select('form'):
   forms.append({'action':f.get('action'),'method':f.get('method'),'fields':[{'tag':x.name,'name':x.get('name'),'type':x.get('type'),'value':x.get('value'),'id':x.get('id')} for x in f.select('input,select')]})
  print(ident,rec['http_status'],json.dumps(forms)[:17000]);
  if 'NYSCEF' in ident:print('links',[(a.get_text(' ',strip=True),a.get('href')) for a in soup.select('a[href]') if 'Name' in a.get_text() or 'name' in str(a.get('href'))])
 except Exception as e:rec['error']=str(e)
 return rec
recs=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(run,items));(root/'sources.json').write_text(json.dumps(recs,indent=2),encoding='utf-8')
