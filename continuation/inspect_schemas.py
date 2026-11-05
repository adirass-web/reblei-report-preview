import pathlib,json
for branch in ['early-employment','corporate-ownership']:
 for name in ['sources.json','claims.json','search-log.json','report.md']:
  p=pathlib.Path('continuation')/branch/name
  print(branch,name,p.exists(),p.stat().st_size if p.exists() else 0)
  if p.exists() and name!='report.md':
   d=json.loads(p.read_text(encoding='utf-8-sig'));print(type(d).__name__,len(d));
   if isinstance(d,dict):print('topkeys',list(d))
   r=d if isinstance(d,list) else d.get('sources',d.get('documents',d.get('claims',d.get('search_logs',[]))))
   if r:print(json.dumps(r[0],ensure_ascii=True)[:2800])
