import requests,pathlib,json,hashlib,datetime,re,time
from bs4 import BeautifulSoup
root=pathlib.Path('continuation-2/litigation');src=json.loads((root/'sources.json').read_text(encoding='utf-8'));logs=[]
queries=['Michael Bleich','Michael Edward Bleich','Scout Trading','Ophir Partners','EntryPoint Capital','EP Third Moment','Inferent Capital']
s=requests.Session()
for n,q in enumerate(queries,1):
 url='https://www.finra.org/arbitration-mediation/arbitration-awards-online';t=datetime.datetime.now(datetime.timezone.utc).isoformat();rec={'document_id':'LIT3-AAO-'+str(n).zfill(2),'url':url,'query':q,'retrieved_at_utc':t,'source_class':'official_native_database_search_response_not_clearance'}
 try:
  r=s.get(url,params={'aao_radios':'all','search':q},timeout=35);rec.update(url=r.url,http_status=r.status_code)
  p=root/'raw'/(rec['document_id']+'.html');p.write_bytes(r.content);rec.update(file=str(p).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest(),bytes=len(r.content))
  soup=BeautifulSoup(r.content,'html.parser');field=soup.select_one('input[name="search"]');rec['echoed_query']=field.get('value') if field else None
  main=soup.select_one('main') or soup;body=main.get_text(' ',strip=True); match=re.search(r'Displaying\s+\d+\s*[-\u2013]\s*\d+\s+of\s+[\d,]+',body);rec['result_count_text']=match.group(0) if match else None
  empties=[x.get_text(' ',strip=True) for x in soup.select('.view-empty')];rec['empty_messages']=empties
  rows=[x.get_text(' ',strip=True) for x in soup.select('table tbody tr')];rec['displayed_rows']=rows
  links=[{'text':a.get_text(' ',strip=True),'href':a.get('href')} for a in main.select('a[href]') if 'Arbitration' in str(a.get('href')) or 'award' in str(a.get('href')).lower() or re.fullmatch(r'\d{2}-\d{4,6}',a.get_text(strip=True))];rec['award_links']=links
  print(json.dumps({k:rec.get(k) for k in ['document_id','http_status','query','echoed_query','result_count_text','empty_messages','displayed_rows','award_links']}))
 except Exception as e:rec['error']=str(e);print(q,'ERROR',str(e))
 src.append(rec);logs.append({'search_id':rec['document_id'],'source_system':'FINRA Arbitration Awards Online native GET form','query':q,'url':rec['url'],'searched_at_utc':t,'result':{k:rec.get(k) for k in ['http_status','echoed_query','result_count_text','empty_messages','displayed_rows','error']},'coverage_limit':'PublicAAOreturnedresponseonly; no sealed/private/unfiled/arbitrationorcompletecourtclearance.'})
 time.sleep(.2)
(root/'sources.json').write_text(json.dumps(src,indent=2),encoding='utf-8');(root/'search-log.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
