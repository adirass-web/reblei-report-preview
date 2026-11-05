from pathlib import Path
import json,subprocess,hashlib,struct,zlib
from datetime import datetime,timezone
base=Path.cwd().resolve()
repo=base/'outputs/ReBlei-migration'
root=repo/'investigations/2026-11-04-official-records'
fresh=base/'outputs/ReBlei-remote-verification'
assert not (fresh/'.git/objects/info/alternates').exists()
subprocess.run(['git','-C',str(fresh),'fsck','--full','--no-dangling'],check=True)
inv=json.loads((root/'migration-2026-11-04/inventory.json').read_text())
head=subprocess.check_output(['git','-C',str(fresh),'rev-parse','HEAD']).decode().strip()
out=[]
for x in inv['files']:
 if x['action']!='excluded_reproducible_cache':continue
 p=base/x['workspace_path'];p.resolve().relative_to(base);assert p.is_file()
 with p.open('rb') as f:localhash=hashlib.file_digest(f,'sha256').hexdigest()
 assert localhash==x['sha256']
 spec='HEAD:investigations/2026-11-04-official-records/'+x['reconstruct_from']
 proc=subprocess.Popen(['git','-C',str(fresh),'show',spec],stdout=subprocess.PIPE)
 rawhash=hashlib.sha256();expanded=hashlib.sha256();size=0
 h=proc.stdout.read(30);rawhash.update(h)
 sig,ver,flags,method,mt,md,crc,cs,us,nl,el=struct.unpack('<IHHHHHIIIHH',h)
 assert sig==0x04034b50 and method==8
 extra=proc.stdout.read(nl+el);rawhash.update(extra);de=zlib.decompressobj(-15)
 while True:
  chunk=proc.stdout.read(512*1024)
  if not chunk:break
  rawhash.update(chunk);b=de.decompress(chunk);expanded.update(b);size+=len(b)
 b=de.flush();expanded.update(b);size+=len(b)
 assert proc.wait()==0 and de.eof
 assert expanded.hexdigest()==localhash and size==p.stat().st_size
 assert rawhash.hexdigest()==x['compressed_sha256']
 out.append({'path':str(p.resolve()),'sha256':localhash,'bytes':size,'remote_original':x['reconstruct_from'],'remote_original_sha256':rawhash.hexdigest(),'action':'remove_reproducible_expanded_cache_after_exact_verification'})
result={'verified_at_utc':datetime.now(timezone.utc).isoformat(),'remote_commit':head,'remote_clone_without_alternates':True,'git_fsck':'passed','files':out,'bytes':sum(x['bytes'] for x in out)}
(root/'cleanup-2026-11-05/cache-verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'verified_caches':len(out),'reclaimable_bytes':result['bytes'],'remote_commit':head}))
