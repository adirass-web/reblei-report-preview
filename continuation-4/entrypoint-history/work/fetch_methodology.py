from pathlib import Path
import requests,json,hashlib,datetime,fitz
r=Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-4/entrypoint-history');p=r/'direct-sources.json';rows=json.loads(p.read_text(encoding='utf-8'))
for ident,url in [('instructions2024','https://www.sec.gov/files/formadv-instructions.pdf'),('adv-faq','https://www.sec.gov/about/divisions-offices/division-investment-management/electronic-filing-investment-advisers-iard/frequently-asked-questions-form-adv-iard')]:
 at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  res=requests.get(url,headers={'User-Agent':'Financial public record research/1.0'},timeout=30);fp=r/'raw'/(ident+('.pdf' if res.content.startswith(b'%PDF') else '.html'));fp.write_bytes(res.content)
  row=dict(source_id='EP5-'+ident,url=url,file='continuation-4/entrypoint-history/raw/'+fp.name,http_status=res.status_code,sha256=hashlib.sha256(res.content).hexdigest(),retrieved_at_utc=at,source_class='official_original' if res.status_code==200 else 'official_access_error')
  if fp.suffix=='.pdf':
   d=fitz.open(fp);row['pdf_pages']=len(d)
   for i,pg in enumerate(d):
    text=' '.join(pg.get_text().split())
    if ('same filing' in text.lower() and 'final report' in text.lower()) or ('not required' in text.lower() and 'part 2b' in text.lower()):print('PAGE',i+1,text.encode('ascii','backslashreplace').decode()[:3000])
  rows.append(row);print(ident,res.status_code,len(res.content))
 except Exception as e:rows.append(dict(source_id='EP5-'+ident,url=url,retrieved_at_utc=at,error=str(e)));print(ident,type(e).__name__)
p.write_text(json.dumps(rows,indent=2),encoding='utf-8')
