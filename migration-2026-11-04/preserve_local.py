"""Inventory and preserve this investigation only. Run once from its workspace."""
from pathlib import Path
import hashlib,json,shutil,struct,zlib,subprocess
from datetime import datetime,timezone
from collections import Counter
base=Path.cwd().resolve()
repo=base/'outputs/ReBlei'
root=repo/'investigations/2026-11-04-official-records'
dest=root/'migration-2026-11-04'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def info(p):
    st=p.stat()
    return {'workspace_path':p.relative_to(base).as_posix(),'bytes':st.st_size,'sha256':sha(p),'mtime_ns':st.st_mtime_ns,'mtime_utc':datetime.fromtimestamp(st.st_mtime,timezone.utc).isoformat()}
assert subprocess.check_output(['git','-C',str(repo),'branch','--show-current']).decode().strip()=='research/bleich-local-migration-2026-11-04'
assert not (dest/'inventory.json').exists(),'Already inventoried; do not overwrite the original snapshot'
original=sorted(p for p in root.rglob('*') if p.is_file() and dest not in p.parents)
known={}
rows=[]
for p in original:
    x=info(p);x.update(action='already_in_research',destination=p.relative_to(root).as_posix())
    rows.append(x);known.setdefault(x['sha256'],x['destination'])
cache_map={
'work/inferent-adv-cache/IA_ADV_Base_A_20111105_20241231.csv':'continuation-3/inferent/raw/IA_ADV_Base_A_20111105_20241231.zip-member.bin',
'work/employment-round2/schedule-cache/IA_Schedule_A_B_20111105_20241231.csv':'continuation-3/employment/raw/IA_Schedule_A_B_20111105_20241231.csv.zip-member.bin',
'work/round4-era-cache/ERA_ADV_Base_20111105_20241231.csv':'continuation-4/entrypoint-history/raw/ERA_ADV_Base_20111105_20241231.csv.zip-member.bin',
'work/round4-era-cache/ERA_Schedule_A_B_20111105_20241231.csv':'continuation-4/entrypoint-history/raw/ERA_Schedule_A_B_20111105_20241231.csv.zip-member.bin'}
external=sorted(p for top in ['work','.playwright-mcp','outputs'] for p in (base/top).rglob('*') if p.is_file() and repo not in p.parents)
for p in external:
    assert not p.is_symlink(),str(p)
    x=info(p);rel=x['workspace_path']
    if rel in cache_map:
        compressed=root/cache_map[rel]
        with compressed.open('rb') as f:
            header=f.read(30)
            sig,version,flags,method,mt,md,crc,cs,us,nl,el=struct.unpack('<IHHHHHIIIHH',header)
            assert sig==0x04034b50 and method==8
            f.read(nl+el)
            de=zlib.decompressobj(-15);h=hashlib.sha256();size=0
            for c in iter(lambda:f.read(1024*1024),b''):
                out=de.decompress(c);h.update(out);size+=len(out)
            out=de.flush();h.update(out);size+=len(out)
            assert de.eof and h.hexdigest()==x['sha256'] and size==x['bytes'],rel
        x.update(action='excluded_reproducible_cache',reconstruct_from=cache_map[rel],reconstruction='ZIP local header: skip 30 + filename length + extra length bytes; raw DEFLATE (zlib wbits=-15); verified complete output SHA256 and size',compressed_sha256=sha(compressed))
    elif x['sha256'] in known:
        x.update(action='excluded_exact_duplicate',duplicate_of=known[x['sha256']])
    else:
        target=dest/'local-support'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(p,target)
        assert sha(target)==x['sha256'] and target.stat().st_mtime_ns==x['mtime_ns']
        x.update(action='imported_unique_support',destination=target.relative_to(root).as_posix())
        known[x['sha256']]=x['destination']
    rows.append(x)
counts=Counter(x['action'] for x in rows)
obj={'created_at_utc':datetime.now(timezone.utc).isoformat(),'workspace':str(base),'source_commit':'96a6bc2becc90d026dcaafce6490fc76798738e4','branch':'research/bleich-local-migration-2026-11-04','root':'investigations/2026-11-04-official-records','protected_refs':{'main':'0e4126ee10bfeeb0257a75a524e8108694a1c0bc','research/bleich-official-records-2026-11-04':'96a6bc2becc90d026dcaafce6490fc76798738e4'},'policy':'All original local files retained; archive is historical supporting work, not current report authority. Original mtime is metadata: Git preserves bytes, not filesystem timestamps. Browser logs are access diagnostics, not official evidence.','counts':dict(counts),'files':rows}
dest.mkdir(exist_ok=True)
(dest/'inventory.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'counts':dict(counts),'inventoried_bytes':sum(x['bytes'] for x in rows),'imported_bytes':sum(x['bytes'] for x in rows if x['action']=='imported_unique_support'),'excluded_bytes':sum(x['bytes'] for x in rows if x['action'].startswith('excluded'))},indent=2))

