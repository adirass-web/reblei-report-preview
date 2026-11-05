"""Inventory only this investigation's redundant local files; never delete."""
from pathlib import Path
from collections import Counter
import json,hashlib,shutil,subprocess
from datetime import datetime,timezone
base=Path.cwd().resolve();keep=base/'outputs/ReBlei-migration';fresh=base/'outputs/ReBlei-remote-verification';old=base/'outputs/ReBlei'
prefix='investigations/2026-11-04-official-records/'
root=keep/prefix;dest=root/'cleanup-2026-11-05'
def git(repo,*a):return subprocess.check_output(['git','-C',str(repo),*a])
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
known={}
for line in (fresh/prefix/'SHA256SUMS.txt').read_text().splitlines():
 h,p=line.split('  ',1);known[h]={'repo_path':prefix+p,'basis':'verified remote package'}
known[sha(fresh/prefix/'SHA256SUMS.txt')]={'repo_path':prefix+'SHA256SUMS.txt','basis':'verified remote manifest'}
for p in git(fresh,'ls-tree','-r','--name-only','HEAD').decode().splitlines():
 if p.startswith(prefix):continue
 h=hashlib.sha256(git(fresh,'show','HEAD:'+p)).hexdigest();known[h]={'repo_path':p,'basis':'existing remote repository file; not research input'}
remotehead=git(fresh,'rev-parse','HEAD').decode().strip()
refs=[]
for line in git(old,'for-each-ref','--format=%(refname) %(objectname)','refs/heads').decode().splitlines():
 name,rev=line.split()
 subprocess.run(['git','-C',str(fresh),'merge-base','--is-ancestor',rev,remotehead],check=True)
 refs.append({'ref':name,'commit':rev,'reachable_from_remote':True})
targets=[base/'work',base/'.playwright-mcp',old]
targets += [p for p in (base/'outputs').iterdir() if p.name not in ['ReBlei','ReBlei-migration','ReBlei-remote-verification']]
external=Path('V:/Codex/editorial-skill-input.json')
if external.exists():targets.append(external)
rows=[];local_hash={}
def preserve(p,label):
 h=sha(p);local_hash[str(p.resolve())]=h
 rec={'path':str(p.resolve()),'bytes':p.stat().st_size,'sha256':h}
 if h in known:rec.update(action='duplicate',preserved=known[h])
 else:
  out=dest/'recovered-files'/(h[:32]+p.suffix[:10])
  out.parent.mkdir(parents=True,exist_ok=True)
  with p.open('rb') as source, out.open('wb') as target:shutil.copyfileobj(source,target,1048576)
  shutil.copystat(p,out);assert sha(out)==h
  known[h]={'repo_path':prefix+out.relative_to(root).as_posix(),'basis':'recovered local support; must be pushed before deletion'}
  rec.update(action='recovered',preserved=known[h])
 rows.append(rec)
for target in targets:
 seq=sorted(target.rglob('*')) if target.is_dir() else [target]
 for p in seq:
  assert not p.is_symlink() and not p.is_junction(),str(p)
  if not p.is_file():continue
  if old in p.parents and '.git' in p.relative_to(old).parts:continue
  label=Path('external/editorial-skill-input.json') if p==external else p.relative_to(base)
  preserve(p,label)
# Preserve staged versions too, if they differ from both remote and disk.
staged=[];proc=subprocess.Popen(['git','-C',str(old),'cat-file','--batch'],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
for row in git(old,'ls-files','--stage','-z').decode().split('\0'):
 if not row:continue
 info,p=row.split('\t',1);mode,oid,stage=info.split();assert stage=='0'
 proc.stdin.write((oid+'\n').encode());proc.stdin.flush();hdr=proc.stdout.readline().decode().split();n=int(hdr[2]);data=proc.stdout.read(n);assert len(data)==n and proc.stdout.read(1)==b'\n'
 h=hashlib.sha256(data).hexdigest()
 if h not in known:
  out=dest/'recovered-files'/(h[:32]+Path(p).suffix[:10]);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(data)
  known[h]={'repo_path':prefix+out.relative_to(root).as_posix(),'basis':'unique staged local version; must be pushed before deletion'}
 staged.append({'path':p,'blob':oid,'sha256':h,'preserved':known[h]})
proc.stdin.close();assert proc.wait()==0
out={'created_at_utc':datetime.now(timezone.utc).isoformat(),'verified_remote_commit':remotehead,'retained_checkout':str(keep),'old_local_refs':refs,'files':rows,'staged_versions':staged,'cleanup_targets':[str(p.resolve()) for p in targets],'counts':dict(Counter(x['action'] for x in rows)),'total_file_bytes':sum(x['bytes'] for x in rows),'recovered_staged_count':sum(x['preserved']['basis'].startswith('unique staged') for x in staged)}
(dest/'local-inventory.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:out[k] for k in ['counts','total_file_bytes','recovered_staged_count']}))
