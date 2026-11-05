import fitz,pathlib
base=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/litigation/raw');d=fitz.open(base/'nasdaq-wedbush-20100243866-02.pdf');print('AWC physical pages',len(d))
for i in [0,2,3,7,8,9,10,11]:
 print('\nPHYSICAL PAGE',i+1);print(d[i].get_text())
 if i in [0,2,3,7,8,11]:d[i].get_pixmap(matrix=fitz.Matrix(1,1)).save('work/employment-round2/awc-page'+str(i+1)+'.png')
