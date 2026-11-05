"""Seal the current evidence package; originals are read, never rewritten."""
from pathlib import Path
import json,hashlib,sqlite3
root=Path('.')
obj=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))
for doc in obj['tables']['documents']:
 path=(root/doc['file_path']).resolve();path.relative_to(root.resolve())
 assert hashlib.sha256(path.read_bytes()).hexdigest()==doc['sha256'],doc['document_id']
con=sqlite3.connect(root/'evidence-index.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not con.execute('PRAGMA foreign_key_check').fetchall();con.close()
files=sorted((p for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'),key=lambda p:p.as_posix())
(root/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.as_posix()+'\n' for p in files),encoding='utf-8')
print(json.dumps({'indexed_document_hashes_verified':len(obj['tables']['documents']),'manifest_entries':len(files),'sqlite_integrity':'ok','foreign_keys':'passed'},indent=2))
