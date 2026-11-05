import requests,struct,zlib,hashlib,json,datetime,pathlib

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def fetch_range(url, spec, out, label):
    out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    log={'url':url,'requested_range':spec,'started_at_utc':utc()}
    try:
        with requests.get(url,headers={'User-Agent':'Public-record research research@example.org','Range':spec},timeout=(10,25),stream=True) as r:
            log.update(http_status=r.status_code,headers=dict(r.headers))
            if r.status_code!=206: raise ValueError('Range not honored; full response not downloaded')
            data=r.content
            if len(data)>4000000: raise ValueError('Range exceeds bounded artifact size')
            f=out/(label+'.bin');f.write_bytes(data)
            log.update(file=str(f),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),completed_at_utc=utc())
    except Exception as e:
        log.update(error=str(e),completed_at_utc=utc());data=None
    (out/(label+'.request.json')).write_text(json.dumps(log,indent=2),encoding='utf-8')
    if data is None: raise RuntimeError(log)
    return data,log

def directory(url,out,label):
    tail,tlog=fetch_range(url,'bytes=-65536',out,label+'-tail')
    e=tail.rfind(b'PK\x05\x06')
    if e<0: raise ValueError('No ZIP end-directory record')
    size,offset=struct.unpack_from('<II',tail,e+12)
    if size>4000000: raise ValueError('Central directory exceeds bound')
    data,dlog=fetch_range(url,f'bytes={offset}-{offset+size-1}',out,label+'-directory')
    entries=[];pos=0
    while pos<len(data) and data[pos:pos+4]==b'PK\x01\x02':
        h=struct.unpack_from('<4s6H3I5H2I',data,pos);nl,el,cl=h[10:13]
        name=data[pos+46:pos+46+nl].decode('utf-8')
        entries.append(dict(member=name,compressed_size=h[8],uncompressed_size=h[9],method=h[4],crc32=h[7],offset=h[-1]))
        pos+=46+nl+el+cl
    return entries,[tlog,dlog]

def member(url,item,out,label):
    off=item['offset'];hdr,hlog=fetch_range(url,f'bytes={off}-{off+29}',out,label+'-header')
    h=struct.unpack('<4s5H3I2H',hdr);skip=30+h[-2]+h[-1];length=skip+item['compressed_size']
    data,log=fetch_range(url,f'bytes={off}-{off+length-1}',out,label+'-member')
    if item['method']==8: payload=zlib.decompress(data[skip:],-15)
    elif item['method']==0: payload=data[skip:]
    else: raise ValueError('Unsupported compression method')
    assert len(payload)==item['uncompressed_size']
    assert zlib.crc32(payload)&0xffffffff==item['crc32']
    path=pathlib.Path(out)/pathlib.Path(item['member']).name;path.write_bytes(payload)
    return path,[hlog,log]
