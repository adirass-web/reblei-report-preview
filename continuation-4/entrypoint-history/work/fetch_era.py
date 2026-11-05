from pathlib import Path
import sys,json,struct,hashlib
r=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records');o=r/'continuation-4/entrypoint-history';sys.path.insert(0,str(r/'continuation-3/inferent'));sys.dont_write_bytecode=True
from chunk_member import retrieve
entries=json.loads((o/'raw/part1bulk-entries.json').read_text(encoding='utf-8'));url='https://www.sec.gov/files/adv-filing-data-20111105-20241231-part1.zip'
cache=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\work\round4-era-cache')
for prefix,label in [('ERA_ADV_Base_','era-base'),('ERA_Schedule_A_B_','era-schedule-ab')]:
 item=next(x for x in entries if Path(x['member']).name.startswith(prefix));p,m=retrieve(url,item,o/'raw',cache,label,workers=4)
 raw=Path(m['compressed_member_file']).read_bytes();hdr=struct.unpack('<4s5H3I2H',raw[:30]);name=raw[30:30+hdr[-2]].decode('utf-8');assert name==item['member'];m['local_central_names_equal']=True;m['local_header_member']=name
 (o/'raw'/(label+'-verification.json')).write_text(json.dumps(m,indent=2),encoding='utf-8');print(label,'verified',p,len(raw),flush=True)
