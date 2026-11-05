from bs4 import BeautifulSoup
from pathlib import Path
p=Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/inferent/raw/part2-archive.html')
s=BeautifulSoup(p.read_bytes(),'html.parser')
for a in s.find_all('a',href=True):
 if any(x in a.get_text(' ',strip=True)+' '+a['href'] for x in ['2015','2016','2017','Mapping','mapping']):print(a.get_text(' ',strip=True),a['href'])
