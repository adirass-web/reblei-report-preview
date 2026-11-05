import pathlib,json
src=json.loads(pathlib.Path('continuation-2/litigation/sources.json').read_text(encoding='utf-8'))
for x in src:
 if x['document_id']=='LIT3-AAO-PHRASE-04':print(json.dumps({k:x[k] for k in ['displayed_rows','award_links']},indent=2))
