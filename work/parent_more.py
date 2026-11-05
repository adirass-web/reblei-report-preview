import requests,fitz,pathlib,json,hashlib,datetime
p=pathlib.Path('outputs/evidence'); out=[]
for name,url in [('parent-scout-audit-2013.pdf','https://www.sec.gov/Archives/edgar/vprr/1404/14048639.pdf'),('parent-ny-corporations-metadata.json','https://data.ny.gov/api/views/7xex-7g3w.json')]:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(url,timeout=30);row={'filename':name,'url':url,'retrieved_at_utc':t,'http_status':r.status_code}
  if r.ok:
   (p/name).write_bytes(r.content);row['sha256']=hashlib.sha256(r.content).hexdigest()
   if name.endswith('.pdf') and r.content.startswith(b'%PDF'):
    d=fitz.open(stream=r.content,filetype='pdf');row['pages']=len(d);(p/(name+'.txt')).write_text('\n'.join('\n=== PHYSICAL PDF PAGE '+str(i+1)+' ===\n'+x.get_text() for i,x in enumerate(d)),encoding='utf8');print(name,len(d),'pages');print('\n'.join(x.get_text() for x in d)[:1600])
   elif name.endswith('.json'):
    j=r.json();print(j.get('name'));print([(x['fieldName'],x['name']) for x in j.get('columns',[]) if not x['fieldName'].startswith(':')])
  else: print(name,r.status_code)
  out.append(row)
 except Exception as e:out.append({'filename':name,'url':url,'retrieved_at_utc':t,'error':str(e)})
f=pathlib.Path('outputs/parent-sources.json'); prior=json.loads(f.read_text());f.write_text(json.dumps(prior+out,indent=2),encoding='utf8')
