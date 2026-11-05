from pathlib import Path
import fitz,re
root=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records\continuation-3\ownership\raw')
for p in sorted(root.glob('*.pdf')):
 d=fitz.open(p);print('\nFILE',p.name)
 for i,pg in enumerate(d):
  t=' '.join(pg.get_text().split())
  for m in re.finditer(r'Finch|NAYS|MEB|management agreement|litigation|repaid|wholly',t,re.I): print('PAGE',i+1,t[max(0,m.start()-150):m.end()+400])
for name,pgs in [('scout2009-annual',[1,2,10]),('scout2013-annual',[2,7,11]),('scout-2012-X-17A-5',[6])]:
 d=fitz.open(root/(name+'.pdf'))
 for pg in pgs:d[pg-1].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(root/(name+'-page'+str(pg)+'.png'))
