from pathlib import Path
from collections import defaultdict
from urllib.parse import quote
import json,hashlib,re,html
R=Path(__file__).resolve().parents[2];D=R/'dossier'
t=json.loads((R/'evidence-index.json').read_text(encoding='utf-8'))['tables']
C={r['claim_id']:r for r in t['claims']};S={r['subject_id']:r['display_name'] for r in t['subjects']};B={r['document_id']:r for r in t['documents']}
def a(k,v):return k+'-'+hashlib.sha256(v.encode()).hexdigest()[:16]
def e(v):return html.escape(str(v if v is not None else 'Not established'),quote=False).replace('|','&#124;').replace('\n','<br>')
def cl(v):return '['+v+'](claims.md#'+a('c',v)+')'
def wr(f,l):(D/f).write_text('\n'.join(l)+'\n',encoding='utf-8')
def local(p):return '../'+quote(p,safe='/')
E=defaultdict(list);X=defaultdict(list)
for r in t['claim_evidence']:E[r['claim_id']].append(r)
for r in t['conflict_claims']:X[r['conflict_id']].append(r['claim_id'])
l=['# Claim and evidence appendix','','All 247 assertions are reproduced with their recorded status and every evidence link. They include search observations, candidates and earlier formulations, not just verified facts. The narrative uses the latest reviewed interpretation. Register wording is retained, including compressed spacing.','','[Full dossier](full-dossier.md) | [Documents](documents.md) | [Conflicts](conflicts-and-gaps.md)','','Physical PDF pages are 1-based. CSV ordinal conventions differ between source packets; follow the exact locator.']
for c in C.values():
 cid=c['claim_id'];l+=['','<a id="'+a('c',cid)+'"></a>','## '+cid,'','Subject: '+e(S.get(c['subject_id'],c['subject_id'])),'','Evidence status: '+e(c['evidence_status'])+'; recorded review status: '+e(c['review_status']),'',e(c['statement']),'']
 if cid=='ID-C012':l+=['Later qualification: the combined CEO/CCO acquired-status field does not independently date the CCO role. See '+cl('EMP4-C05')+' and '+cl('EMP5-C03')+'.','']
 related=[r['conflict_id'] for r in t['conflict_claims'] if r['claim_id']==cid]
 if related:l+=['Issues: '+', '.join('['+v+'](conflicts-and-gaps.md#'+a('x',v)+')' for v in related),'']
 l+=['| Supporting record | Source class | Exact locator |','|---|---|---|']
 for r in E[cid]:
  b=B[r['document_id']]
  l+=['| ['+e(b['document_id'])+'](documents.md#'+a('d',b['document_id'])+') / [retained file]('+local(b['file_path'])+') | '+e(b['source_class'])+' | '+e(r['locator'])+' |']
wr('claims.md',l)
l=['# Preserved document catalogue','','All 396 indexed source representations appear below: originals, compressed members, derivatives, unjoined leads and failed responses. This is not a unique-filing count. SHA256 identifies bytes, not truth.','','[Full dossier](full-dossier.md) | [Claims](claims.md) | [Complete metadata](../evidence-index.json)']
for b in B.values():
 l+=['','<a id="'+a('d',b['document_id'])+'"></a>','## '+e(b['document_id']),'',e(b['title']),'','| Field | Recorded value |','|---|---|']
 for k in ['authority','document_type','source_class','filing_date','period_end','accession_id','pdf_pages','retrieved_at_utc','preservation_status','sha256']:l+=['| '+k.replace('_',' ')+' | '+e(b[k])+' |']
 l+=['','[Retained local file]('+local(b['file_path'])+')']
 if b['official_url']:l+=['[Source URL]('+b['official_url']+')']
 l+=['','Additional identifiers and archive reconstruction metadata remain in this document row of the [source index](../evidence-index.json).']
wr('documents.md',l)
l=['# Conflicts, qualifications and access gaps','','All 26 registered issues are retained, including resolved distinctions and rejected identities. Historical status text is preserved; current-reading notes prevent an older access gap being mistaken for a current one.','','[Current follow-up instructions](../remaining-work-instructions.md) | [Full dossier](full-dossier.md)']
for r in t['conflicts']:
 l+=['','<a id="'+a('x',r['conflict_id'])+'"></a>','## '+r['conflict_id']+': '+e(r['topic']),'','Recorded status: '+e(r['status']),'',e(r['resolution']),'']
 if r['conflict_id'] in ['EVT-X001','EVT-X002']:l+=['Current-reading note: original Cboe orders were subsequently recovered. The historical missing-order wording is superseded. See '+cl('LIT-C004' if r['conflict_id']=='EVT-X002' else 'LIT-C006')+', '+cl('LIT-C005' if r['conflict_id']=='EVT-X002' else 'LIT-C008')+' and the events chapter. The separate June/July 2013 date issue remains open.','']
 if X[r['conflict_id']]:l+=['Evidence: '+', '.join(cl(v) for v in X[r['conflict_id']])]
wr('conflicts-and-gaps.md',l)
def table(l,rows):
 if not rows:return
 keys=list(rows[0]);l+=['| '+' | '.join(k.replace('_',' ') for k in keys)+' |','|'+'|'.join('---' for k in keys)+'|']
 for r in rows:
  vals=[]
  for k in keys:
   v=r[k]
   if k=='claim_id' and v:vals.append(cl(v));continue
   if k in ['entity_id','person_id','source_subject_id','target_subject_id','respondent_entity_id','claimant_entity_id'] and v:v=str(v)+': '+S.get(v,'')
   vals.append(e(v))
  l+=['| '+' | '.join(vals)+' |']
l=['# People, entities, roles and relationships','','Inclusion can mean a conditional affiliation, unresolved name or rejected candidate. Read status and notes. Unknown dates do not create tenure periods.','','[Full dossier](full-dossier.md) | [Claims](claims.md)']
for k in ['persons','entities','identifiers','roles','relationships']:l+=['','## '+k.replace('_',' ').capitalize(),''];table(l,t[k])
wr('entities-and-roles.md',l)
l=['# Financial observation register','','All 67 observations retain the metric, amount, units, date basis and qualification. Filing dates do not automatically measure assets. Discrepant observations must not be silently corrected or combined.','','[Full dossier](full-dossier.md) | [Claims](claims.md)',''];table(l,t['financial_observations']);wr('financial-observations.md',l)
l=['# Event register','','Nine records comprise five firm regulatory matters, one arbitration and three administrative withdrawals. They are not nine sanctions against Bleich. Administrative filing subjects resolve through linked claims; blank respondent fields are intentional.','','[Full dossier](full-dossier.md) | [Claims](claims.md)']
for r in t['events']:
 l+=['','## '+r['event_id'],''];table(l,[r]);l+=['','Evidence: '+', '.join(cl(v['claim_id']) for v in t['event_claims'] if v['event_id']==r['event_id'])]
wr('events.md',l)
text='\n\n'.join(p.read_text(encoding='utf-8-sig') for p in sorted((D/'sections').glob('*.md')))
used=re.findall(r'\[\[([^\]]+)\]\]',text);assert not set(used)-set(C),set(used)-set(C)
text=re.sub(r'\[\[([^\]]+)\]\]',lambda m:cl(m.group(1)),text);wr('full-dossier.md',[text])
coverage={'source_commit':'4826d590fdc656bf9f33b4e026455cac9a9930a0','index_sha256':hashlib.sha256((R/'evidence-index.json').read_bytes()).hexdigest(),'counts':{k:len(v) for k,v in t.items()},'narrative_claim_ids':sorted(set(used)),'appendix_claim_ids':list(C),'appendix_document_ids':list(B),'appendix_only_claim_ids':sorted(set(C)-set(used)),'claims_in_appendix':len(C),'evidence_links_in_appendix':len(t['claim_evidence']),'conflicts_in_appendix':len(t['conflicts']),'source_files_unchanged':all(hashlib.sha256((R/b['file_path']).read_bytes()).hexdigest()==b['sha256'] for b in B.values())}
assert coverage['source_files_unchanged']
(D/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n',encoding='utf-8')
print('Built dossier appendices; all indexed sources hash-match. Narrative claim count:',len(set(used)))
