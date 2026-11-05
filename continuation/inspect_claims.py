import json,pathlib
for branch in ['early-employment','corporate-ownership','investment-litigation']:
 print(branch)
 d=json.loads((pathlib.Path('continuation')/branch/'claims.json').read_text(encoding='utf-8-sig'))
 for x in d if isinstance(d,list) else d['claims']:
  print(json.dumps({k:v for k,v in x.items() if k in ['claim_id','id','statement','claim','source_ids','source_id','document_id','evidence','locators','case_number']},ensure_ascii=True))
