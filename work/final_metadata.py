from pathlib import Path
import json
p=Path('outputs/parent-sources.json');j=json.loads(p.read_text())
for x in j:
 f=x.get('filename','')
 if 'brochure-1031410' in f:x.update(title='EntryPoint Capital FormADV Part2A March2026 brochure version1031410',document_period='2026-03',document_type='FormADV Part2A',filing_date=None)
 if 'brochure-956158' in f:x.update(title='EntryPoint Capital FormADV Part2A March2025 brochure version956158',document_period='2025-03',document_type='FormADV Part2A',filing_date=None)
 if 'inferent-292027' in f:x.update(title='Inferent Capital FormADV annual amendment March6 2019',document_type='FormADV',filing_date='2019-03-06')
 if 'cboe-lehman' in f:x.update(title='Lehman corporate release September19 2006, Cboe-hosted; lead only',document_type='corporate release',document_period='2006-09-19')
p.write_text(json.dumps(j,indent=2),encoding='utf8')
p=Path('work/build_index.py');s=p.read_text(encoding='utf8');s=s.replace("x.get('title') or x.get('document_type')","x.get('title') or x.get('document_type')")
s=s.replace("('financial',read('financial-search-log.json',[]))]:","('financial',read('financial-search-log.json',[])),('parent',read('parent-search-log.json',[]))]:")
p.write_text(s,encoding='utf8')
