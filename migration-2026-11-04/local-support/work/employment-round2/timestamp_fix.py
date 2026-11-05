import json,pathlib,datetime
base=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/employment');p=pathlib.Path('work/employment-round2/brokercheck-main.js');t=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()
for fn in ['sources.json','search-log.json']:
 data=json.loads((base/fn).read_text())
 for s in data:
  if s.get('document_id',s.get('log_id'))=='EMP3-FINRA-APP':s['retrieved_at_utc']=t;s['retrieval_time_precision']='filesystem save timestamp of original downloaded public JS; response completion time';
 (base/fn).write_text(json.dumps(data,indent=2),encoding='utf-8')
print(t)
