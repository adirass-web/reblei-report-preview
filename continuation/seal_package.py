from pathlib import Path
import hashlib,json,sqlite3
root=Path('.')
data=json.loads((root/'evidence-index.json').read_text(encoding='utf-8'))['tables']
for doc in data['documents']:
 p=root/doc['file_path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==doc['sha256'],doc['document_id']
con=sqlite3.connect(root/'evidence-index.sqlite');assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok';assert not con.execute('PRAGMA foreign_key_check').fetchall();con.close()
assert len(data['events'])==5
assert not any(x['value']=='1977777' for x in data['identifiers'])
assert not any(r['entity_id']=='E021' for r in data['roles'])
files=sorted((p for p in root.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt'),key=lambda p:p.as_posix())
(root/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.as_posix()+'\n' for p in files),encoding='utf-8')
print('All indexed hashes and database checks pass; manifest',len(files),'files')
