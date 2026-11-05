import pathlib,json
p=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/employment/search-log.json')
a=json.loads(p.read_text());q=[["4262671 Bleich registration history","Michael Edward Bleich Chase employment","Michael Bleich Lehman Barclays dates"],["site:sec.gov Michael Edward Bleich","site:sec.gov Michael Bleich Chase","site:gov Bleich Lehman employment"],["Michael Bleich brochure supplement employment","Michael Bleich Chase 1998 Lehman","4262671 adviserinfo employment history"],["FINRA BrokerCheck individual API history","SEC IAPD individual bulk archives","FINRA historical broker registration records"],["Michael Bleich Lehman site:gov","Michael Bleich Barclays site:finra.org","Michael Bleich Chase site:sec.gov","Michael Bleich employment court exhibit"],["Michael Bleich Lehman deposition","Bleich Barclays employee exhibit court","Michael Edward Bleich employment exhibit"],["Michael Bleich Chase Manhattan 1998","Michael Bleich risk management 2000","Michael Bleich Lehman joined 2000"]]
for i in range(7):a[i]['search_queries']=q[i]
p.write_text(json.dumps(a,indent=2),encoding='utf-8')

