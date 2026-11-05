import requests,pathlib,re
p=pathlib.Path('work/employment-round2')
r=requests.get('https://brokercheck.finra.org/main.2b8c58f556a565c0.js',timeout=30);(p/'brokercheck-main.js').write_bytes(r.content)
s=r.text
for needle in ['api.brokercheck','/search/individual','search/individual','individual/','hl=true']:
 print('\nNEEDLE',needle)
 for m in list(re.finditer(re.escape(needle),s))[:8]:print(s[max(0,m.start()-250):m.end()+400])
