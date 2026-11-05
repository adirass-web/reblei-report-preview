from pathlib import Path
import fitz,re
root=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records\continuation-3\ownership\raw')
for p in sorted(root.glob('*.pdf')):
 d=fitz.open(p); print('\nFILE',p.name,'pages',len(d))
 for i,pg in enumerate(d):
  t=' '.join(pg.get_text().split())
  if any(x in t.lower() for x in ['wholly','finch','nays','meb','management fee','subordinat','oath or','nature of business','litigation']): print('PAGE',i+1, t[:4800])
