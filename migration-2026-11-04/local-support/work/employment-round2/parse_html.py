from bs4 import BeautifulSoup
from pathlib import Path
base=Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/employment/raw')
for f in ['EMP3-FINRA-ABOUT.html','EMP3-FINRA-CATALOG.html']:
 s=BeautifulSoup((base/f).read_text(encoding='utf-8'),'html.parser')
 text=s.get_text(' ',strip=True)
 for needle in ['employment history for the last','Composite Individual','Individual Pre-Registration','public records','ten years','10 years']:
  start=text.find(needle)
  if start>=0: print(f,needle,text[max(start-150,0):start+1400])
 for a in s.find_all('a',href=True):
  if any(x in a.get_text().lower() for x in ['composite individual','pre-registration','faq']): print(a.get_text(),a['href'])
