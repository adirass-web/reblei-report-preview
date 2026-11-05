from pathlib import Path
import requests,json,hashlib,datetime
from bs4 import BeautifulSoup
r=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records\continuation-4\entrypoint-history')
urls=[('adv-catalogue','https://www.sec.gov/foia-services/frequently-requested-documents/form-adv-data'),('adv-instructions2016','https://www.sec.gov/files/rules/final/2016/ia-4509-appendix-a.pdf')]
rows=[]
for ident,url in urls:
 at=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  res=requests.get(url,headers={'User-Agent':'Financial public record research/1.0'},timeout=30);p=r/'raw'/(ident+('.pdf' if res.content.startswith(b'%PDF') else '.html'));p.write_bytes(res.content)
  rows.append(dict(source_id='EP5-'+ident,url=url,file=p.relative_to(r.parent.parent).as_posix(),http_status=res.status_code,sha256=hashlib.sha256(res.content).hexdigest(),retrieved_at_utc=at,source_class='official_original' if res.status_code==200 else 'official_access_error'))
  print(ident,res.status_code,len(res.content))
  if ident=='adv-catalogue' and res.status_code==200:
   soup=BeautifulSoup(res.content,'html.parser');print([(a.get_text(' ',strip=True),a.get('href')) for a in soup.select('a[href]') if any(q in a.get('href','').lower() for q in ['era','part1','part-1','zip','adv-w'])])
  if p.suffix=='.pdf':
   import fitz
   d=fitz.open(p);rows[-1]['pdf_pages']=len(d)
   for i,pg in enumerate(d):
    t=' '.join(pg.get_text().split())
    if 'final report' in t.lower() and ('initial application' in t.lower() or 'applying for' in t.lower()): print('PAGE',i+1,t)
 except Exception as e:rows.append(dict(source_id='EP5-'+ident,url=url,retrieved_at_utc=at,error=str(e)));print(type(e).__name__)
(r/'direct-sources.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
