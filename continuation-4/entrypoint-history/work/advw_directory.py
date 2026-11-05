from pathlib import Path
import sys,struct,json
r=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records');o=r/'continuation-4/entrypoint-history/raw';sys.path.insert(0,str(r/'continuation-3/inferent'));sys.dont_write_bytecode=True
from range_zip import fetch_range
url='https://www.sec.gov/files/advw-20001019-20241231.zip'
try:
 b,l=fetch_range(url,'bytes=-22',o,'advw-eocd');assert b[:4]==b'PK\x05\x06';size,offset=struct.unpack_from('<II',b,12)
 b,l=fetch_range(url,f'bytes={offset}-{offset+size-1}',o,'advw-directory');pos=0;out=[]
 while pos<len(b) and b[pos:pos+4]==b'PK\x01\x02':
  h=struct.unpack_from('<4s6H3I5H2I',b,pos);nl,el,cl=h[10:13];name=b[pos+46:pos+46+nl].decode('utf-8');out.append(dict(member=name,compressed_size=h[8],uncompressed_size=h[9],method=h[4],crc32=h[7],offset=h[-1]));pos+=46+nl+el+cl
 (o/'advw-entries.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print([(x['member'],x['compressed_size']) for x in out])
except Exception as e: print(str(e)[:1500])
