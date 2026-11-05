from bs4 import BeautifulSoup
from pathlib import Path
s=BeautifulSoup(Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/inferent/raw/part2-archive.html').read_bytes(),'html.parser')
for a in s.find_all('a',href=True):
 if any(x in a['href'].lower() for x in ['csv','mapping','map','201501','201601','201701']):print(a.get_text(' ',strip=True),a['href'])
