"""Record the completed bounded cleanup and reseal its stable research snapshot."""
from pathlib import Path
import json,hashlib,sqlite3,subprocess
from datetime import datetime,timezone
root=Path.cwd();repo=root.parent.parent;workspace=repo.parent.parent;cleanup=root/'cleanup-2026-11-05'
receipt=json.loads((cleanup/'cleanup-receipt.json').read_text(encoding='utf-8-sig'));caches=json.loads((cleanup/'cache-verification.json').read_text(encoding='utf-8'))
assert receipt['all_targets_removed']
for item in receipt['removed']:assert not Path(item['path']).exists(),item['path']
assert not (repo/'.git/objects/info/alternates').exists()
assert {p.name for p in workspace.iterdir()}=={'outputs'}
assert {p.name for p in (workspace/'outputs').iterdir()}=={'ReBlei-migration'}
old={p:h for h,p in (line.split('  ',1) for line in (root/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines())}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in old.items():assert sha(root/p)==h,p
index=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))
for d in index['tables']['documents']:assert sha(root/d['file_path'])==d['sha256'],d['document_id']
with sqlite3.connect(root/'evidence-index.sqlite') as con:
 assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
 assert not con.execute('PRAGMA foreign_key_check').fetchall()
subprocess.run(['git','-C',str(repo),'fsck','--full','--no-dangling'],check=True)
removed_bytes=int(receipt['removed_bytes'])+int(caches['bytes']);removed_files=int(receipt['removed_files'])+len(caches['files'])
proof={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'preservation_checkpoint':receipt['preflight']['verified_remote_commit'],'all_inventoried_targets_removed':True,'retained_checkout':str(repo),'retained_checkout_object_integrity':'passed without alternates','original_source_hashes_verified':len(index['tables']['documents']),'sqlite_integrity':'passed','total_removed_files_including_caches':removed_files,'total_removed_file_bytes_including_caches':removed_bytes,'count_scope':'Includes disposable verification clone, old Git objects and expanded caches; file bytes, not net free-space gain.','active_visualization_work':'Retained unchanged; separate ongoing task owns delivery.','final_manifest_scope':'Previously sealed completed research plus cleanup records; excludes active visualization.'}
(cleanup/'final-local-verification.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
p=cleanup/'README.md';s=p.read_text(encoding='utf-8');s=s.replace('Completion and actual removal counts will be recorded in `cleanup-receipt.json` and this report updated after deletion.','Completion and actual removal counts are recorded in [cleanup-receipt.json](cleanup-receipt.json).')
assert '## Completed cleanup' not in s
s+='''\n## Completed cleanup\n\nPreservation checkpoint `0cea55390695459bfc91d57a1ef9f6420b737417` was pushed and verified before deletion. All listed targets were removed. Including the four expanded caches, **3,472 files containing 2,246,770,055 bytes (2.25 GB)** were removed. Counts include the old Git store and disposable verification clone; they are file bytes removed, not a claim about net disk-space gain after creating preservation copies.\n\nOnly `outputs/ReBlei-migration` remains in this task workspace. It passed Git object-integrity checks again without alternates. All 396 indexed source hashes remain unchanged; SQLite integrity and foreign keys pass. See [final-local-verification.json](final-local-verification.json). The active visualization folder remains protected and was not cleaned or committed by this task.\n\nThe final checksum manifest retains the isolated snapshot's file set and adds cleanup records. All preceding hashes were checked before updating this report, the continuation handoff and cleanup records. It deliberately excludes the separate task's changing visualization files. Historical cleanup scripts describe this one completed operation; they must not be rerun against a changed workspace.\n'''
p.write_text(s,encoding='utf-8')
p=root/'MIGRATION-HANDOFF.md';s=p.read_text(encoding='utf-8');marker='# ReBlei migration and continuation handoff\n'
assert s.startswith(marker)
s=s.replace(marker,marker+'\n**November 5 cleanup update:** remote recovery and the dossier rebuild were verified, then redundant local originals and the old checkout were removed. Continue in `outputs/ReBlei-migration`, which now has its own complete Git object store, or clone the migration branch. See [cleanup completion and preservation proof](cleanup-2026-11-05/README.md). Statements below that local originals remain retained describe the earlier migration checkpoint. A separate visualization task may have work in progress under `visualization/`; preserve it when syncing.\n',1);p.write_text(s,encoding='utf-8')
paths=set(old)|{p.relative_to(root).as_posix() for p in cleanup.rglob('*') if p.is_file()}
(root/'SHA256SUMS.txt').write_text(''.join(sha(root/p)+'  '+p+'\n' for p in sorted(paths)),encoding='utf-8')
print(json.dumps({'files_including_manifest':len(paths)+1,'removed_files':removed_files,'removed_bytes':removed_bytes,'original_source_hashes_verified':len(index['tables']['documents'])}))
