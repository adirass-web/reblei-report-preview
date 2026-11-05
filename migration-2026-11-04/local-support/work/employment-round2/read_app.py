import requests,json,pathlib,hashlib,datetime
from bs4 import BeautifulSoup
p=pathlib.Path('work/employment-round2')
r=requests.get('https://brokercheck.finra.org',timeout=30)
(p/'brokercheck-app.html').write_bytes(r.content)
s=BeautifulSoup(r.content,'html.parser')
print(r.status_code)
print([a.get('src') for a in s.find_all('script',src=True)])
