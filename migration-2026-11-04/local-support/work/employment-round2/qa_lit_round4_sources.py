import pathlib,json
p=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-4/investment-litigation');s=json.loads((p/'sources.json').read_text());print('SOURCEKEYS',list(s[0]));
for x in s:print(json.dumps({k:x.get(k) for k in ['document_id','url','file','sha256','retrieved_at_utc','http_status','source_class','status','physical_pages','locator']}))
log=json.loads((p/'search-log.json').read_text());print('LOG COUNT',len(log),'LOGKEYS',[list(x) for x in log[-3:]])
