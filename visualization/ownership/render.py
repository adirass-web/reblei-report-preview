from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'.runtime/python'))
import fitz,xml.etree.ElementTree as E,json,re
p=Path(__file__).resolve().parent; results=[]
D=json.loads((p/'data.json').read_text(encoding='utf-8'));required={e['claim_id'] for s in D['snapshots'] for e in s['edges']}|{'SEC-C006'}
for v in 'abc':
 f=p/f'ownership-{v}.svg';root=E.fromstring(f.read_text(encoding='utf-8'));w,h=float(root.get('width')),float(root.get('height'))
 ids=[el.get('id') for el in root.iter() if el.get('id')];assert len(ids)==len(set(ids)),f'duplicate SVG ID {v}'
 doc=fitz.open(stream=f.read_bytes(),filetype='svg'); original=fitz.open('pdf',doc.convert_to_pdf())
 original[0].get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).save(p/f'ownership-{v}.png')
 # Preserve all content while using a convenient common large-format print width.
 scale=1684/w;pdf=fitz.open();page=pdf.new_page(width=w*scale,height=h*scale);page.show_pdf_page(page.rect,original,0)
 pdf.save(p/f'ownership-{v}.pdf')
 spans=[s for b in page.get_text('dict')['blocks'] if 'lines'in b for l in b['lines'] for s in l['spans']]
 outside=[s['text'] for s in spans if not page.rect.contains(fitz.Rect(s['bbox']))]
 smallest=min(s['size'] for s in spans);missing=sorted(required-set(re.findall(r'(?:ID|SEC)-C\d+',page.get_text())))
 assert not outside,outside;assert smallest>=10,smallest;assert not missing,missing
 results.append({'file':f.name,'svg_size':[w,h],'pdf_points':[page.rect.width,page.rect.height],'min_pdf_font_pt':round(smallest,2),'text_outside_page':outside,'missing_claim_ids':missing,'svg_ids_unique':True})
(p/'render-check.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2))
