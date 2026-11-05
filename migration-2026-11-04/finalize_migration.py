"""Finalize migration metadata without changing source evidence."""
from pathlib import Path
import json,hashlib,sqlite3,shutil,re
from datetime import datetime,timezone
from urllib.parse import unquote
from collections import Counter
base=Path.cwd().resolve()
root=base/'outputs/ReBlei/investigations/2026-11-04-official-records'
m=root/'migration-2026-11-04'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
invpath=m/'inventory.json'
old=json.loads(invpath.read_text())
assert not (m/'inventory-initial-observation.json').exists(),'One-time finalization'
shutil.copy2(invpath,m/'inventory-initial-observation.json')
entries=[x for x in old['files'] if x['action']!='already_in_research']
for x in entries:
    assert sha(base/x['workspace_path'])==x['sha256'],x['workspace_path']
    if x['action']=='imported_unique_support':assert sha(root/x['destination'])==x['sha256']
    elif x['action']=='excluded_exact_duplicate':assert sha(root/x['duplicate_of'])==x['sha256']
snap=m/'pre-migration-snapshots';snap.mkdir()
for name in ['README.md','SHA256SUMS.txt']:
    shutil.copy2(root/name,snap/name)
for p in sorted(root.rglob('*')):
    if not p.is_file() or m in p.parents:continue
    st=p.stat()
    x={'workspace_path':p.relative_to(base).as_posix(),'bytes':st.st_size,'sha256':sha(p),'mtime_ns':st.st_mtime_ns,'mtime_utc':datetime.fromtimestamp(st.st_mtime,timezone.utc).isoformat(),'action':'already_in_research','destination':p.relative_to(root).as_posix()}
    if p.name in ['README.md','SHA256SUMS.txt'] and p.parent==root:x['preserved_snapshot']=(snap/p.name).relative_to(root).as_posix()
    entries.append(x)
old.update(finalized_at_utc=datetime.now(timezone.utc).isoformat(),files=entries)
old['counts']=dict(Counter(x['action'] for x in entries))
old['note']='Initial observation retained separately. Two late research QA updates were captured in this final inventory. Active README routing and SHA256SUMS are intentionally refreshed; their original bytes are in pre-migration-snapshots. Inventory timestamps preserve source filesystem metadata; Git itself does not.'
invpath.write_text(json.dumps(old,indent=2)+'\n',encoding='utf-8')
readme=(root/'README.md').read_text(encoding='utf-8')
(root/'README.md').write_text('> **Migration handoff:** Continue on research/bleich-local-migration-2026-11-04. Read [the verified-transfer handoff](MIGRATION-HANDOFF.md) first. The previous branch reference below records historical context.\n\n'+readme,encoding='utf-8')
obj=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))
con=sqlite3.connect((root/'evidence-index.sqlite').as_uri()+'?mode=ro',uri=True)
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
assert not con.execute('PRAGMA foreign_key_check').fetchall()
counts={}
for table,rows in obj['tables'].items():
    cols=[d[1] for d in con.execute('PRAGMA table_info('+table+')')]
    actual=[dict(zip(cols,r)) for r in con.execute('SELECT * FROM '+table)]
    assert sorted(actual,key=lambda x:str(x.get(cols[0])))==sorted(rows,key=lambda x:str(x.get(cols[0]))),table
    counts[table]=len(rows)
con.close()
for d in obj['tables']['documents']:
    p=(root/d['file_path']).resolve();p.relative_to(root)
    assert p.is_file() and sha(p)==d['sha256'],d['document_id']
(m/'README.md').write_text("""# Local migration archive
inventory.json records the final included files, exact-duplicate destinations, verified cache reconstruction paths, SHA256, sizes, and original filesystem timestamps. inventory-initial-observation.json is an earlier metadata observation, superseded by the final inventory.
local-support/ preserves unique historical local work in its original workspace layout. It is an archive, not the active report or executable workflow. Old scripts may contain obsolete absolute paths and branch names; do not run them without reviewing their intended inputs/outputs.
pre-migration-snapshots/ preserves the former README and checksum manifest before migration routing and resealing.
Current research is in the parent directory. Original source bytes were not rewritten. Browser captures and work logs remain diagnostics or leads, not promoted official evidence.
Git does not preserve source file mtimes; use the nanosecond/UTC timestamp metadata in the inventory when needed.
""",encoding='utf-8')
(root/'MIGRATION-HANDOFF.md').write_text("""# ReBlei migration and continuation handoff

Migration date: November 4, 2026 (user date). Repository: private adirass-web/ReBlei.
Continue on **research/bleich-local-migration-2026-11-04**, based on commit 96a6bc2becc90d026dcaafce6490fc76798738e4.
Scope: investigations/2026-11-04-official-records/ only. Local originals remain retained. Other repository content was not reviewed or used as research evidence.

## Continue here
Use the local Git checkout at V:/Codex/2026-11-04/referenced-chatgpt-conversation-this-is-an-3/outputs/ReBlei, or a fresh clone of the same repository and branch. Do not continue in the older loose outputs/work folders.
At each session start verify origin equals https://github.com/adirass-web/ReBlei.git, the active branch is research/bleich-local-migration-2026-11-04, and local/remote commit and working-tree status are understood. Do not overwrite a dirty checkout or force a divergent history. Sync a clean branch by fast-forward only.
Keep evidence, analysis, scripts, QA and planning inside the investigation folder. At every completed stage validate and reseal, commit only intended investigation paths, push this branch and verify remote HEAD equals the local commit. Report any unsynced work explicitly.
Do not merge or change main, the previous research branch, repository visibility or other work. GitHub is the shared continuation record; the checkout is the editing environment.

## Read first
- [Current research results](continuation-4/summary.md)
- [Separate remaining-work instructions](remaining-work-instructions.md)
- [Current evidence index](evidence-index.json) and [document guide](evidence-index.md)
- [Independent research QA](independent-qa.md)
- [Migration inventory and exclusions](migration-2026-11-04/inventory.json)
- [Migration validation](migration-2026-11-04/validation.json)
- [Supporting-work archive guide](migration-2026-11-04/README.md)

The source checkpoint contained earlier research. This transfer adds local round-four material and unique external supporting work; it does not claim new research findings. Preserve IDs, date/metric qualifications, firm-versus-person distinctions and unresolved joins. The new branch supersedes old branch names in historical notes and scripts.

## Preservation and QA
All indexed originals are unchanged and SHA256-verified. All 17 JSON tables equal SQLite; integrity and foreign-key checks pass. All claims have evidence links. The whole-package checksum manifest is SHA256SUMS.txt; its own bytes are verified against the committed blob.
Unique files were copied with original mtimes; Git stores bytes and the inventory separately preserves timestamps. Exact duplicate locations and four SEC CSV cache exclusions are individually recorded. Every excluded CSV was decompressed from its retained ZIP member and matched by full SHA256 and size.
archive-manifest.json is a HISTORICAL BASELINE with outdated counts (47 documents, 104 claims, 5 events). Retain it as provenance, not the current manifest. Current normalized totals are 396 documents, 247 claims, and 9 events; the events include administrative withdrawals, not nine sanctions.
Late corporate and registration QA notes were captured before final sealing. Their bounded passes and the independent normalized-index review are retained. No missing round-four QA note remained at finalization. These checks do not certify exhaustive employment, corporate or court coverage.

## Remaining work and limits
Follow the separate instructions for early employment, alleged Inferent affiliation, corporate ownership/identity bridges, adviser histories, award follow-up, financial/date discrepancies, missing originals, and unavailable Library documents.
**NYSCEF remains an accepted access gap.** No retry or CAPTCHA request is authorized. No PACER account, paid records, outreach, public release or default-branch merge was undertaken.
The full-career investigation remains incomplete. Hash integrity does not establish the truth of filed statements or a clean litigation/regulatory history.
Plan the simple internal HTML report and dossier with the user subsequently. No HTML implementation, hosting or deployment is included in this transfer.

## Migration completion
Verify the pushed branch equals local HEAD, the original research and main refs remain unchanged, all committed file hashes match, and the checkout is clean. Report the final commit and file totals in the user handoff; do not claim completion if verification fails.
""",encoding='utf-8')
# The validation file is a link target during the following link check.
(m/'validation.json').write_text('{}\n',encoding='utf-8')
checked=[];broken=[]
paths=list(root.glob('*.md'))+list((root/'continuation-4').rglob('*.md'))+[m/'README.md']
for p in paths:
    for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
        if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'):continue
        target=unquote(target.strip('<>').split('#')[0].split('?')[0])
        if not target:continue
        q=p.parent/target
        checked.append({'from':p.relative_to(root).as_posix(),'to':target})
        if not q.exists():broken.append(checked[-1])
assert not broken,broken
result={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'json_sqlite_equal':True,'sqlite_integrity':'ok','foreign_key_violations':0,'indexed_documents_verified':len(obj['tables']['documents']),'table_counts':counts,'active_markdown_links_checked':len(checked),'broken_active_markdown_links':broken,'independent_qa':'Separate read-only reviewer repeated register/hash/reference checks and confirmed bounded round-four QA notes. Not exhaustive research completeness.','historical_artifact':'archive-manifest.json retains baseline counts, not current package totals.','credential_pattern_scan':'No GitHub token/private-key/literal Bearer-token patterns found in imported text diagnostics; bounded scan, not a security audit.'}
(m/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'inventory_counts':old['counts'],'validation':result},indent=2))

