import requests,pathlib,json,datetime,hashlib,re
root=pathlib.Path('continuation/corporate-ownership');sources=[]
s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
for name,url in [('ny-public-inquiry','https://apps.dos.ny.gov/publicInquiry/'),('de-search','https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx')]:
 try:
  r=s.get(url,timeout=35);at=datetime.datetime.now(datetime.timezone.utc).isoformat();rec=dict(document_id='CORP2-'+name,url=url,final_url=r.url,retrieved_at_utc=at,http_status=r.status_code,bytes=len(r.content),content_type=r.headers.get('Content-Type'),file=None,sha256=None)
  if r.status_code==200:
   path=root/'evidence'/f'{name}.html';path.write_bytes(r.content);rec.update(file=str(path).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest());print(name,'scripts',re.findall(r'<script[^>]+src=[\"\x27]([^\"\x27]+)',r.text));print('title',re.findall(r'<title>(.*?)</title>',r.text,re.S));print('forms',re.findall(r'<form[^>]*>',r.text)[:3])
  sources.append(rec);print(name,r.status_code,len(r.content))
 except Exception as e:sources.append(dict(document_id='CORP2-'+name,url=url,error=str(e),retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()));print(name,str(e))
(root/'sources.json').write_text(json.dumps(sources,indent=2),encoding='utf8')
