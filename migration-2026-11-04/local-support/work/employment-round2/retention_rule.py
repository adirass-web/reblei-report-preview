from bs4 import BeautifulSoup
from pathlib import Path
p=Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/employment/raw/EMP3-FINRA-ABOUT.html')
s=BeautifulSoup(p.read_bytes(),'html.parser').get_text(' ',strip=True)
i=s.find('Individuals Whose Registrations Ended More than 10 Years Ago')
print(s[i:i+5000])
