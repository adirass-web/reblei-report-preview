"""Reconstruct the original SEC CSV from the exact preserved ZIP member.

Usage: python reconstruct_base_a.py OUTPUT_CSV
Use a work/cache path for OUTPUT_CSV; the expanded original is 533MB.
"""
import pathlib,struct,zlib,hashlib,json,sys

def reconstruct(member,output,metadata):
    dec=zlib.decompressobj(-15);crc=0;size=0;sha=hashlib.sha256()
    with pathlib.Path(member).open('rb') as src:
        header=src.read(30);h=struct.unpack('<4s5H3I2H',header)
        assert h[0]==b'PK\x03\x04' and h[3]==8
        src.read(h[-2]+h[-1])
        with pathlib.Path(output).open('wb') as dst:
            while b:=src.read(2000000):
                data=dec.decompress(b);dst.write(data);crc=zlib.crc32(data,crc);size+=len(data);sha.update(data)
            data=dec.flush();dst.write(data);crc=zlib.crc32(data,crc);size+=len(data);sha.update(data)
    assert dec.eof and size==metadata['member']['uncompressed_size']
    assert crc&0xffffffff==metadata['member']['crc32']
    assert sha.hexdigest()==metadata['uncompressed_sha256']
    return {'bytes':size,'sha256':sha.hexdigest(),'crc32':crc&0xffffffff}

if __name__=='__main__':
    here=pathlib.Path(__file__).resolve().parent
    meta=json.loads((here/'base-a-verification.json').read_text())
    print(json.dumps(reconstruct(here/meta['compressed_member_file'],sys.argv[1],meta),indent=2))
