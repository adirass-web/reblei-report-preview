import json,re,hashlib, pathlib,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1]
snapshot=json.loads((R/'source-snapshot.json').read_text(encoding='utf-8-sig'))
claims=(R/'inputs/claims.md').read_text(encoding='utf-8-sig')
index=json.loads((R/'inputs/evidence-index.json').read_text(encoding='utf-8-sig'))
known={c['claim_id']:c for c in index['tables']['claims']}
out={'snapshot_hashes':{},'timeline':{},'ownership':{},'local_link_failures':{}}
for f in snapshot['files']:
 p=R/f['snapshot_path']; out['snapshot_hashes'][str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
def norm(s):return re.sub(r'\s+',' ',s).strip()
def svgtxt(p):return norm(' '.join(''.join(e.itertext()) for e in ET.parse(p).iter() if e.tag.split('}')[-1]=='text'))
t=json.loads((R/'timelines/data.json').read_text(encoding='utf-8-sig'))
for v in 'abc':
 text=svgtxt(R/f'timelines/timeline-{v}.svg')
 out['timeline'][v]={'observation_ids_present':[x['id'] for x in t['observations'] if x['id'] in text], 'missing_titles':[], 'missing_details':[], 'missing_claim_ids':[]}
 for x in t['observations']:
  for key,dest in [('title','missing_titles'),('detail','missing_details')]:
   if norm(x[key]) not in text:out['timeline'][v][dest].append(x['id'])
  for c in x['claim_ids']:
   if c not in text:out['timeline'][v]['missing_claim_ids'].append(c)
out['timeline']['claim_record_mismatches']=[]
for x in t['observations']:
 for c,b in x['claim_records'].items():
  if c not in known or norm(b) not in norm(claims):out['timeline']['claim_record_mismatches'].append(c)
o=json.loads((R/'ownership/data.json').read_text(encoding='utf-8-sig'))
for v in 'abc':
 text=svgtxt(R/f'ownership/ownership-{v}.svg'); checks=[]
 for panel in o['snapshots']:
  for e in panel['edges']:
   checks.append({'claim_id':e['claim_id'],'label_present':all(q in text for q in [e['claim_id'],e['ownership_band'],e['acquired_status']]),'claim_exists':e['claim_id'] in known})
 out['ownership'][v]=checks
out['ownership']['dot_edge_mismatch']=[]
for v in 'abc':
 for panel in o['snapshots']:
  dot=(R/f"ownership/ownership-{v}-{panel['id']}.dot").read_text(encoding='utf-8-sig')
  actual=re.findall(r'^(\w+) -> (\w+) \[label="([^"]+)"',dot,re.M)
  expected={(e['from'],e['to'],e['ownership_band']+'\\n'+e['acquired_status']+' · '+e['claim_id']) for e in panel['edges']}
  if set(actual)!=expected:out['ownership']['dot_edge_mismatch'].append([v,panel['id']])
for fam in ['ownership','timelines']:
 p=R/fam/'evidence-map.md'; s=p.read_text(encoding='utf-8-sig'); failures=[]
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if '://' in link or link.startswith('#'):continue
  target=link.split('#')[0]
  if target and not (p.parent/target).exists():failures.append(target)
  out['local_link_failures'][fam]=sorted(set(failures))
 fragment_failures=[]
 for link in re.findall(r'\]\(([^)]+)\)',s):
  if '://' in link or '#' not in link:continue
  target,frag=link.split('#',1); ptarget=p.parent/target
  if not ptarget.exists() or not frag:continue
  body=ptarget.read_text(encoding='utf-8-sig')
  explicit=re.findall(r'id="([^"]+)"',body)
  headings=[re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in re.findall(r'^#{1,6} +(.+)$',body,re.M)]
  if frag not in explicit+headings:fragment_failures.append(link)
 out.setdefault('fragment_failures',{})[fam]=sorted(set(fragment_failures))
(R/'review/semantic-checks.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))

