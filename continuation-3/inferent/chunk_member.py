"""Reusable bounded-chunk ZIP member fetch. Import and call retrieve().

Uses range_zip.fetch_range; preserves exact compressed member, request logs,
CRC/size/hash metadata, and puts expanded original only in explicit cache_dir.
"""
import pathlib,json,struct,concurrent.futures,zlib,hashlib
from range_zip import fetch_range,utc

def retrieve(url,item,out_dir,cache_dir,label,workers=4):
    out_dir=pathlib.Path(out_dir);cache_dir=pathlib.Path(cache_dir)
    out_dir.mkdir(parents=True,exist_ok=True);cache_dir.mkdir(parents=True,exist_ok=True)
    off=item['offset'];header,hl=fetch_range(url,f'bytes={off}-{off+29}',out_dir,label+'-header')
    h=struct.unpack('<4s5H3I2H',header);skip=30+h[-2]+h[-1]
    total=skip+item['compressed_size'];jobs=[(i,start,min(start+2000000,total)) for i,start in enumerate(range(0,total,2000000))]
    def job(v):
        i,start,end=v;fn=out_dir/f'{label}-chunk-{i:03d}.bin';log=fn.with_suffix('.request.json')
        if fn.exists() and log.exists():return json.loads(log.read_text())
        _,request=fetch_range(url,f'bytes={off+start}-{off+end-1}',out_dir,f'{label}-chunk-{i:03d}')
        return request
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:logs=list(ex.map(job,jobs))
    compressed=out_dir/(pathlib.Path(item['member']).name+'.zip-member.bin')
    with compressed.open('wb') as dst:
        for i,_,_ in jobs:dst.write((out_dir/f'{label}-chunk-{i:03d}.bin').read_bytes())
    expanded=cache_dir/pathlib.Path(item['member']).name;dec=zlib.decompressobj(-15);crc=0;size=0;sha=hashlib.sha256()
    with compressed.open('rb') as src,expanded.open('wb') as dst:
        src.read(skip)
        while b:=src.read(2000000):
            data=dec.decompress(b);dst.write(data);crc=zlib.crc32(data,crc);size+=len(data);sha.update(data)
        data=dec.flush();dst.write(data);crc=zlib.crc32(data,crc);size+=len(data);sha.update(data)
    assert dec.eof and crc&0xffffffff==item['crc32'] and size==item['uncompressed_size']
    for i,start,end in jobs:
        fn=out_dir/f'{label}-chunk-{i:03d}.bin';jf=fn.with_suffix('.request.json');log=json.loads(jf.read_text())
        log.update(preserved_as_compressed_member=compressed.name,member_byte_start=start,member_byte_end=end-1,original_range_chunk_replaced_by_exact_member_slice=True)
        jf.write_text(json.dumps(log,indent=2));fn.unlink()
    meta=dict(url=url,member=item,requests=[hl]+logs,crc32_verified=True,uncompressed_size_verified=True,uncompressed_sha256=sha.hexdigest(),compressed_member_file=str(compressed),compressed_member_sha256=hashlib.sha256(compressed.read_bytes()).hexdigest(),expanded_cache_path=str(expanded),completed_at_utc=utc())
    (out_dir/(label+'-verification.json')).write_text(json.dumps(meta,indent=2))
    return expanded,meta
