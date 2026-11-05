from pathlib import Path
p=Path('work/build_index.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("for r in read('financial-sources.json',[]):raws.append(('financial',r))","for r in read('financial-sources.json',[]):raws.append(('financial',r))\ncorp=read('corporate-sources.json',{})\nfor r in corp.get('sources',[]):raws.append(('corporate',r))")
s=s.replace("# Identifier assignments are source-linked; ambiguity is not silently collapsed.","""for x in corp.get('claims',[]):
 loc='API response row '+str(x['response_row_one_based']) if x.get('response_row_one_based') else 'physical PDF pages '+','.join(map(str,x.get('physical_pdf_pages',[])))
 claim(x['id'],x['claim'],x['status'],x['source_id'],loc,None,x)
# Identifier assignments are source-linked; ambiguity is not silently collapsed.""")
s=s.replace("financial=read('financial-observations.json',{})","""financial=read('financial-observations.json',[])
claim('FIN-UNIT-001','SEC Form13F instructions require information-table values rounded to nearest dollar; amendments identify restatement or new-holdings treatment.','official_instruction','FIN-13F-INSTRUCTIONS','physical PDF pp6,13',None)
for x in financial:
 if x.get('observation_type')!='13F_cover_summary':continue
 cid=x['observation_id'];status=x.get('status','as_filed')
 if not x.get('usable_for_comparison',True):status+='; quarantined_or_amendment_not_standalone'
 statement=f"EntryPoint {x['form']} accession {x['accession_id']} period {x['measurement_date']} cover reports tableEntryTotal {x['table_entry_total']} and tableValueTotal {x['table_value_total_raw']} USD; amendment type {x.get('amendment_type')}. Preserve as filed; limitations and reconciliation are in claim metadata."
 claim(cid,statement,status,x['document_id'],x['locator'],'E003',x)
 fin('E003',x['metric'],x['table_value_total_raw'],'nearest_dollars',cid,x['measurement_date'],'13F cover as filed; not RAUM/NAV; check claim metadata usable_for_comparison',filing_date=x['filing_date'],status=status)
 fin('E003','13F_cover_entry_count',x['table_entry_total'],'entries',cid,x['measurement_date'],'raw cover field, not independently confirmed holdings count',currency=None,filing_date=x['filing_date'],status=status)
 if x['accession_id']=='0001992519-24-000008':
  fin('E003','13F_information_table_recomputed_value_sum','175789004','nearest_dollars',cid,x['measurement_date'],'derived sum independently reproduced; does not correct original cover',filing_date=x['filing_date'],status='derived_reconciliation_quarantined')
  fin('E003','13F_information_table_recomputed_entry_count','594','entries',cid,x['measurement_date'],'derived row count independently reproduced',currency=None,filing_date=x['filing_date'],status='derived_reconciliation_quarantined')
""")
s=s.replace("for owner,logs in [('identity',ident.get('search_logs',[])),('events',evt.get('search_logs',[]))]:","for owner,logs in [('identity',ident.get('search_logs',[])),('events',evt.get('search_logs',[])),('corporate',corp.get('search_logs',[])),('financial',read('financial-search-log.json',[]))]:")
s=s.replace("query=x.get('query') or x.get('url')","query=x.get('query') if isinstance(x.get('query'),str) else json.dumps(x.get('queries') or x.get('query') or x.get('url'))")
s=s.replace("result=x.get('result'),coverage_limit=","result=x.get('result') if isinstance(x.get('result'),str) else json.dumps(x.get('result') or x.get('note')),coverage_limit=")
s=s.replace("# Explicit relational schema, with references enforcing ownership of evidence and identity.","""add('conflicts',conflict_id='X-13F-2024Q3',topic='13F original cover versus information-table values',status='unresolved_quarantined',resolution='0001992519-24-000008 cover entryTotal175789/valueTotal594; information table594 entries sum175789004 USD. Preserve raw and derived values separately; cause unknown, no silent correction.')
add('conflict_claims',conflict_id='X-13F-2024Q3',claim_id='FIN-13F-0001992519-24-000008')
# Explicit relational schema, with references enforcing ownership of evidence and identity.""")
p.write_text(s,encoding='utf8')
