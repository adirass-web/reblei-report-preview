import requests,re
u='https://hedgefunddb.com/Home/FundDetails/801-112741/INFERENT-CAPITAL--LLC'
r=requests.get(u,timeout=40)
print('status',r.status_code)
for x in re.findall(r'.{0,300}(?:Brochure|aspx|Bleich).{0,300}',r.text,re.I): print(x)
