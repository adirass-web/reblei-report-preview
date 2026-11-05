import pathlib,json,sqlite3,csv,hashlib,datetime,re,sys
ROOT=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path('outputs')
NOW=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(n,default=None):
 p=ROOT/n
 return json.loads(p.read_text(encoding='utf-8-sig')) if p.exists() else default
ident=read('identity-sources.json',{});sec=read('sec-sources.json',[]);sc=read('sec-claims.json',[]);evt=read('events-sources.json',{});par=read('parent-sources.json',[])
data={k:[] for k in ['subjects','persons','entities','identifiers','documents','document_aliases','claims','claim_evidence','roles','relationships','financial_observations','events','event_claims','search_logs','conflicts','conflict_claims','retrieval_attempts']}
def add(k,**r):data[k].append(r);return r
names={}
def person(i,n,crd=None,status='confirmed_subject',note=''):
 add('subjects',subject_id=i,kind='person',display_name=n);add('persons',person_id=i,legal_name=n,crd=crd,identity_status=status,note=note);names[n]=i
person('P001','Michael Edward Bleich','4262671');person('P002','Keith Michael Bleich','2372764','excluded_name_collision','Excluded by mandate; no personal sanctions attributed to P001 from this identity.')
for i,n,crd in [('P003','Dror Niv',None),('P004','Lawrence Edward Leibowitz','2024745'),('P005','Andrew Louis Alkon','5079758')]:person(i,n,crd,'documented_professional_counterparty')
entities=[('E001','Scout Trading, LLC','broker-dealer','Delaware','confirmed',''),('E002','Ophir Partners LLC','investment adviser',None,'confirmed',''),('E003','EntryPoint Capital, LLC','investment adviser','Delaware','confirmed',''),('E004','MEB NY INC','ownership intermediary',None,'confirmed_filing_name','Corporate registry candidate is kept separately; name-only correspondence is not unique identity proof.'),('E005','Finch LLC','ownership intermediary',None,'confirmed_filing_name',''),('E006','NAYS LLC','ownership intermediary',None,'confirmed_filing_name',''),('E007','Ophir Partners Master Fund Ltd','fund','Cayman Islands','confirmed',''),('E008','OPHIR PARTNERS BEAUFORT FUND LP','fund',None,'ambiguous_identifier','Two private-fund IDs retained as ambiguous disclosed identifiers; no assertion they are one legal vehicle.'),('E009','OPHIR PARTNERS BEAUFORT GP, LLC','general partner',None,'confirmed_filing_name',''),('E010','EntryPoint Partners, LP','ownership intermediary',None,'confirmed_filing_name',''),('E011','EntryPoint GP LLC','ownership intermediary',None,'confirmed_filing_name','Distinct from EP Fund GP LLC.'),('E012','EP Fund GP, LLC','fund general partner',None,'confirmed_filing_name','Distinct from EntryPoint GP LLC.'),('E013','EP Third Moment Master Fund, LP','master fund','Cayman Islands','confirmed',''),('E014','EP Third Moment Fund, LLC','feeder fund','Delaware','confirmed','Former name EP Healthcare Transformation Fund, LLC in official Forms D.'),('E015','EP Third Moment International, LP','feeder fund; legal-form conflict','Cayman Islands','confirmed','Name and brochures say LP; Form D entityType says Corporation. Legal form unresolved.'),('E016','Walleye Opportunities Master Fund Ltd','private fund',None,'confirmed_reporting_connection','No personal Bleich ownership, employment or control inferred.'),('E017','Walleye Capital LLC','other reporting adviser',None,'confirmed_reporting_connection',''),('E018','Richard A. Desich Irrevocable 2005 SD Trust','ownership trust',None,'confirmed_filing_name','Professional ownership chain only.'),('E019','South Dakota Trust Company','trustee',None,'confirmed_filing_name',''),('E020','Wedbush Securities Inc','clearing broker',None,'related_event_only','Separate respondent and penalty; not Bleich personal liability.'),('E021','Inferent Capital, LLC','investment adviser',None,'candidate_subject_affiliation','Official entity CRD292027/SEC801-112741 exists; preserved March2019 ADV has no Bleich text. Subject role is not officially confirmed.'),('E022','Lehman Brothers','employer legal entity unresolved',None,'career_lead_only','Exchange-hosted corporate release names Michael Bleich; CRD/legal employer chain incomplete.'),('E023','Barclays','employer legal entity unresolved',None,'career_lead_only','Third-party professional-history lead only.'),('E024','Chase Manhattan Bank','employer legal entity unresolved',None,'career_lead_only','Third-party professional-history lead only.'),('E025','INFERENT QE, LLC','fund manager/GP',None,'candidate_branch','Official Inferent structure; no confirmed Bleich affiliation.'),('E026','INFERENT PLENARY FUND LP','fund','Delaware','candidate_branch',''),('E027','INFERENT QE MASTER FUND, LP','fund',None,'candidate_branch',''),('E028','INFERENT QE FUND INTERNATIONAL, LP','fund',None,'candidate_branch',''),('E029','INFERENT QE FUND, LLC','fund',None,'candidate_branch',''),('E030','INFERENT ADVISORY HOLDINGS, LP','ownership intermediary',None,'candidate_branch',''),('E031','REFLEXIVE, LLC','ownership intermediary',None,'candidate_branch','')]
for i,n,t,j,s,note in entities:add('subjects',subject_id=i,kind='entity',display_name=n);add('entities',entity_id=i,legal_name=n,entity_type=t,jurisdiction=j,inclusion_status=s,note=note);names[n]=i
# Each byte representation has one canonical document row; repeated specialist references are aliases.
docmap={};hashmap={}
def normpath(s):
 if not s:return None
 s=s.replace('\\','/')
 if s.startswith('outputs/'):s=s[8:]
 return s
raws=[]
for r in ident.get('sources',[]):raws.append(('identity',r))
for r in sec:raws.append(('sec',r))
for r in evt.get('sources',[]):raws.append(('events',r))
for r in par:raws.append(('parent',r))
for r in read('financial-sources.json',[]):raws.append(('financial',r))
corp=read('corporate-sources.json',{})
for r in corp.get('sources',[]):raws.append(('corporate',r))
for r in raws:
 owner,x=r;old=x.get('document_id') or x.get('id') or x.get('filename');f=normpath(x.get('file') or ('evidence/'+x['filename'] if x.get('sha256') and x.get('filename') else None));sha=x.get('sha256');ok=bool(f and sha and (ROOT/f).exists())
 a_id='ACQ-'+str(len(data['retrieval_attempts'])+1).zfill(4)
 if ok:
  actual=hashlib.sha256((ROOT/f).read_bytes()).hexdigest();assert actual.lower()==sha.lower(),(old,'hash mismatch');sha=sha.lower()
  docid=hashmap.get(sha)
  if not docid:
   docid=old or 'DOC-'+str(len(data['documents'])+1).zfill(3);hashmap[sha]=docid
   u=x.get('url','');authority=x.get('authority') or ('SEC' if 'sec.gov' in u else 'FINRA' if 'finra.org' in u else 'Cboe' if 'cboe' in u else 'New York State open data' if 'ny.gov' in u else None)
   source_class=x.get('source_class') or x.get('source_category') or ('rendered_official_result_capture' if 'browser' in f or 'summary.json' in f else 'official_filing_or_record')
   if 'lead-cboe' in f:source_class='corporate_release_lead_only'
   if 'ny-' in f:source_class='official_open_dataset_reference_or_candidate_only'
   add('documents',document_id=docid,authority=authority,title=x.get('title') or x.get('document_type') or pathlib.Path(f).name,document_type=x.get('form') or x.get('document_type'),source_class=source_class,official_url=u,file_path=f,sha256=sha,filing_date=x.get('filing_date'),period_end=x.get('report_date') or x.get('period_end'),accession_id=x.get('accession_id'),pdf_pages=x.get('pdf_pages') or x.get('physical_page_count') or (x.get('physical_pages') if isinstance(x.get('physical_pages'),int) else None) or x.get('pages'),retrieved_at_utc=x.get('retrieved_at_utc'),preservation_status=x.get('preservation_note') or x.get('preserved_format') or 'original_response_bytes',metadata_json=json.dumps(x,ensure_ascii=False))
  docmap[old]=docid
  if not any(z['alias_id']==old for z in data['document_aliases']):add('document_aliases',alias_id=old,document_id=docid,origin_register=owner)
 else:docid=None
 add('retrieval_attempts',attempt_id=a_id,document_id=docid,requested_url=x.get('url'),retrieved_at_utc=x.get('retrieved_at_utc'),http_status=x.get('status_code') or x.get('http_status'),result='preserved' if ok else 'not_preserved',details=x.get('error') or x.get('note') or x.get('status') or '',origin_register=owner)
# Normalize all specialist assertions and source locators.
clmap={}
def claim(cid,statement,status,old,locator,subject=None,metadata=None,excerpt=None):
 if cid in clmap:return
 add('claims',claim_id=cid,subject_id=subject,statement=statement,evidence_status=status,review_status='specialist_claim; see independent-qa.md for bounded review',metadata_json=json.dumps(metadata or {},ensure_ascii=False));clmap[cid]=data['claims'][-1]
 if old:
  assert old in docmap,('unresolved document',cid,old)
  add('claim_evidence',claim_id=cid,document_id=docmap[old],locator=locator,short_extract=excerpt)
for x in ident.get('claims',[]):
 subject='E001' if int(x['id'].split('C')[-1])<=10 else 'E002'
 if x['id'] in ['ID-C001','ID-C021','ID-C022']:subject='P001'
 claim(x['id'],x['claim'],x['status'],x['source_id'],'physical PDF pages '+','.join(map(str,x['physical_pdf_pages'])) if x.get('physical_pdf_pages') else 'rendered text; query provenance per specialist note',subject,x)
for x in sc:
 cid=x['claim_id'];sid=x['document_id'];sub='E003'
 if '1555295' in cid:sub='E007'
 elif '2016250' in cid:sub='E014'
 elif '2016251' in cid:sub='E015'
 claim(cid,x['statement'],x['status'],sid,x['locator'],sub,x)
for x in evt.get('claims',[]):claim(x['claim_id'],x['statement'],x['status'],x['document_id'],'physical PDF pages '+','.join(map(str,x.get('physical_pages',[]))),'E020' if x['claim_id']=='EVT-C005' else 'E001',x)
for v,date,amount in [('956158','2024-12-31','578038743'),('1031410','2026-03-11','700332093')]:
 old='parent-entrypoint-brochure-'+v+'.pdf'
 claim('PAR-B'+v+'-RAUM',f'The March brochure version {v} reports approximately USD {amount} discretionary RAUM as of {date}.','verified_as_filed',old,'physical PDF p4, Item4','E003',{'measurement_date':date,'amount':amount})
 claim('PAR-B'+v+'-OWN','Brochure states EntryPoint is indirectly owned by Michael Bleich through EntryPoint Partners, LP.','verified_as_filed',old,'physical PDF p4, Item4','E003')
 claim('PAR-B'+v+'-FEES','Management fee summary states monthly one-twelfth of 2% of beginning-month capital-account balance, subject to waiver/modification. GP performance allocation summary states 20%; computation sentence is incomplete, so precise hurdle/watermark terms cannot be reconstructed.','verified_summary_with_limitation',old,'physical PDF pp4-5, Items5-6','E003')
 claim('PAR-B'+v+'-FORM','Brochure describes international and master funds as Cayman exempted limited partnerships, differing from the International FormD Corporation selection.','verified_as_filed',old,'physical PDF p4, Item4','E015')
claim('PAR-INF-001','Inferent Capital LLC official March6 2019 ADV identifies CRD292027 and SEC801-112741. Full extracted text contains no Bleich match; absence does not disprove an undisclosed employee role.','official_entity_confirmed_subject_affiliation_unresolved','lead-inferent-292027-adv.pdf','physical PDF p1, ScheduleA/B pp29-30; full-text search','E021')
claim('PAR-LEH-001','A Lehman corporate release dated September19 2006 hosted by Cboe names Michael Bleich as head of liquidity strategy. This is a career lead, not a verified government-record identity join.','corporate_release_lead_only','lead-cboe-lehman-20060919.pdf','physical PDF p1','E022')
for x in corp.get('claims',[]):
 loc='API response row '+str(x['response_row_one_based']) if x.get('response_row_one_based') else 'physical PDF pages '+','.join(map(str,x.get('physical_pdf_pages',[])))
 claim(x['id'],x['claim'],x['status'],x['source_id'],loc,None,x)
# Identifier assignments are source-linked; ambiguity is not silently collapsed.
def identifier(entity,scheme,value,cid,status='as_filed'):
 add('identifiers',identifier_id='I'+str(len(data['identifiers'])+1).zfill(3),entity_id=entity,scheme=scheme,value=value,match_status=status,claim_id=cid)
for e,scheme,val,c in [('E001','CRD','151990','ID-C002'),('E001','SEC','8-68420','ID-C002'),('E002','CRD','164729','ID-C011'),('E002','SEC','801-77121','ID-C011'),('E003','CRD','313946','SEC-C001'),('E003','SEC','801-130798','SEC-C001'),('E003','CIK','1992519','SEC-C001'),('E007','CIK','1555295','SEC-H1555295'),('E008','private_fund','805-5280422629','ID-C016'),('E008','private_fund','805-9412438643','ID-C017'),('E013','private_fund','805-7203779905','SEC-C009'),('E014','CIK','2016250','SEC-H2016250'),('E014','private_fund','805-8039696809','SEC-C009'),('E015','CIK','2016251','SEC-H2016251'),('E015','private_fund','805-5004504749','SEC-C009'),('E016','private_fund','805-3011135543','SEC-C011'),('E017','SEC','801-113731','SEC-C011'),('E021','CRD','292027','PAR-INF-001'),('E021','SEC','801-112741','PAR-INF-001')]:identifier(e,scheme,val,c,'ambiguous_same_name' if e=='E008' else 'as_filed')
def role(p,e,title,start,c,status='verified_as_filed',basis='status_acquired; not complete employment period'):
 add('roles',role_id='R'+str(len(data['roles'])+1).zfill(3),person_id=p,entity_id=e,title=title,start_value=start,end_value=None,date_basis=basis,evidence_status=status,claim_id=c)
role('P001','E001','CEO and Managing Member','2009-05','ID-C003');role('P001','E002','CEO and CCO','2012-04','ID-C012');role('P001','E003','Chief Investment Officer','2023-05','SEC-C002');role('P001','E007','Director','2012-07-31','SEC-D-0001555295-12-000002-SIG',basis='signature date; appointment commencement unknown');role('P004','E003','CEO','2020-10','SEC-C013');role('P005','E003','CCO, COO, CFO','2023-05','SEC-C013')
def edge(src,dst,t,c,start=None,low=None,hi=None,upper_exclusive=None,status='verified_as_filed',note=''):
 add('relationships',relationship_id='L'+str(len(data['relationships'])+1).zfill(3),source_subject_id=src,target_subject_id=dst,relationship_type=t,effective_from=start,effective_to=None,ownership_min_percent=low,ownership_max_percent=hi,upper_exclusive=upper_exclusive,evidence_status=status,claim_id=c,note=note)
for args in [('P001','E004','shareholder','ID-C005','2009-05',75,100,0),('E004','E005','member','ID-C006','2012-08',50,75,1),('E006','E005','member','ID-C007','2012-08',25,50,1),('P003','E006','member','ID-C008','2009-05',25,50,1),('E005','E001','member','ID-C004','2012-08',75,100,0),('E005','E001','wholly_owned_as_reported','ID-C009','2012-06-01',100,100,0),('E005','E002','wholly_owned_as_reported','ID-C009','2012-06-01',100,100,0),('E005','E002','managing_member','ID-C013','2012-04',75,100,0),('E004','E005','managing_member','ID-C014','2012-04',75,100,0),('P001','E004','owner','ID-C015','2009-05',75,100,0),('P001','E011','member','SEC-C003','2023-07',25,50,1),('P001','E010','limited_partner','SEC-C004','2023-07',25,50,1),('E010','E003','member','SEC-C005','2020-10',75,100,0)]:edge(*args)
edge('E011','E003','general_partner_designation_as_filed','SEC-C006','2020-10',note='NA less-than5% code; no affirmative holding implied; role kept as filed.')
edge('E009','E008','GP_manager_or_director_as_listed','ID-C016',note='Specifically Section7B1 privatefund805-5280422629; not attributed to other same-name ID805-9412438643.');edge('E014','E013','feeder_to_master','SEC-C009');edge('E015','E013','feeder_to_master','SEC-C009')
for f in ['E013','E014','E015']:edge('E012',f,'GP_manager_or_equivalent_as_listed','SEC-C009')
edge('E003','E012','related_person_disclosure','SEC-C012');edge('E003','E016','Schedule7B2_advisory_reporting_connection','SEC-C011',note='No personal ownership or employment inferred.');edge('E017','E016','full_private_fund_reporting_adviser','SEC-C011');edge('P004','E011','member','SEC-C015','2020-10',25,50,1);edge('E018','E011','member','SEC-C015','2024-11',25,50,1);edge('E019','E018','trustee','SEC-C015','2020-12')
# Financial observations preserve metric and period distinctions. Decimal amounts are strings.
def fin(e,metric,value,unit,cid,date=None,basis=None,currency='USD',filing_date=None,status='as_filed'):
 add('financial_observations',observation_id='F'+str(len(data['financial_observations'])+1).zfill(3),entity_id=e,metric=metric,amount=str(value),currency=currency,unit=unit,measurement_date=date,measurement_date_basis=basis,filing_date=filing_date,evidence_status=status,claim_id=cid)
fin('E003','regulatory_assets_under_management','999157153','dollars','SEC-C007','2026-09-30','explicit ScheduleD Miscellaneous','USD','2026-10-15');fin('E013','private_fund_gross_asset_value','799157153','dollars','SEC-C010',None,'current value field; September30 RAUM date not transplanted','USD','2026-10-15');fin('E002','regulatory_assets_under_management','24250059','dollars','ID-C019',None,'measurement date not established','USD','2017-03-30');fin('E008','private_fund_gross_asset_value','24250059','dollars','ID-C019',None,'Specifically Section7B1 ID805-5280422629; no attribution to805-9412438643; measurement date not established','USD','2017-03-30')
for v,date,amount in [('956158','2024-12-31','578038743'),('1031410','2026-03-11','700332093')]:fin('E003','regulatory_assets_under_management',amount,'dollars','PAR-B'+v+'-RAUM',date,'explicit brochure; approximately',filing_date=None)
for x in sc:
 if x.get('metric')=='FormD_cumulative_amount_sold':
  e='E014' if '2016250' in x['claim_id'] else 'E015' if '2016251' in x['claim_id'] else 'E007'
  fin(e,'FormD_cumulative_amount_sold',x['value'],'dollars',x['claim_id'],None,'cumulative notice as filed; not period flows',filing_date=x.get('filing_date'))
  fin(e,'FormD_investor_count',x['investor_count'],'issuer_reported_investors',x['claim_id'],None,'not verified unique natural persons',currency=None,filing_date=x.get('filing_date'))
# Financial-stage data remains separately preserved; normalize reviewed cover observations without correcting originals.
financial=read('financial-observations.json',[])
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

# Events remain firm events. Litigation with no demonstrated investment-management nexus is excluded.
for x in evt.get('events',[]):
 e='E020' if x.get('respondent_crd')=='877' else 'E001';add('events',event_id=x['event_id'],respondent_entity_id=e,event_type='regulatory_firm_event',authority=x['authority'],case_number=x.get('case_number'),initiated_date=x.get('initiated_date'),resolution_date=x.get('resolution_date'),fine_amount=str(x['fine_amount']),currency=x['currency'],disposition=x['disposition'],personal_sanction_attribution=x.get('personal_sanction_attribution') or 'Firm respondent; no personal sanction inference',note=x.get('qualification') or '')
 for c in x['claim_ids']:add('event_claims',event_id=x['event_id'],claim_id=c)
for owner,logs in [('identity',ident.get('search_logs',[])),('events',evt.get('search_logs',[])),('corporate',corp.get('search_logs',[])),('financial',read('financial-search-log.json',[])),('parent',read('parent-search-log.json',[]))]:
 for x in logs:add('search_logs',search_id='S'+str(len(data['search_logs'])+1).zfill(3),source_system=x.get('database') or x.get('method') or owner,query=x.get('query') if isinstance(x.get('query'),str) else json.dumps(x.get('queries') or x.get('query') or x.get('url')),searched_at_utc=x.get('timestamp_utc') or x.get('searched_on_utc') or '2026-11-04',time_precision='as_recorded',result=x.get('result') if isinstance(x.get('result'),str) else json.dumps(x.get('result') or x.get('note')),coverage_limit=x.get('coverage_limit') or 'Bounded search only; absence of returned results is not absence of conduct.',metadata_json=json.dumps(x,ensure_ascii=False))
for owner,conf in [('identity',ident.get('conflicts',[])),('events',evt.get('conflicts',[]))]:
 for n,x in enumerate(conf):
  i=x.get('id') or x.get('conflict_id') or owner+'-X'+str(n+1);add('conflicts',conflict_id=i,topic=x.get('topic') or x.get('issue') or x.get('title') or 'source representation discrepancy',status='open_or_source_specific',resolution=x.get('detail') or x.get('resolution') or x.get('note') or json.dumps(x,ensure_ascii=False))
  for c in x.get('claims',x.get('claim_ids',[])):
   if c in clmap:add('conflict_claims',conflict_id=i,claim_id=c)
for i,topic,detail,cids in [('X-INT-FORM','International feeder legal form','FormD2024-2026 selects Corporation; March2025/2026 brochures describe Cayman exempted LP. Registry original needed.',['SEC-D-0002016251-26-000001','PAR-B1031410-FORM']),('X-CIO-DATE','EntryPoint career-start versus reported status date','Third-party professional profile suggests October2020; official ScheduleA status acquiredMay2023. Neither proves the other date is erroneous. Full employment timeline unresolved.',['SEC-C002']),('X-ARCHIVE','Prior Library archive inaccessible','Five named prior research files not attached; user confirms no local copies. No claim of reconciliation. No existing ReBlei materials used. ',[]),('X-FEE','Performance allocation calculation incomplete','Brochure summary20% sentence lacks enough text to reconstruct precise base/hurdles/watermarks. No actual revenue or personal income inferred.',['PAR-B1031410-FEES'])]:
 add('conflicts',conflict_id=i,topic=topic,status='unresolved',resolution=detail)
 for c in cids:add('conflict_claims',conflict_id=i,claim_id=c)
add('conflicts',conflict_id='X-13F-2024Q3',topic='13F original cover versus information-table values',status='unresolved_quarantined',resolution='0001992519-24-000008 cover entryTotal175789/valueTotal594; information table594 entries sum175789004 USD. Preserve raw and derived values separately; cause unknown, no silent correction.')
add('conflict_claims',conflict_id='X-13F-2024Q3',claim_id='FIN-13F-0001992519-24-000008')
# Explicit relational schema, with references enforcing ownership of evidence and identity.
schema='''PRAGMA foreign_keys=ON;
CREATE TABLE subjects(subject_id TEXT PRIMARY KEY,kind TEXT NOT NULL CHECK(kind IN ('person','entity')),display_name TEXT NOT NULL);
CREATE TABLE persons(person_id TEXT PRIMARY KEY REFERENCES subjects(subject_id),legal_name TEXT NOT NULL,crd TEXT,identity_status TEXT,note TEXT);
CREATE TABLE entities(entity_id TEXT PRIMARY KEY REFERENCES subjects(subject_id),legal_name TEXT NOT NULL,entity_type TEXT,jurisdiction TEXT,inclusion_status TEXT,note TEXT);
CREATE TABLE documents(document_id TEXT PRIMARY KEY,authority TEXT,title TEXT,document_type TEXT,source_class TEXT,official_url TEXT,file_path TEXT,sha256 TEXT CHECK(length(sha256)=64),filing_date TEXT,period_end TEXT,accession_id TEXT,pdf_pages INTEGER,retrieved_at_utc TEXT,preservation_status TEXT,metadata_json TEXT);
CREATE TABLE document_aliases(alias_id TEXT PRIMARY KEY,document_id TEXT NOT NULL REFERENCES documents(document_id),origin_register TEXT);
CREATE TABLE claims(claim_id TEXT PRIMARY KEY,subject_id TEXT REFERENCES subjects(subject_id),statement TEXT NOT NULL,evidence_status TEXT,review_status TEXT,metadata_json TEXT);
CREATE TABLE claim_evidence(claim_id TEXT REFERENCES claims(claim_id),document_id TEXT REFERENCES documents(document_id),locator TEXT NOT NULL,short_extract TEXT,PRIMARY KEY(claim_id,document_id));
CREATE TABLE identifiers(identifier_id TEXT PRIMARY KEY,entity_id TEXT REFERENCES entities(entity_id),scheme TEXT,value TEXT,match_status TEXT,claim_id TEXT REFERENCES claims(claim_id));
CREATE TABLE roles(role_id TEXT PRIMARY KEY,person_id TEXT REFERENCES persons(person_id),entity_id TEXT REFERENCES entities(entity_id),title TEXT,start_value TEXT,end_value TEXT,date_basis TEXT,evidence_status TEXT,claim_id TEXT REFERENCES claims(claim_id));
CREATE TABLE relationships(relationship_id TEXT PRIMARY KEY,source_subject_id TEXT REFERENCES subjects(subject_id),target_subject_id TEXT REFERENCES subjects(subject_id),relationship_type TEXT,effective_from TEXT,effective_to TEXT,ownership_min_percent REAL,ownership_max_percent REAL,upper_exclusive INTEGER,evidence_status TEXT,claim_id TEXT REFERENCES claims(claim_id),note TEXT);
CREATE TABLE financial_observations(observation_id TEXT PRIMARY KEY,entity_id TEXT REFERENCES entities(entity_id),metric TEXT,amount TEXT,currency TEXT,unit TEXT,measurement_date TEXT,measurement_date_basis TEXT,filing_date TEXT,evidence_status TEXT,claim_id TEXT REFERENCES claims(claim_id));
CREATE TABLE events(event_id TEXT PRIMARY KEY,respondent_entity_id TEXT REFERENCES entities(entity_id),event_type TEXT,authority TEXT,case_number TEXT,initiated_date TEXT,resolution_date TEXT,fine_amount TEXT,currency TEXT,disposition TEXT,personal_sanction_attribution TEXT,note TEXT);
CREATE TABLE event_claims(event_id TEXT REFERENCES events(event_id),claim_id TEXT REFERENCES claims(claim_id),PRIMARY KEY(event_id,claim_id));
CREATE TABLE search_logs(search_id TEXT PRIMARY KEY,source_system TEXT,query TEXT,searched_at_utc TEXT,time_precision TEXT,result TEXT,coverage_limit TEXT,metadata_json TEXT);
CREATE TABLE conflicts(conflict_id TEXT PRIMARY KEY,topic TEXT,status TEXT,resolution TEXT);
CREATE TABLE conflict_claims(conflict_id TEXT REFERENCES conflicts(conflict_id),claim_id TEXT REFERENCES claims(claim_id),PRIMARY KEY(conflict_id,claim_id));
CREATE TABLE retrieval_attempts(attempt_id TEXT PRIMARY KEY,document_id TEXT REFERENCES documents(document_id),requested_url TEXT,retrieved_at_utc TEXT,http_status INTEGER,result TEXT,details TEXT,origin_register TEXT);
'''
# Rebuild derived database only. Original evidence files are never overwritten by this builder.
db=ROOT/'evidence-index.sqlite';temp=ROOT/'evidence-index.build.sqlite'
if temp.exists():temp.unlink()
con=sqlite3.connect(temp);con.executescript(schema)
order=['subjects','persons','entities','documents','document_aliases','claims','claim_evidence','identifiers','roles','relationships','financial_observations','events','event_claims','search_logs','conflicts','conflict_claims','retrieval_attempts']
for k in order:
 for row in data[k]:
  cols=list(row);con.execute('INSERT INTO '+k+' ('+','.join(cols)+') VALUES ('+','.join('?' for _ in cols)+')',[row[c] for c in cols])
assert not con.execute('PRAGMA foreign_key_check').fetchall()
assert con.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
con.commit();con.close();temp.replace(db)
(ROOT/'schema.sql').write_text(schema,encoding='utf8')
(ROOT/'evidence-index.json').write_text(json.dumps({'schema_version':1,'generated_at_utc':NOW,'cutoff_date':'2026-11-04','scope':'Full-career mandate; bounded completed stages with explicit gaps; investment-management conduct only; existing repository material excluded','tables':data},indent=2,ensure_ascii=False),encoding='utf8')
(ROOT/'tables').mkdir(exist_ok=True)
for k,rows in data.items():
 if not rows:continue
 with (ROOT/'tables'/(k+'.csv')).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
summary={'generated_at_utc':NOW,'table_counts':{k:len(v) for k,v in data.items()},'foreign_key_check':'passed','sqlite_integrity_check':'ok','preserved_document_hashes':'all rechecked at build','full_career_complete':False,'independent_qa_scope':'specialist originals, brochures, 13F anomaly and bounded final normalized index second pass; see independent-qa.md, not every filing audited'}
(ROOT/'validation.json').write_text(json.dumps(summary,indent=2),encoding='utf8');print(json.dumps(summary,indent=2))
