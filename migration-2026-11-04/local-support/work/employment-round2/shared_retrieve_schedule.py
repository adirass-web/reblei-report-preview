import sys,pathlib,json,csv
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');shared=root/'continuation-3/inferent';sys.path.insert(0,str(shared.resolve()));from chunk_member import retrieve
cat=json.loads((shared/'part1bulk-directory.json').read_text());e=next(x for x in cat['entries'] if x['member'].endswith('/IA_Schedule_A_B_20111105_20241231.csv'))
p,m=retrieve(cat['url'],e,root/'continuation-3/employment/raw',pathlib.Path('work/employment-round2/schedule-cache'),'EMP4-SCHEDULE-AB',workers=3)
print('Recovered',p,m['uncompressed_sha256'],m['crc32_verified']);print(next(csv.reader(p.open(encoding='utf-8-sig',newline=''))))
