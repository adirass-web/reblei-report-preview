import fitz,pathlib
base=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');out=pathlib.Path('work/employment-round2')
for f,nums,tag in [('evidence/id-finra-scout-151990.pdf',[13],'scout'),('evidence/evt-finra-may2016-disciplinary.pdf',[41,42],'bulletin')]:
 d=fitz.open(base/f)
 for i in nums:d[i].get_pixmap(matrix=fitz.Matrix(1,1)).save(str(out/f'{tag}-page{i+1}.png'))
