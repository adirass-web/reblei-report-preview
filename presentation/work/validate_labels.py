"""Verify reviewed label coverage and unchanged machine values in the reader."""
from pathlib import Path
import json,sys
sys.dont_write_bytecode=True
from bs4 import BeautifulSoup
from build_front import ROOT,OUT,TABLES,anchor,LABEL_ROWS,STATUS_LABELS
soup=BeautifulSoup((OUT/'claims.html').read_text(encoding='utf-8'),'html.parser')
options={o['value']:o.get_text() for o in soup.select('[data-filter="evidence-status"] option') if o['value']}
assert set(options)==set(LABEL_ROWS)
for c in TABLES['claims']:
 row=soup.find(id=anchor('c',c['claim_id']));status=c['evidence_status']
 assert json.loads(row['data-evidence-status'])==[status]
 assert status in row.get_text()
 if status in STATUS_LABELS:
  assert row.select_one('.status-label').get_text()== 'In plain English: '+STATUS_LABELS[status]
  assert options[status]==STATUS_LABELS[status]
 else:
  assert row.select_one('.status-label') is None
  assert options[status]==status
result={'statuses':len(LABEL_ROWS),'claims':len(TABLES['claims']),'applied':len(STATUS_LABELS),'exceptions':len(LABEL_ROWS)-len(STATUS_LABELS),'original_status_values_unchanged':True}
(OUT/'review/status-label-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
