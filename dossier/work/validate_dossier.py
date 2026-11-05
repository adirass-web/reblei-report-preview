"""Validate the authored dossier and create this release's verification record."""
from pathlib import Path
import json,re,hashlib,subprocess,html
from urllib.parse import urlsplit,unquote
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[2];D=R/'dossier';repo=R.parents[1]
base='4826d590fdc656bf9f33b4e026455cac9a9930a0'
prefix='investigations/2026-11-04-official-records/'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
t=json.loads((R/'evidence-index.json').read_text(encoding='utf-8'))['tables']
for p in ['evidence-index.json','evidence-index.sqlite','remaining-work-instructions.md']:
 assert hashlib.sha256(git('show',base+':'+prefix+p)).hexdigest()==sha(R/p),p
main=(D/'full-dossier.md').read_text(encoding='utf-8')
digest=sha(D/'full-dossier.md')
assert digest in (D/'review/independent-fidelity-review.md').read_text(encoding='utf-8'), 'Final reviewer hash does not match manuscript'
assert not re.search(r'\[\[[^\]]+\]\]',main),'Unexpanded reference'
c=(D/'claims.md').read_text(encoding='utf-8')
def esc(v):return html.escape(str(v if v is not None else 'Not established'),quote=False).replace('|','&#124;').replace('\n','<br>')
for x in t['claims']:assert esc(x['statement']) in c,x['claim_id']
for x in t['claim_evidence']:assert esc(x['locator']) in c,x['claim_id']
assert len(re.findall(r'^## ',c,re.M))==247
assert len(re.findall(r'^\| \[',c,re.M))==444
conf=(D/'conflicts-and-gaps.md').read_text(encoding='utf-8')
for x in t['conflicts']:
 assert esc(x['resolution']) in conf,x['conflict_id']
 assert esc(x['status']) in conf,x['conflict_id']
assert len(re.findall(r'^## ',conf,re.M))==26
record={'research_cutoff':'2026-11-04','checked_at_utc':datetime.now(timezone.utc).isoformat(),'base_research_commit':base,'index_sha256':sha(R/'evidence-index.json'),'manuscript_sha256':digest,'source_index_and_followup_instructions_unchanged':True,'claims_preserved':247,'evidence_links_preserved':444,'conflicts_preserved':26,'all_indexed_source_hashes_verified':True,'review_scope':'Three bounded independent/cross-reviews; source sampling and full manuscript review. Not fresh research, exhaustive court coverage or rendered/printed layout QA.','pre_release_manifest_sha256':sha(R/'SHA256SUMS.txt')}
for x in t['documents']:assert sha(R/x['file_path'])==x['sha256'],x['document_id']
# The release record is a generated navigation target; create before link validation.
(D/'release.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
checked=0
for p in [D/x for x in ['README.md','full-dossier.md','claims.md','documents.md','entities-and-roles.md','events.md','financial-observations.md','conflicts-and-gaps.md']]:
 text=p.read_text(encoding='utf-8-sig')
 ids=re.findall(r'<a id="([^"]+)"',text);assert len(ids)==len(set(ids)),p.name
 for url in re.findall(r'\[[^\]\n]*\]\(([^)\n]+)\)',text):
  u=urlsplit(html.unescape(url))
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p
  target.relative_to(R.resolve());assert target.exists(),(p.name,url)
  if u.fragment:
   assert target.suffix=='.md',(p.name,url)
   body=target.read_text(encoding='utf-8-sig');assert 'id="'+unquote(u.fragment)+'"' in body,(p.name,url)
  checked+=1
record['local_links_and_fragments_checked']=checked
record['broken_local_links']=0
record['review_notes']={p.name:sha(p) for p in sorted((D/'review').glob('*.md'))}
record['dossier_files_sha256_excluding_release']={p.relative_to(D).as_posix():sha(p) for p in sorted(D.rglob('*')) if p.is_file() and p.name!='release.json'}
(D/'release.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:record[k] for k in ['manuscript_sha256','claims_preserved','evidence_links_preserved','conflicts_preserved','local_links_and_fragments_checked','broken_local_links','source_index_and_followup_instructions_unchanged']},indent=2))
