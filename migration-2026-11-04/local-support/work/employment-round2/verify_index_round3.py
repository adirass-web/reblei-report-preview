import json,pathlib,sqlite3,hashlib,collections,fitz
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records').resolve();ip=root/'evidence-index.json';sp=root/'evidence-index.sqlite';a=json.loads(ip.read_text(encoding='utf-8-sig'));t=a['tables'];out=dict(generated_at_utc=a['generated_at_utc'],index_sha256=hashlib.sha256(ip.read_bytes()).hexdigest(),sqlite_sha256=hashlib.sha256(sp.read_bytes()).hexdigest(),counts={k:len(v) for k,v in t.items()})
def freeze(v):
 if isinstance(v,dict):return tuple(sorted((k,freeze(x)) for k,x in v.items()))
 if isinstance(v,list):return tuple(freeze(x) for x in v)
 return v
def rowkey(r):
 d=dict(r)
 for k,v in d.items():
  if k.endswith('_json') and v is not None:d[k]=json.loads(v) if isinstance(v,str) else v
 return freeze(d)
c=sqlite3.connect('file:'+sp.as_posix()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
out['integrity_check']=[tuple(r) for r in c.execute('pragma integrity_check')];out['foreign_key_check']=[tuple(r) for r in c.execute('pragma foreign_key_check')];out['table_comparison']={}
for name,rows in t.items():
 sql=[dict(r) for r in c.execute('select * from "'+name+'"')];left=collections.Counter(rowkey(r) for r in rows);right=collections.Counter(rowkey(r) for r in sql);out['table_comparison'][name]=dict(json_rows=len(rows),sqlite_rows=len(sql),equal=left==right)
c.close();bad=[];pdfbad=[];within=0
for d in t['documents']:
 p=(root/d['file_path']).resolve()
 if not p.is_relative_to(root):bad.append(dict(document_id=d['document_id'],reason='outside investigationroot',file=str(p)));continue
 within+=1
 if not p.is_file():bad.append(dict(document_id=d['document_id'],reason='missing',file=str(p)));continue
 sh=hashlib.sha256(p.read_bytes()).hexdigest()
 if sh!=d['sha256']:bad.append(dict(document_id=d['document_id'],reason='hash mismatch',actual=sh,expected=d['sha256']))
 if d.get('pdf_pages') is not None and p.suffix.lower()=='.pdf':
  doc=fitz.open(p)
  if len(doc)!=d['pdf_pages']:pdfbad.append(dict(document_id=d['document_id'],actual=len(doc),recorded=d['pdf_pages']))
out['documents_within_investigation_root']=within;out['document_hash_errors']=bad;out['pdf_page_count_errors']=pdfbad
validation=json.loads((root/'validation.json').read_text(encoding='utf-8-sig'));out['validation_counts_equal']=validation['table_counts']==out['counts'];out['all_pass']=not bad and not pdfbad and all(x['equal'] for x in out['table_comparison'].values()) and not out['foreign_key_check'] and out['integrity_check']==[('ok',)] and out['validation_counts_equal']
p=pathlib.Path('work/employment-round2/index-qa-check.json');p.write_text(json.dumps(out,indent=2),encoding='utf-8');print(json.dumps(out,indent=2))
