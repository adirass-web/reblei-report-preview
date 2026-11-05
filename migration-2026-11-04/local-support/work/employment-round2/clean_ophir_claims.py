import pathlib,json
p=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-3/employment/claims.json');a=json.loads(p.read_text())
for c in a:
 c['statement']=c['statement'].replace('Part2','Part 2').replace('ten2017','ten 2017').replace('eight2016','eight 2016').replace('ten2015','ten 2015').replace('2015ZIPs','2015 ZIPs').replace('2016ZIPs','2016 ZIPs').replace('2017ZIPs','2017 ZIPs').replace('selected2015/2016ZIPs','selected 2015/2016 ZIPs').replace('returnedHTTP403','returned HTTP 403').replace('Untested2015/2016parts','Untested 2015/2016 parts').replace('Part2A/2B','Part 2A/2B').replace('latest-brochure-ID247246','the supplied latest-brochure-ID 247246 lead')
p.write_text(json.dumps(a,indent=2),encoding='utf-8')
