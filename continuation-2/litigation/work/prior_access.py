import pathlib,json
p=pathlib.Path('continuation/investment-litigation/sources.json');d=json.loads(p.read_text(encoding='utf-8-sig'))
for x in d['documents']:
 if x['document_id']=='LIT-D005':print(json.dumps(x,indent=2))
