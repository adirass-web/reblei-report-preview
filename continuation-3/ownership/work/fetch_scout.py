import requests, pathlib, json, hashlib, datetime
root=pathlib.Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records\continuation-3\ownership')
items=[('scout-submissions','https://data.sec.gov/submissions/CIK0001474522.json',{}),('scout2013-annual','https://www.sec.gov/Archives/edgar/vprr/1404/14048639.pdf',{}),('scout2009-annual','https://www.sec.gov/Archives/edgar/vprr/1002/10027661.pdf',{})]
log=[]
for ident,url,extra in items:
 at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(url,headers={'User-Agent':'Financial public record research/1.0','Accept-Encoding':'gzip, deflate',**extra},timeout=35)
  suffix='.pdf' if r.content.startswith(b'%PDF') else '.json' if r.headers.get('content-type','').startswith('application/json') else '.response.txt'
  p=root/'raw'/(ident+suffix);p.write_bytes(r.content)
  row={'source_id':'CORP4-'+ident.upper(),'url':url,'retrieved_at_utc':at,'http_status':r.status_code,'file':'continuation-3/ownership/raw/'+p.name,'sha256':hashlib.sha256(r.content).hexdigest(),'bytes':len(r.content),'content_type':r.headers.get('content-type'),'response_headers':dict(r.headers),'source_class':'official_original' if r.status_code==200 else 'official_access_error_not_substantive_evidence'}
  if suffix=='.pdf':
   import fitz
   doc=fitz.open(p);row['pdf_pages']=len(doc)
   (root/'raw'/(ident+'-text.txt')).write_text('\n'.join('PHYSICAL PAGE '+str(i+1)+'\n'+page.get_text() for i,page in enumerate(doc)),encoding='utf-8')
  log.append(row)
  print(ident,r.status_code,len(r.content),suffix,flush=True)
 except Exception as e:
  log.append({'source_id':'CORP4-'+ident.upper(),'url':url,'retrieved_at_utc':at,'error':str(e)})
  print(ident,type(e).__name__,flush=True)
(root/'request-log.json').write_text(json.dumps(log,indent=2),encoding='utf-8')
