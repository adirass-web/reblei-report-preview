from pathlib import Path
import fitz
base=Path('outputs/ReBlei/investigations/2026-11-04-official-records')
for f,pages in [('continuation-2/litigation/raw/finra-award-15-02816.pdf',None),('evidence/id-finra-scout-151990.pdf',[13]),('evidence/evt-finra-may2016-disciplinary.pdf',[41,42])]:
 r=fitz.open(base/f);print('\nDOCUMENT',f,'PAGES',len(r))
 for i in range(len(r)) if pages is None else pages:
  print('\nPHYSICAL PAGE',i+1);print(r[i].get_text())

