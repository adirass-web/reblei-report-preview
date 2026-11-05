from pathlib import Path
import subprocess,hashlib,sys
repo=Path(sys.argv[1]) if len(sys.argv)>1 else Path('outputs/ReBlei')
prefix='investigations/2026-11-04-official-records/'
paths=subprocess.check_output(['git','-C',str(repo),'diff','--cached','--name-only','-z']).decode().strip('\0').split('\0')
assert paths and all(p.startswith(prefix) for p in paths),'Unexpected staged path'
for p in paths:
 blob=subprocess.check_output(['git','-C',str(repo),'show',':'+p]);local=(repo/p).read_bytes()
 assert hashlib.sha256(blob).digest()==hashlib.sha256(local).digest(),('Git changed bytes',p)
print(f'Verified {len(paths)} staged files byte-for-byte; all changes inside {prefix}')
