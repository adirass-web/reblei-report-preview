from pathlib import Path
import json
p=Path('continuation-2/ownership/report.md');s=p.read_text(encoding='utf-8-sig');s=s.replace('marked last updated December20,2024/effective January2025','headed 2025 Revision and marked Last Updated 20DEC2024');p.write_text(s,encoding='utf-8')
for branch in ['employment','inferent','ownership']:
 print('\nBRANCH',branch)
 for name in ['sources.json','claims.json','search-log.json']:
  d=json.loads((Path('continuation-2')/branch/name).read_text(encoding='utf-8-sig'));print(name,len(d),json.dumps(d[0],ensure_ascii=True)[:2100])
d=json.loads(Path('evidence-index.json').read_text(encoding='utf-8'))
print('EVENTS',json.dumps(d['tables']['events'],indent=2))
