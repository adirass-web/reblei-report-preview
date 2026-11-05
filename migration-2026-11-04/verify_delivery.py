"""Verify the exact migration package and protected refs; no research or source edits."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[1]
repo=root.parents[1]
prefix=root.relative_to(repo).as_posix()+'/'
branch='research/bleich-local-migration-2026-11-04'
def git(*args):return subprocess.check_output(['git','-C',str(repo),*args])
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert git('remote','get-url','origin').decode().strip()=='https://github.com/adirass-web/ReBlei.git'
assert git('branch','--show-current').decode().strip()==branch
inv=json.loads((root/'migration-2026-11-04/inventory.json').read_text())
for x in inv['files']:
    if x['action']=='excluded_reproducible_cache':assert sha(root/x['reconstruct_from'])==x['compressed_sha256']
    else:
        target=x.get('preserved_snapshot') or x.get('destination') or x['duplicate_of']
        assert sha(root/target)==x['sha256'],target
manifest={}
for line in (root/'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    h,p=line.split('  ',1);assert sha(root/p)==h,p;manifest[p]=h
files={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
assert set(manifest)==files-{'SHA256SUMS.txt'},('manifest coverage',files-set(manifest))
manifest['SHA256SUMS.txt']=sha(root/'SHA256SUMS.txt')
ref='HEAD' if '--remote' in sys.argv else ''
tracked=git('ls-tree','-r','--name-only','HEAD','--',prefix).decode().splitlines() if ref else git('ls-files','--',prefix).decode().splitlines()
assert {p[len(prefix):] for p in tracked}==files,'Git path coverage differs from local package'
proc=subprocess.Popen(['git','-C',str(repo),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for p,h in manifest.items():
    spec=('HEAD:' if ref else ':')+prefix+p
    proc.stdin.write((spec+'\n').encode());proc.stdin.flush()
    header=proc.stdout.readline().decode().strip().split()
    assert len(header)==3 and header[1]=='blob',spec
    size=int(header[2]);remaining=size;d=hashlib.sha256()
    while remaining:
        chunk=proc.stdout.read(min(1024*1024,remaining));assert chunk
        remaining-=len(chunk);d.update(chunk)
    assert proc.stdout.read(1)==b'\n'
    assert d.hexdigest()==h,('Git changed bytes',p)
proc.stdin.close();assert proc.wait()==0
head=git('rev-parse','HEAD').decode().strip()
if ref:
    refs=dict((line.split()[1].removeprefix('refs/heads/'),line.split()[0]) for line in git('ls-remote','--heads','origin','main','research/bleich-official-records-2026-11-04',branch).decode().splitlines())
    assert refs[branch]==head
    for name,h in inv['protected_refs'].items():assert refs[name]==h,('Protected ref changed',name)
    assert not git('status','--porcelain')
    changed=git('diff','--name-only',inv['source_commit'],'HEAD').decode().splitlines()
else:changed=git('diff','--cached','--name-only').decode().splitlines()
assert changed and all(p.startswith(prefix) for p in changed)
print(json.dumps({'commit':head,'mode':'remote committed verification' if ref else 'staged verification','branch':branch,'file_count':len(files),'bytes':sum((root/p).stat().st_size for p in files),'whole_package_hashes_verified':len(manifest),'migration_inventory_verified':True,'changed_paths':len(changed),'all_changes_in_investigation':True,'remote_and_protected_refs_verified':bool(ref),'clean_checkout':bool(ref)},indent=2))

