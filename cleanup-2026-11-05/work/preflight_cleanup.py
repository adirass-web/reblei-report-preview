from pathlib import Path
import subprocess,json,hashlib
base=Path.cwd().resolve();keep=base/'outputs/ReBlei-migration';old=base/'outputs/ReBlei';fresh=base/'outputs/ReBlei-remote-verification';prefix='investigations/2026-11-04-official-records/';root=keep/prefix
inv=json.loads((root/'cleanup-2026-11-05/local-inventory.json').read_text())
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a])
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert git(keep,'remote','get-url','origin').decode().strip()=='https://github.com/adirass-web/ReBlei.git'
assert not (keep/'.git/objects/info/alternates').exists()
changes=git(keep,'status','--porcelain','-z').decode().split('\0')
assert all(not x or x.startswith('?? '+prefix+'visualization/') for x in changes),changes
head=git(keep,'rev-parse','HEAD').decode().strip()
assert head==git(keep,'ls-remote','origin','refs/heads/research/bleich-local-migration-2026-11-04').decode().split()[0]
assert git(keep,'branch','--show-current').decode().strip()=='research/bleich-local-migration-2026-11-04'
subprocess.run(['git','-C',str(keep),'fsck','--full','--no-dangling'],check=True)
# The entire committed manifest must match local bytes before relying on any retained copy.
manifest={p:h for h,p in (x.split('  ',1) for x in (root/'SHA256SUMS.txt').read_text().splitlines())}
manifest['SHA256SUMS.txt']=sha(root/'SHA256SUMS.txt')
proc=subprocess.Popen(['git','-C',str(keep),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for p,h in manifest.items():
 assert sha(root/p)==h,p
 proc.stdin.write(('HEAD:'+prefix+p+'\n').encode());proc.stdin.flush();hdr=proc.stdout.readline().decode().split();assert hdr[1]=='blob';n=int(hdr[2]);d=hashlib.sha256()
 while n:
  b=proc.stdout.read(min(n,1048576));assert b;n-=len(b);d.update(b)
 assert proc.stdout.read(1)==b'\n' and d.hexdigest()==h,p
proc.stdin.close();assert proc.wait()==0
expected={x['path'] for x in inv['files']};actual=set()
for target in map(Path,inv['cleanup_targets']):
 for p in (target.rglob('*') if target.is_dir() else [target]):
  assert not p.is_symlink() and not p.is_junction(),str(p)
  if p.is_file() and not (old in p.parents and '.git' in p.relative_to(old).parts):actual.add(str(p.resolve()))
assert expected==actual,{'new_files':list(actual-expected),'missing':list(expected-actual)}
for x in inv['files']:
 assert sha(Path(x['path']))==x['sha256'],x['path']
 retained=keep/x['preserved']['repo_path'];assert sha(retained)==x['sha256'],str(retained)
# Account for staged work and all local branch tips.
staged={}
for row in git(old,'ls-files','--stage','-z').decode().split('\0'):
 if row:
  info,p=row.split('\t',1);mode,oid,stage=info.split();staged[p]=oid;assert stage=='0'
assert staged=={x['path']:x['blob'] for x in inv['staged_versions']}
for r in inv['old_local_refs']:subprocess.run(['git','-C',str(keep),'merge-base','--is-ancestor',r['commit'],head],check=True)
for x in inv['staged_versions']:assert sha(keep/x['preserved']['repo_path'])==x['sha256']
# The disposable clone contains the remote source plus our exact cleanup snapshot.
assert git(fresh,'remote','get-url','origin').decode().strip()=='https://github.com/adirass-web/ReBlei.git'
actual_fresh={p.relative_to(fresh).as_posix() for p in fresh.rglob('*') if p.is_file() and '.git' not in p.relative_to(fresh).parts}
assert actual_fresh=={prefix+p for p in manifest},'Unexpected disposable clone file'
for p,h in manifest.items():assert sha(fresh/prefix/p)==h,p
print(json.dumps({'verified_remote_commit':head,'source_files_safe_to_remove':len(expected),'unique_local_files_preserved':inv['counts']['recovered'],'staged_versions_accounted_for':len(staged),'retained_checkout_self_contained':True,'manifest_files_verified':len(manifest),'active_visualization_work_retained':True}))
