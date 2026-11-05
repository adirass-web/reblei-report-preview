import fitz
p='outputs/ReBlei/investigations/2026-11-04-official-records/evidence/id-sec-ophir-164729-adv.pdf';d=fitz.open(p)
for i in [18,19]:d[i].get_pixmap(matrix=fitz.Matrix(1,1)).save('work/employment-round2/ophir-page'+str(i+1)+'.png')
