import requests,struct,zlib,json,hashlib,pathlib,datetime,concurrent.futures,csv
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-3/employment';out=base/'raw';work=pathlib.Path('work/employment-round2');chunkdir=work/'schedule-chunks';chunkdir.mkdir(exist_ok=True)
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
cat=json.loads((root/'continuation-3/inferent/part1bulk-directory.json').read_text());url=cat['url'];e=next(x for x in cat['entries'] if x['member'].endswith('/IA_Schedule_A_B_20111105_20241231.csv'));off=e['offset'];logs=[]
def fetch(lo,hi,label):
 t=utc();r=requests.get(url,headers={'Range':f'bytes={lo}-{hi}','User-Agent':'Public professional-record research'},timeout=(10,35));d=r.content;log=dict(url=url,requested_range=f'bytes={lo}-{hi}',started_at_utc=t,completed_at_utc=utc(),http_status=r.status_code,response_headers=dict(r.headers),bytes=len(d),sha256=hashlib.sha256(d).hexdigest())
 if r.status_code!=206 or len(d)!=hi-lo+1:raise RuntimeError(log)
 p=chunkdir/(label+'.bin');p.write_bytes(d);log['scratch_file']=str(p);return p,log
try:
 hp,hl=fetch(off,off+29,'header');h=struct.unpack('<4s5H3I2H',hp.read_bytes());assert h[0]==b'PK\x03\x04';skip=30+h[-2]+h[-1];length=skip+e['compressed_size'];ranges=[(off+i,min(off+i+1999999,off+length-1),'chunk-'+str(i//2000000).zfill(3)) for i in range(0,length,2000000)]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:parts=list(ex.map(lambda a:fetch(*a),ranges))
 logs=[hl]+[x[1] for x in parts];payload=b''.join(p.read_bytes() for p,l in parts);assert len(payload)==length
 original=out/'EMP4-OPHIR-SCHEDULE-AB.zip-member.bin';original.write_bytes(payload)
 data=zlib.decompress(payload[skip:],-15);assert len(data)==e['uncompressed_size'];assert zlib.crc32(data)&0xffffffff==e['crc32'];expanded=work/'IA_Schedule_A_B_20111105_20241231.csv';expanded.write_bytes(data)
 result=dict(url=url,member=e,local_header_size=skip,original_member_file=original.relative_to(root).as_posix(),original_member_sha256=hashlib.sha256(payload).hexdigest(),compressed_deflate_sha256=hashlib.sha256(payload[skip:]).hexdigest(),uncompressed_sha256=hashlib.sha256(data).hexdigest(),uncompressed_size_verified=True,crc32_verified=True,expanded_cache=str(expanded),completed_at_utc=utc(),requests=logs)
 (base/'schedule-ab-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='requests'},indent=2));print('CSV header',next(csv.reader(expanded.open(encoding='utf-8-sig',newline=''))))
except Exception as error:
 (base/'schedule-ab-failure.json').write_text(json.dumps(dict(error=str(error),requests=logs,logged_at_utc=utc()),indent=2),encoding='utf-8');raise
