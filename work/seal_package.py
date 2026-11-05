"""Seal the current evidence package; originals are read, never rewritten."""
from pathlib import Path
import json,hashlib,sqlite3,subprocess,sys
root=Path('.')
obj=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))
for doc in obj['tables']['documents']:
 path=(root/doc['file_path']).resolve();path.relative_to(root.resolve())
 assert hashlib.sha256(path.read_bytes()).hexdigest()==doc['sha256'],doc['document_id']
con=sqlite3.connect(root/'evidence-index.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not con.execute('PRAGMA foreign_key_check').fetchall();con.close()
# Git owns the package boundary. Include new deliverables but omit ignored runtimes/caches.
# Tracked evidence is included even when an ignore rule would now match its name.
repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],text=True).strip())
prefix=root.resolve().relative_to(repo.resolve()).as_posix()+'/'
options=['--cached'] if '--tracked-only' in sys.argv else ['--cached','--others','--exclude-standard']
listed=subprocess.check_output(['git','ls-files',*options,'--full-name','-z','--',prefix],cwd=repo).decode('utf-8').split('\0')
files=[]
for name in sorted(set(x for x in listed if x)):
 path=repo/name
 path.resolve().relative_to(root.resolve())
 assert path.is_file(),('Missing package file',name)
 if path.name=='SHA256SUMS.txt' and path.parent.resolve()==root.resolve():continue
 files.append(Path(path.relative_to(root.resolve())))
(root/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.as_posix()+'\n' for p in files),encoding='utf-8')
print(json.dumps({'indexed_document_hashes_verified':len(obj['tables']['documents']),'manifest_entries':len(files),'sqlite_integrity':'ok','foreign_keys':'passed'},indent=2))
