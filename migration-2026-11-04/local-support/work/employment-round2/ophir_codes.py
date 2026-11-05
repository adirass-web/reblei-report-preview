import fitz,pathlib
p=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/evidence/id-sec-ophir-164729-adv.pdf');d=fitz.open(p)
for i,pg in enumerate(d):
 s=pg.get_text()
 if '75%' in s or '50% to' in s or 'Ownership Codes' in s:print('PHYSICAL',i+1,s[s.find('Ownership Codes')-200:s.find('Ownership Codes')+1800] if 'Ownership Codes' in s else s[-2600:])
