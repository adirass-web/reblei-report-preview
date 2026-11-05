import fitz,pathlib
p=pathlib.Path('work/employment-round2');d=fitz.open('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-2/litigation/raw/finra-award-15-02816.pdf')
for i in [1,2,4,5,6]:d[i].get_pixmap(matrix=fitz.Matrix(1,1)).save(str(p/f'award-page{i+1}.png'))
