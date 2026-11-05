from pathlib import Path
import subprocess,hashlib,json
repo=Path('outputs/ReBlei');prefix='investigations/2026-11-04-official-records/';branch='research/bleich-official-records-2026-11-04'
def git(*a):return subprocess.check_output(['git','-C',str(repo),*a])
head=git('rev-parse','HEAD').decode().strip();remote=git('ls-remote','--heads','origin',branch).decode().split()[0];assert remote==head
changed=git('diff','--name-only','origin/main','HEAD').decode().splitlines();assert all(x.startswith(prefix) for x in changed)
assert git('status','--porcelain')==b''
manifest=(repo/prefix/'SHA256SUMS.txt').read_text(encoding='utf8').splitlines()
for line in manifest:
 sha,p=line.split('  ',1);blob=git('show','HEAD:'+prefix+p);assert hashlib.sha256(blob).hexdigest()==sha
print(json.dumps({'commit':head,'remote_matches':True,'clean_checkout':True,'changed_files':len(changed),'all_changes_in_requested_folder':True,'committed_manifest_entries_verified':len(manifest),'main_branch_changed':False},indent=2))
