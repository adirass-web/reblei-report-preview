import requests,fitz,pathlib,json,datetime,hashlib
p=pathlib.Path('outputs/evidence');a=[]
for v in ['1031410','956158']:
 u='https://files.adviserinfo.sec.gov/IAPD/Content/Common/crd_iapd_Brochure.aspx?BRCHR_VRSN_ID='+v;t=datetime.datetime.now(datetime.timezone.utc).isoformat();r=requests.get(u,timeout=30);row={'filename':'parent-entrypoint-brochure-'+v+'.pdf','url':u,'retrieved_at_utc':t,'http_status':r.status_code,'source_category':'official_filing'}
 if r.ok and r.content.startswith(b'%PDF'):
  (p/row['filename']).write_bytes(r.content);row['sha256']=hashlib.sha256(r.content).hexdigest();d=fitz.open(stream=r.content,filetype='pdf');row['pages']=len(d);(p/(row['filename']+'.txt')).write_text('\n'.join('\n=== PHYSICAL PDF PAGE '+str(i+1)+' ===\n'+x.get_text() for i,x in enumerate(d)),encoding='utf8');print(v,len(d),'pages')
  for i,x in enumerate(d):
   s=x.get_text()
   if any(k in s.lower() for k in ['bleich','management fee','performance fee','indirectly owned']):print('PAGE',i+1,s[:6500])
 else:print(v,r.status_code)
 a.append(row)
f=pathlib.Path('outputs/parent-sources.json');j=json.loads(f.read_text());f.write_text(json.dumps(j+a,indent=2),encoding='utf8')
