import fitz,pathlib
for fn in ['id-finra-scout-151990.pdf','evt-finra-may2016-disciplinary.pdf']:
 d=fitz.open(pathlib.Path('evidence')/fn)
 for i,p in enumerate(d):
  t=p.get_text();low=t.lower()
  if ('wedbush' in low and fn.startswith('id-')) or ('scout' in low and 'may2016' in fn):
   print(fn,'PAGE',i+1,t[:8500])
