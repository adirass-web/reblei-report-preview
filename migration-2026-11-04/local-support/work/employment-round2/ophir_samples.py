import pathlib,json,concurrent.futures,urllib.parse
from bs4 import BeautifulSoup
from range_zip import directory
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-3/employment';out=base/'raw'
s=BeautifulSoup((root/'continuation-2/inferent/raw/part2-archive.html').read_bytes(),'html.parser')
links=[(a.get_text(' ',strip=True),urllib.parse.urljoin('https://www.sec.gov',a['href'])) for a in s.find_all('a',href=True) if any(z in a.get_text() for z in ['ADV Brochures 2015','ADV Brochures 2016'])]
items=[links[0],links[1],links[3],next(x for x in links if '2016 1 of' in x[0]),next(x for x in links if '2016 3 of' in x[0])]
def go(t):
 label='EMP4-SAMPLE-'+str(items.index(t)+1)
 try:
  entries,logs=directory(t[1],out,label);matches=[e for e in entries if '164729' in e['member'] or '247246' in e['member']];rs=dict(label=label,url=t[1],title=t[0],entries=len(entries),matches=matches,requests=logs);print(label,len(entries),matches,flush=True)
 except Exception as e:rs=dict(label=label,url=t[1],title=t[0],error=str(e));print(label,'FAIL',str(e)[:150],flush=True)
 (base/(label+'-inventory.json')).write_text(json.dumps(rs,indent=2),encoding='utf-8');return rs
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:r=list(ex.map(go,items))
(base/'inventory-2015-2016-sample.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
