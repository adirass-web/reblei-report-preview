import requests,hashlib,json,datetime,pathlib,fitz
base=pathlib.Path('outputs/evidence')
items=[('lead-cboe-lehman-20060919.pdf','https://cdn.cboe.com/resources/press_releases/Lehman%20Brothers%20Acquires%20Stake%20in%20BATS%20Electronic%20Communications%20Network.pdf','corporate_release_exchange_hosted'),('lead-inferent-292027-adv.pdf','https://reports.adviserinfo.sec.gov/reports/ADV/292027/PDF/292027.pdf','official_filing')]
rows=[]
for name,url,category in items:
 t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=requests.get(url,timeout=35)
  row=dict(filename=name,url=url,retrieved_at_utc=t,http_status=r.status_code,source_category=category)
  if r.ok and r.content.startswith(b'%PDF'):
   (base/name).write_bytes(r.content);row['sha256']=hashlib.sha256(r.content).hexdigest();doc=fitz.open(stream=r.content,filetype='pdf');row['pages']=len(doc)
   text='\n'.join(f'\n=== PHYSICAL PDF PAGE {i+1} ===\n'+p.get_text() for i,p in enumerate(doc));(base/(name+'.txt')).write_text(text,encoding='utf8')
   print(name,row['pages'],row['sha256'])
   for i,p in enumerate(doc):
    s=p.get_text()
    if any(x in s.lower() for x in ['bleich','date:','march','june','2020']):print('PAGE',i+1,s[:1800] if 'bleich' not in s.lower() else s)
  else:print(name,'HTTP',r.status_code)
  rows.append(row)
 except Exception as e:rows.append(dict(filename=name,url=url,retrieved_at_utc=t,error=str(e)));print(str(e))
pathlib.Path('outputs/parent-sources.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
