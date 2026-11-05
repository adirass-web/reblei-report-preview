import json,pathlib
for b in ['inferent','employment','ownership']:
 print('\n'+b)
 for x in json.loads((pathlib.Path('continuation-2')/b/'claims.json').read_text(encoding='utf-8-sig')):print(x['claim_id'],x['statement'])
p=pathlib.Path('continuation-2/litigation/search-log.json');logs=json.loads(p.read_text(encoding='utf-8'));q={
'parallel-access-discovery.json':['NYSCEF guest party search official','New Jersey civil case jacket public','FINRA arbitration awards online search'],
'parallel-award-followup.json':['Scout Wedbush 15-02816 court','Scout Trading Wedbush 237594','Scout Wedbush arbitration November 2016'],
'parallel-clearing-corroboration.json':['site:finra.org Wedbush Scout 675000','site:nasdaq.com Wedbush Scout March 2016','site:finra.org Scout Trading clearing']}
for x in logs:
 if x.get('query') in q:x['queries']=q[x['query']]
p.write_text(json.dumps(logs,indent=2),encoding='utf-8')
