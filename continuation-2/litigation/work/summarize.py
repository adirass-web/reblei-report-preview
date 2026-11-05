import json,pathlib
root=pathlib.Path('continuation-2/litigation');a=json.loads((root/'sources.json').read_text(encoding='utf-8'))
for r in a:print(r['document_id'],r.get('http_status'),r.get('error'),r.get('query'),r.get('result_count_text'),r.get('empty_messages'))
