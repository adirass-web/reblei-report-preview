from pathlib import Path
import json,hashlib,subprocess,shutil
from datetime import datetime,timezone
v=Path('visualization'); r=Path('.')
files=['dossier/full-dossier.md','dossier/release.json','dossier/claims.md','evidence-index.json']
release=json.loads((r/'dossier/release.json').read_text())
assert hashlib.sha256((r/'dossier/full-dossier.md').read_bytes()).hexdigest()==release['manuscript_sha256']
assert hashlib.sha256((r/'evidence-index.json').read_bytes()).hexdigest()==release['index_sha256']
rows=[]
for name in files:
 dst=v/'inputs'/Path(name).name
 shutil.copyfile(r/name,dst)
 rows.append({'repository_path':'investigations/2026-11-04-official-records/'+name,'snapshot_path':dst.relative_to(v).as_posix(),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest()})
commit=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip()
(v/'source-snapshot.json').write_text(json.dumps({'captured_at_utc':datetime.now(timezone.utc).isoformat(),'source_commit':commit,'branch':'research/bleich-local-migration-2026-11-04','research_cutoff':'2026-11-04','review_release_hashes_match':True,'files':rows},indent=2))
(v/'.gitignore').write_text('.runtime/\n__pycache__/\n*.pyc\n')
(v/'TASKS.md').write_text('''# Visualization tasks\n\nScope: six draft visual alternatives, inventory and integration-ready assets only. No research, dossier or HTML-front edits.\n\n- [x] T1 Verify reviewed input release and pin immutable snapshot.\n- [ ] T2 Write visual inventory and shared evidence rules.\n- [ ] T3 Create three ownership-layout alternatives with the same selected relationships.\n- [ ] T4 Create three timeline-layout alternatives with the same selected observations.\n- [ ] T5 Independently review claim/date/identity fidelity and inspect all rendered graphics.\n- [ ] T6 Produce comparison guide, captions, editable sources, SVG/PDF/PNG outputs and scoped checksums.\n- [ ] T7 Commit only visualization files, push migration branch and verify remote bytes.\n\nDefaults: static English graphics, restrained professional style, source IDs visible, November 4 research cut-off. Alternatives are draft layouts for user selection, not new factual scenarios. Ownership snapshots are separate panels. Unknown employment intervals are not fabricated. No unverified affiliation is connected into a confirmed chain.\n''')
(v/'checkpoints/01-inputs-pinned.md').write_text(f'''# Checkpoint: reviewed inputs pinned\n\nStatus: in progress\nBranch: research/bleich-local-migration-2026-11-04\nSource commit: {commit}\nDate: November 5, 2026 (user date)\n\nDossier and index hashes match dossier/release.json. Copies and provenance are inside visualization/inputs and source-snapshot.json. Existing cleanup-2026-11-05 work is unrelated and will remain untouched.\n\nRemaining: inventory; ownership and timeline production; independent QA; six visual review; scoped manifest and GitHub delivery. All new task files stay inside visualization. No root research manifest or dossier is edited.\n''')
print(json.dumps({'source_commit':commit,'inputs':len(rows),'hashes_match_reviewed_release':True}))
