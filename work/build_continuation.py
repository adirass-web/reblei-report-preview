# Extend the existing normalized register from the four preserved continuation manifests.
# Invoked by build_index.py with ROOT and data in globals; no source originals are mutated.
import json,pathlib,hashlib

def read2(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def rows2(v,*keys):
 if isinstance(v,list):return v
 for k in keys:
  if isinstance(v.get(k),list):return v[k]
 return []
def add2(table,**row):data[table].append(row)
def text2(v):return v if isinstance(v,str) or v is None else json.dumps(v,ensure_ascii=False)
byhash={r['sha256']:r['document_id'] for r in data['documents']}; aliases={r['alias_id']:r['document_id'] for r in data['document_aliases']}
subject_names={r['display_name'].lower().replace(',','').strip():r['subject_id'] for r in data['subjects']}
new_claims=set(); raw_claims=[]; branches={}; failed_sources={}
for stage,branch in [('continuation',x) for x in ['early-employment','corporate-ownership','inferent','investment-litigation']]+[('continuation-2',x) for x in ['employment','inferent','ownership','litigation']]+[('continuation-3',x) for x in ['inferent','employment','ownership','award-followup']]+[('continuation-4',x) for x in ['entrypoint-history','employment-inferent','corporate-identity','investment-litigation']]:
 folder=ROOT/stage/branch
 sources=read2(folder/'sources.json'); claims=read2(folder/'claims.json'); logs=read2(folder/'search-log.json');branches[branch]=(sources,claims,logs)
 for n,x in enumerate(rows2(sources,'documents','sources')):
  old=x.get('document_id') or x.get('source_id') or x.get('id') or 'CONT-'+branch+'-'+str(n)
  url=x.get('url') or x.get('requested_url') or x.get('final_url'); path=x.get('file') or x.get('file_path') or x.get('local_file'); sha=x.get('sha256');docid=None
  if path and sha:
   path=path.replace('\\','/'); options=[ROOT/path,folder/path]
   found=[p for p in options if p.is_file()]
   assert found,('missing original',branch,old,path)
   p=found[0].resolve();p.relative_to(ROOT.resolve());assert hashlib.sha256(p.read_bytes()).hexdigest()==sha.lower(),('source hash mismatch',old)
   path=p.relative_to(ROOT.resolve()).as_posix();docid=byhash.get(sha.lower())
   if docid is None:
    docid=old;assert not any(r['document_id']==docid for r in data['documents']),('document ID collision',old)
    cls=x.get('source_class') or x.get('evidence_class') or x.get('source_type') or ('discovery_capture_not_case_evidence' if 'parallel' in path else 'official_response_context_in_metadata')
    authority=x.get('authority') or ('SEC' if url and 'sec.gov' in url else 'Delaware Division of Corporations' if url and 'delaware.gov' in url else 'Cboe' if url and 'cboe.com' in url else 'NY Department of State open data' if url and 'data.ny.gov' in url else None)
    add2('documents',document_id=docid,authority=authority,title=x.get('title') or x.get('description') or p.name,document_type=x.get('document_type') or x.get('content_type') or x.get('source_format'),source_class=cls,official_url=url,file_path=path,sha256=sha.lower(),filing_date=x.get('filing_date') or x.get('order_date'),period_end=x.get('period_end'),accession_id=x.get('accession_id'),pdf_pages=x.get('pdf_pages') or x.get('physical_page_count') or x.get('page_count') or (x.get('physical_pages') if isinstance(x.get('physical_pages'),int) else None),retrieved_at_utc=x.get('retrieved_at_utc'),preservation_status=x.get('preservation_note') or x.get('preservation_status') or x.get('document_role') or 'see source_class and source metadata',metadata_json=json.dumps(x,ensure_ascii=False));byhash[sha.lower()]=docid
   if old not in aliases:add2('document_aliases',alias_id=old,document_id=docid,origin_register=stage+'/'+branch);aliases[old]=docid
   else:assert aliases[old]==docid,('alias collision',old)
  if docid is None:failed_sources[old]=folder/'sources.json'
  add2('retrieval_attempts',attempt_id='CONT-ACQ-'+str(len(data['retrieval_attempts'])+1).zfill(4),document_id=docid,requested_url=url,retrieved_at_utc=x.get('retrieved_at_utc'),http_status=x.get('http_status') or x.get('status_code'),result='preserved' if docid else 'not_preserved',details=text2(x.get('error') or x.get('access_limitation') or x.get('preservation_note') or ''),origin_register=stage+'/'+branch)
 for x in rows2(claims,'claims'):
  cid=x.get('claim_id') or x.get('id');assert cid and not any(r['claim_id']==cid for r in data['claims']),('claim collision',cid)
  statement=x.get('statement') or x.get('claim');assert statement,('empty claim',cid)
  sub=x.get('subject_id') or subject_names.get(str(x.get('entity_name','')).lower().replace(',','').strip())
  if sub:assert any(r['subject_id']==sub for r in data['subjects']),('subject reference',cid,sub)
  status=x.get('evidence_status') or x.get('status') or 'see specialist claim qualification'
  add2('claims',claim_id=cid,subject_id=sub,statement=statement,evidence_status=status,review_status=stage+' specialist claim; independent review scope in that stage QA reports',metadata_json=json.dumps(x,ensure_ascii=False));new_claims.add(cid);raw_claims.append((stage+'/'+branch,x))
  ev=x.get('evidence') or []
  if not ev:
   ids=x.get('document_ids') or x.get('source_ids') or [x.get('document_id') or x.get('source_id')]
   ev=[{'document_id':d,'locator':x.get('locator') or '; '.join(x.get('locators',[])),'physical_pages':x.get('physical_pdf_pages') or x.get('physical_pages')} for d in ids if d]
  assert ev,('no evidence links',cid)
  linked=set()
  for e in ev:
   if isinstance(e,str):e={'document_id':e}
   did=e.get('document_id') or e.get('source_id')
   if did not in aliases and did in failed_sources:
    fp=failed_sources[did]; lid='REQUEST-LOG-'+stage+'-'+branch
    if not any(r['document_id']==lid for r in data['documents']):
     add2('documents',document_id=lid,authority='researcher retrieval log',title=stage+'/'+branch+' request log',document_type='JSON request metadata',source_class='request_log_not_original_case_record',official_url=None,file_path=fp.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(fp.read_bytes()).hexdigest(),filing_date=None,period_end=None,accession_id=None,pdf_pages=None,retrieved_at_utc=None,preservation_status='Researcher request log; no claim that failed original was saved',metadata_json=json.dumps({'purpose':'Documents failed requests only'}))
    aliases[did]=lid;e['locator']='sources.json record '+did+'; '+str(e.get('locator',''))
   assert did in aliases,('unresolved evidence',cid,did)
   canon=aliases[did]
   if canon in linked:continue
   linked.add(canon);pages=e.get('physical_pages') or e.get('physical_pdf_pages')
   loc=e.get('locator') or ('physical PDF pages '+','.join(map(str,pages)) if pages else None) or x.get('locator') or 'Source field/section described in specialist claim metadata'
   add2('claim_evidence',claim_id=cid,document_id=canon,locator=text2(loc),short_extract=e.get('short_extract'))
 logrows=rows2(logs,'batches','search_logs','searches','logs')
 if isinstance(logs,dict):logrows=logrows+logs.get('direct_official_requests',[])
 for x in logrows:
  add2('search_logs',search_id='CONT-S'+str(len(data['search_logs'])+1).zfill(4),source_system=x.get('source_system') or x.get('provider') or x.get('service') or x.get('database') or x.get('method') or stage+'/'+branch,query=text2(x.get('queries') or x.get('search_queries') or x.get('query') or x.get('url') or x.get('objective')),searched_at_utc=x.get('searched_at_utc') or x.get('retrieved_at_utc') or x.get('timestamp_utc') or x.get('logged_at_utc') or (logs.get('logged_at_utc') or logs.get('prepared_at_utc') if isinstance(logs,dict) else None),time_precision=x.get('time_precision') or 'as recorded',result=text2(x.get('result') or x.get('conclusion') or x.get('outcome') or x.get('http_status') or x.get('results')),coverage_limit=x.get('coverage_limit') or x.get('limits') or 'Bounded retrieval/search; no comprehensive absence inference.',metadata_json=json.dumps(x,ensure_ascii=False))
 if isinstance(claims,dict):
  for x in claims.get('open_conflicts',[]):
   ident=x.get('conflict_id');assert ident and not any(r['conflict_id']==ident for r in data['conflicts'])
   add2('conflicts',conflict_id=ident,topic=x.get('issue') or x.get('topic'),status=x.get('status') or 'unresolved',resolution=x.get('resolution') or x.get('note') or json.dumps(x,ensure_ascii=False))
   for cid in x.get('claim_ids',[]):
    assert cid in new_claims;add2('conflict_claims',conflict_id=ident,claim_id=cid)
# Link new originals to existing events; never count them as additional sanctions.
for branch,x in raw_claims:
 if branch!='continuation/investment-litigation':continue
 case=(x.get('case_number') or '').replace(' ','').upper()
 if not case:continue
 for event in data['events']:
  if (event.get('case_number') or '').replace(' ','').upper()==case:
   add2('event_claims',event_id=event['event_id'],claim_id=x['claim_id'])
# Inferent remains a conditional affiliate branch; metadata IDs do not prove employment.
for entity,cik,cid in [('E029','1750250','INF-C001'),('E026','1769569','INF-C002')]:
 add2('identifiers',identifier_id='CONT-CIK-'+cik,entity_id=entity,scheme='CIK',value=cik,match_status='official entity metadata; subject affiliation remains unverified',claim_id=cid)
# Every source byte representation is checked, including reused originals.
for x in data['documents']:assert hashlib.sha256((ROOT/x['file_path']).read_bytes()).hexdigest()==x['sha256'],x['document_id']

# New corporate IDs remain provisional mappings to regulatory names.
for entity,scheme,value,cid in [
 ('E011','Delaware file','3458887','CORP2-ENTITY-3458887'),('E010','Delaware file','3458856','CORP2-ENTITY-3458856'),('E005','Delaware file','5142327','CORP2-ENTITY-5142327'),('E006','Delaware file','4688408','CORP2-ENTITY-4688408'),('E009','New York DOS','4790401','CORP2-NY-BEAUFORT'),('E008','New York DOS','4790408','CORP2-NY-BEAUFORT')]:
 add2('identifiers',identifier_id='CONT-REG-'+value,entity_id=entity,scheme=scheme,value=value,match_status='provisional name/chronology mapping; no ownership-ID join proven',claim_id=cid)
for ent,name,typ,juris,status,note in [
 ('E032','Lehman Brothers Holdings Inc.','bankruptcy debtor; disclosed contract counterparty','United States','official_debtor_record_subject_person_join_provisional','Separate from unresolved legal employer Lehman Brothers Inc. Debtor schedule is not an adjudication of employment, award entitlement or claim allowance.'),
 ('E033','Finch LLC (Delaware file10521968)','same-name corporate candidate','Delaware','excluded_from_historical_2012_join','Formation2026-02-24; no succession evidence. Do not merge with historical Finch ownership intermediary.')]:
 add2('subjects',subject_id=ent,kind='entity',display_name=name);add2('entities',entity_id=ent,legal_name=name,entity_type=typ,jurisdiction=juris,inclusion_status=status,note=note)
add2('identifiers',identifier_id='CONT-REG-10521968',entity_id='E033',scheme='Delaware file',value='10521968',match_status='verified registry identity; excluded historical subject linkage',claim_id='CORP2-ENTITY-10521968')
add2('relationships',relationship_id='CONT-R001',source_subject_id='P001',target_subject_id='E032',relationship_type='provisional exact-full-name RSU contract counterparty',effective_from=None,effective_to=None,ownership_min_percent=None,ownership_max_percent=None,upper_exclusive=None,evidence_status='court-agent original; subject identity join provisional without CRD',claim_id='EARLY-C003',note='Schedule filed2009-03-12 is not employment or award date. No compensation entitlement or misconduct inferred.')
manual_subjects={'EARLY-C003':'P001','EARLY-C004':'P001','EARLY-C005':'E022','EARLY-C006':'P001','CORP2-ENTITY-3458887':'E011','CORP2-ENTITY-3458856':'E010','CORP2-ENTITY-5142327':'E005','CORP2-ENTITY-10521968':'E033','CORP2-ENTITY-4688408':'E006','CORP2-NY-MEB':'E004','CORP2-NY-PARTNERS':'E010'}
for row in data['claims']:
 if row['claim_id'] in manual_subjects:row['subject_id']=manual_subjects[row['claim_id']]
for ev in data['events']:
 if (ev.get('case_number') or '').replace(' ','').upper()=='12-0099AND12-0126':
  ev['note']=(ev.get('note') or '')+' FINRA-reported resolution date2013-06-26 retained; original order is dated2013-07-03. Their procedural relationship is unresolved; see LIT-C009.'
add2('conflicts',conflict_id='CONT-X-CIK1977777',topic='Rejected third-party EP Fund GP CIK assignment',status='rejected_identifier_assignment',resolution='Official SEC submissions CIK1977777 names Cata Labs Inc.; do not assign to EP Fund GP or the subject.')
add2('conflict_claims',conflict_id='CONT-X-CIK1977777',claim_id='CORP2-CIK-REJECTION')

# Round2: one new arbitration, not another regulatory penalty.
for row in data['events']:row['claimant_entity_id']=None
for row in data['events']:
 if row['event_id']=='EVT-E005':
  row['case_number']='20100243866-02';row['resolution_date']='2016-02-25'
  row['disposition']='Nasdaq AWC accepted without admitting or denying findings and without adjudication; censure and joint FINRA/Nasdaq fine'
  row['note']='Original Nasdaq acceptance date2016-02-25. Joint fineUSD675000 includesUSD337500Nasdaq, not an additional fine. Sanctions effective date to be set byFINRAstaff; payment/undertaking completion not verified.'
add2('events',event_id='LIT3-E001',respondent_entity_id='E020',event_type='firm_arbitration_award_identity_join_inferred',authority='FINRA Office of Dispute Resolution',case_number='15-02816',initiated_date='2015-10-22',resolution_date='2016-11-18',fine_amount=None,currency='USD',disposition='Wedbush ordered to pay Scout damages,interest,filing-fee reimbursement; counterclaim and unspecified relief including attorneys fees denied.',personal_sanction_attribution='No Bleich party or personal sanction in award. ScoutCRD151990join probable inference from multiple officialrecords.',note='Claim filed on or about2015-10-22; resolution field uses FINRAindex/service date; signature dates2016-11-16. Legal date of award for interest unresolved. No payment,appeal,confirmation,vacatur or satisfaction verified.',claimant_entity_id='E001')
for cid in ['LIT3-C03','LIT3-C04','LIT3-C05','LIT3-C06','LIT3-C07','LIT3-C08','LIT3-C09','LIT3-C10']:add2('event_claims',event_id='LIT3-E001',claim_id=cid)
for cid in ['LIT3-C11','LIT3-C12']:add2('event_claims',event_id='EVT-E005',claim_id=cid)
for oid,entity,metric,amount,cid,basis in [
 ('LIT3-F001','E001','arbitration_compensatory_damages_awarded','237594','LIT3-C04','Obligation awarded; collection notverified. Separate from RAUM,revenue,personalincome and regulatoryfines.'),
 ('LIT3-F002','E001','arbitration_filing_fee_reimbursement_awarded','1250','LIT3-C04','Reimbursementordered toScout; noactualpaymentestablished.'),
 ('LIT3-F003','E020','arbitration_hearing_session_fees_assessed','9550','LIT3-C09','Assessed toWedbush payabletoFINRA; notScoutincome orregulatoryfine.')]:
 add2('financial_observations',observation_id=oid,entity_id=entity,metric=metric,amount=amount,currency='USD',unit='dollars',measurement_date=None,measurement_date_basis=basis,filing_date=None,evidence_status='verified_award_content; Scoutentitymappingprobableinference',claim_id=cid)
for ident,topic,resolution,cids in [
 ('LIT3-X-DATE','Award signature/service/index dates and interest boundary','Signatures2016-11-16;FINRAservice/index2016-11-18; legal interestboundary unresolved.',['LIT3-C05','LIT3-C07']),
 ('LIT3-X-AMOUNTS','Different requested-relief amounts printed in award','Requested clearingdamages237594 versus alternativeconversion237549; awarded237594. Preserveasprinted withouttypoassumption.',['LIT3-C08']),
 ('LIT3-X-IDENTITY','Scout arbitration claimant mapped to subjectfirm by corroboration','Probable official-recordinference; noCRDinaward. Samefirmname,Wedbushclearingrelationship,675kregulatorycontext; namecollisionnoteliminated.',['LIT3-C10'])]:
 add2('conflicts',conflict_id=ident,topic=topic,status='explicitly_qualified_unresolved',resolution=resolution)
 for cid in cids:add2('conflict_claims',conflict_id=ident,claim_id=cid)
for row in data['claims']:
 if row['claim_id'].startswith('EMP3-'):row['subject_id']='P001'
 if row['claim_id'].startswith('INF3-'):row['subject_id']='E021'

# Historical Inferent firm observations, not subject assets or employment proof.
for oid,metric,value,filing,cid in [('INF3-F001','client_assets_under_management_approximate','31250250','2018-07-05','INF3-C002'),('INF3-F002','regulatory_assets_under_management_approximate','62000000','2018-08-31','INF3-C003')]:
 add2('financial_observations',observation_id=oid,entity_id='E021',metric=metric,amount=value,currency='USD',unit='dollars',measurement_date=None,measurement_date_basis='Original brochure states approximatelyUS$; exact assetmeasurementdate notspecified. Filingdatefromofficialmapping isnotmeasurementdate. Inferent-Bleichaffiliationunverified.',filing_date=filing,evidence_status='verified_as_filed_firm_fact_in_conditional_branch',claim_id=cid)

add2('conflicts',conflict_id='INF3-X-FUNDNAME',topic='Inferent2018 Client/Master fund wording versus2019ADV name',status='unresolved_wording_and_identity',resolution='August2018brochurep4 introducesInferentQEClientLP then referencesMasterFund;2019ADV p19 namesInferentQEMasterFundLP805-6736389159. No typo,rename,succession or entityequivalence assumed. No newverifiedentitycreated.')
add2('conflict_claims',conflict_id='INF3-X-FUNDNAME',claim_id='INF3-C008')

# Round3: dated original ownership snapshots, without silently reconciling dates.
add2('identifiers',identifier_id='CORP4-CIK-1474522',entity_id='E001',scheme='CIK',value='1474522',match_status='official SEC metadata and SEC-file-number match to FINRA',claim_id='CORP4-C01')
for rid,owner,typ,frm,to,minp,maxp,cid,note in [
 ('CORP4-R01','E004','direct owner before disclosed holding-company transition',None,'2012-08-31',None,None,'CORP4-C03','FY2012 Note1 says until August31; no inception date, exact percentage or registry ID.'),
 ('CORP4-R02','E006','direct owner before disclosed holding-company transition',None,'2012-08-31',None,None,'CORP4-C03','FY2012 Note1 says until August31; no inception date, exact percentage or registry ID.'),
 ('CORP4-R03','E005','sole direct owner as disclosed in FY2012 audited note','2012-08-31',None,100,100,'CORP4-C03','Source-specific date; BrokerCheck common-control narrative givesJune1; reconciliation unresolved. FY2013 Note1 corroborates wholly owned. No current-ownership claim.')]:
 add2('relationships',relationship_id=rid,source_subject_id=owner,target_subject_id='E001',relationship_type=typ,effective_from=frm,effective_to=to,ownership_min_percent=minp,ownership_max_percent=maxp,upper_exclusive=0 if minp is not None else None,evidence_status='verified_as_filed_date_conflict_retained',claim_id=cid,note=note)
for oid,metric,value,day,basis in [
 ('CORP4-F01','subordinated_debt_principal_repayment_reported','5000000','2013-10-08','FY2013 Note5 reports payment to NAYS LLC plus unpaid interest; interest amount unspecified, no personal income attribution.'),
 ('CORP4-F02','subordinated_note_liability_to_unnamed_member','4000000','2013-12-31','FY2013 Note5; remaining lender not identified; 10% annual, due2014. Not assigned to NAYS or Bleich.')]:
 add2('financial_observations',observation_id=oid,entity_id='E001',metric=metric,amount=value,currency='USD',unit='dollars',measurement_date=day,measurement_date_basis=basis,filing_date='2014-02-28',evidence_status='verified_as_filed_corporate_financing',claim_id='CORP4-C05')
for rid,title,date,docnote in [
 ('CORP4-ROLE01','Member (annual-report oath capacity)','2010-02-26','FY2009 report; no independently established signature date.'),
 ('CORP4-ROLE02','Managing member (annual-report oath capacity)','2014-02-28','FY2013 report; no independently established signature date.')]:
 add2('roles',role_id=rid,person_id='P001',entity_id='E001',title=title,start_value=None,end_value=None,date_basis='Oath in filing dated'+date+'; '+docnote+' Not role commencement or full employment period.',evidence_status='official_oath_content_subject_join_supported',claim_id='CORP4-C02')
for ident,topic,resolution,cids in [
 ('CORP4-X-DATE','Scout holding-company ownership transition date','FY2012 audited note: August31,2012. FINRA ownership schedules: August2012. FINRA common-control effective date: June1,2012. Different source/event meanings unresolved.',['CORP4-C03','CORP4-C06']),
 ('CORP4-X-MEMBER','Historical Scout FINRA membership statements','FY2009 original/amendment call Scout a FINRA member; May2016 FINRA bulletin says Nasdaq but not FINRA in a passage about a separate April7,2015 proceeding, without dating nonmembership throughout the conduct period. No error or membership-change timeline established.',['CORP4-C07']),
 ('CORP4-X-PERIOD','Scout FY2009 report-period start versus establishment','Report period starts February5,2009; FINRA establishment May20,2009. Neither treated as employment start; no assumed corporate continuity before establishment.',['CORP4-C08']),
 ('INF4-X-ENTRYPOINT','EntryPoint historical same-CRD name and SEC-file differences','CRD313946 July12,2021 row: ENTRYPOINT CAPITAL /801-122062, Initial SEC Registration=Y, Final SEC ERA blank. June27,2024 row: ENTRYPOINT CAPITAL,LLC /801-130798, BOTH Initial SEC Registration=Y and Final SEC ERA=Y. No explanation selected for dual flags, name/file differences or corporate history.',['INF4-C008'])]:
 add2('conflicts',conflict_id=ident,topic=topic,status='unresolved_source_specific',resolution=resolution)
 for cid in cids:add2('conflict_claims',conflict_id=ident,claim_id=cid)
for row in data['roles']:
 if row['role_id']=='R002':
  row['date_basis']='Single status-acquired field04/2012 in combined CEO/CCO row of2017ADV. Historical CEO-only rows precede CEO,CCO wording by March2015; not proof CCO began04/2012 or CEO ceased.'
for row in data['claims']:
 if row['claim_id'].startswith('INF4-'):row['subject_id']='E003' if row['claim_id']=='INF4-C008' else 'E021'

for cid in ['LIT4-C01','LIT4-C02','LIT4-C04']:add2('event_claims',event_id='LIT3-E001',claim_id=cid)

# Dated historical Ophir disclosures: preserve naming and transaction uncertainty.
add2('subjects',subject_id='E034',kind='entity',display_name='MEB INC (historical Ophir disclosure name)')
add2('entities',entity_id='E034',legal_name='MEB INC',entity_type='historical ownership-intermediary name placeholder',jurisdiction=None,inclusion_status='as_filed_name_identity_unresolved',note='Earlier Ophir ScheduleB name; relationship/equivalence to MEB NY INC E004 unresolved. No claim of a separately incorporated company or a legal rename.')
add2('relationships',relationship_id='EMP4-L01',source_subject_id='P001',target_subject_id='E034',relationship_type='OWNER as named in historical Ophir ScheduleB',effective_from=None,effective_to=None,ownership_min_percent=None,ownership_max_percent=None,upper_exclusive=None,evidence_status='verified_as_filed_name_identity_unresolved',claim_id='EMP4-C09',note='CRD4262671 owner row Entity in Which=MEB INC; retain as-filed spelling, do not silently join MEB NY INC.')
for rid,owner,lo,hi,exc,date,band in [
 ('EMP4-L02','E004',50,75,1,'2016-03-18','D'),
 ('EMP4-L03','E006',25,50,1,'2016-03-18','C'),
 ('EMP4-L04','E004',75,100,0,'2016-06-17','E')]:
 add2('relationships',relationship_id=rid,source_subject_id=owner,target_subject_id='E005',relationship_type='Ophir ScheduleB ownership-band disclosure snapshot',effective_from=None,effective_to=None,ownership_min_percent=lo,ownership_max_percent=hi,upper_exclusive=exc,evidence_status='verified_as_filed_snapshot_not_transaction_date',claim_id='EMP4-C08',note='Filing snapshot '+date+'; code'+band+' mapped using EMP4-C07 official legend. Older acquired-status field is not2016transaction date. No inferred current stake or sale terms.')
for rid,title,start,basis in [
 ('EMP4-R01','CEO','2012-04','Initial retrieved Ophir filing663868 submitted2012-08-30; acquired-status04/2012; not full employment interval.'),
 ('EMP4-R02','CEO, CCO',None,'Combined wording first appears among retrieved snapshots in884710 submitted2015-03-25; shared04/2012field does not independently date CCO start. CEO-only row in863218 submitted2015-02-20.')]:
 add2('roles',role_id=rid,person_id='P001',entity_id='E002',title=title,start_value=start,end_value=None,date_basis=basis,evidence_status='verified_historical_disclosure_snapshot',claim_id='EMP4-C05')
for ident,topic,resolution,cids in [
 ('EMP4-X-NAME','MEB INC and MEB NY INC historical naming mismatch','Earlier Ophir rows say MEB INC;2014-2016paired rows mix MEB NY INC/Finch with Bleich/MEB INC;June2016onward say MEB NY INC in both. No same-entity, typo,rename or succession conclusion.',['EMP4-C09']),
 ('EMP4-X-OWNERSHIP','Ophir intermediate ownership changes between filing snapshots','March18,2016 MEB NY/Finch codeD and NAYS codeC;June17 MEB NY codeE with no NAYS/Dror Niv row. Disclosure differences verified, transaction date/terms/economic exit not established.',['EMP4-C07','EMP4-C08'])]:
 add2('conflicts',conflict_id=ident,topic=topic,status='unresolved_legal_history_source_snapshots_retained',resolution=resolution)
 for cid in cids:add2('conflict_claims',conflict_id=ident,claim_id=cid)
for row in data['claims']:
 if row['claim_id'].startswith('EMP4-'):row['subject_id']='E002'

# Round4: disclosed administrative history, never classified as sanctions.
for pid,name,crd in [('P006','Jose Laurencio Marques','2850248'),('P007','James Pak','5491200'),('P008','Daniel Charles Lubin','2868633')]:
 add2('subjects',subject_id=pid,kind='person',display_name=name)
 add2('persons',person_id=pid,legal_name=name,crd=crd,identity_status='exact professional identifier in historical official firm disclosure',note='Professional capacity only; no private/family data or implied misconduct.')
for eid,name in [('E035','United Master Investment 2, LLC'),('E036','United Master, LLC'),('E037','United International Bank Corp')]:
 add2('subjects',subject_id=eid,kind='entity',display_name=name)
 add2('entities',entity_id=eid,legal_name=name,entity_type='historical disclosed ownership intermediary',jurisdiction=None,inclusion_status='official_as_filed_name_registry_ID_unresolved',note='Historical EntryPoint ScheduleB name. No name-only registry/LEI/bank licensing join or current-ownership conclusion.')
for ident,ent,value,cid,note in [
 ('EP5-ID-ERA','E003','802-125863','EP5-C001','Exact CRD313946 ERA reporting-file field2022-2024; not SEC registration.'),
 ('EP5-ID-OLDSEC','E003','801-122062','EP5-C004','Historical exactCRD EntryPoint withdrawal2021; distinct from later801-130798.'),
 ('EMP5-ID-OPHIRERA','E002','802-77010','EMP5-C03','ExactCRD164729 earlier ERA filing656739; not a separate firm or approval finding.')]:
 add2('identifiers',identifier_id=ident,entity_id=ent,scheme='SEC file',value=value,match_status=note,claim_id=cid)
for rid,src,dst,kind,lo,hi,exc,cid,note in [
 ('EP5-L01','E035','E011','MEMBER CodeC',25,50,1,'EP5-C007','Status acquired03/2021; historical March2023-June2024 filing snapshots.'),
 ('EP5-L02','E036','E035','SOLE MEMBER CodeE',75,100,0,'EP5-C007','Title and band retained separately; status12/2020.'),
 ('EP5-L03','E037','E036','SOLE MEMBER CodeE',75,100,0,'EP5-C007','No registry identity or bank-license conclusion; status12/2020.'),
 ('EP5-L04','E018','E037','OWNER CodeE',75,100,0,'EP5-C007','Professional corporate-ownership chain only; status12/2020.'),
 ('EP5-L05','E019','E018','TRUSTEE CodeF',None,None,None,'EP5-C007','No numerical beneficial ownership inferred from trustee role orCodeF.'),
 ('EP5-L06','P006','E003','OWNER CodeB',10,25,1,'EP5-C008','May12,2022 ScheduleA snapshot; reported status10/2020.'),
 ('EP5-L07','P007','E003','CFO,CCO,OWNER CodeNA',0,5,1,'EP5-C008','May12,2022 ScheduleA snapshot; NA<5% per legend, not exact stake.'),
 ('EP5-L08','P008','E003','OWNER CodeB',10,25,1,'EP5-C008','May12,2022 direct-owner snapshot; later GP-member row is distinct.'),
 ('EP5-L09','P008','E011','MEMBER CodeC',25,50,1,'EP5-C008','March2023 and later historical ScheduleB snapshots; no transaction-date inference.')]:
 add2('relationships',relationship_id=rid,source_subject_id=src,target_subject_id=dst,relationship_type=kind,effective_from=None,effective_to=None,ownership_min_percent=lo,ownership_max_percent=hi,upper_exclusive=exc,evidence_status='verified_as_filed_historical_snapshot',claim_id=cid,note=note+' No current ownership, exact wealth or legal transition date is established.')
for rid,pid,eid,title,start,basis,cid in [
 ('EMP5-R01','P001','E002','CEO','2012-04','Earlier ERA656739 submitted2012-08-01; acquired-status field04/2012, not a new hiring date.','EMP5-C03'),
 ('EP5-R01','P001','E002','CCO signatory and professional books/records custodian',None,'ADV-W signed2017-06-23/filed2017-06-29; not employment end or legal dissolution.','EP5-C005'),
 ('EP5-R02','P007','E003','CFO, CCO, OWNER','2020-10','Status-acquired field inMay2022 ERA snapshot; not full employment interval.','EP5-C008')]:
 add2('roles',role_id=rid,person_id=pid,entity_id=eid,title=title,start_value=start,end_value=None,date_basis=basis,evidence_status='verified_as_filed_role_observation',claim_id=cid)
for ev,eid,case,day,cid,disp,note in [
 ('EP5-W01','E003','1583338','2021-12-10','EP5-C004','Full ADV-W: continued business; newly formed adviser eligibility reason','Self-reported reason under801-122062; no sanction or corporate closure conclusion.'),
 ('EP5-W02','E002','1123733','2017-06-29','EP5-C005','Full ADV-W: advisory activity reportedly ceased2017-06-23','SignatureJune23; filingJune29. No legal dissolution or individual departure date.'),
 ('EP5-W03','E021','1398407','2020-03-21','EP5-C006','Full ADV-W: advisory activity continuing under an exemption','Not business closure; exact later exemption/operating history unresolved. Bleich affiliation unverified.')]:
 add2('events',event_id=ev,respondent_entity_id=None,claimant_entity_id=None,event_type='administrative_adviser_withdrawal_filing',authority='SEC hosted firm Form ADV-W',case_number='ADV-W FilingID'+case,initiated_date=day,resolution_date=None,fine_amount=None,currency=None,disposition=disp,personal_sanction_attribution='No disciplinary or personal sanction inferred.',note='Subject entity'+eid+' via linked claim. Filing date, not adjudication/effective withdrawal. '+note)
 add2('event_claims',event_id=ev,claim_id=cid)
for num,metric,val in [
 (1,'adviser_balance_sheet_total_assets_reported','1261506'),
 (2,'adviser_balance_sheet_current_liabilities_reported','986536'),
 (3,'adviser_balance_sheet_long_term_debt_to_others_reported','568700'),
 (4,'adviser_balance_sheet_shareholder_equity_reported','-293731'),
 (5,'adviser_balance_sheet_total_liabilities_and_equity_reported','1261505')]:
 add2('financial_observations',observation_id='EP5-INF-F'+str(num),entity_id='E021',metric=metric,amount=val,currency='USD',unit='dollars',measurement_date=None,measurement_date_basis='ADVW ScheduleW2FilingID1398407; measurement date not established. One-dollar total imbalance retained. Adviser-company values, not fundRAUM/personal assets; no legal insolvency finding.',filing_date='2020-03-21',evidence_status='as_filed_arithmetic_discrepancy_quarantined',claim_id='EP5-C010')
for num,day,val in [(1,'2022-05-12','30000000'),(2,'2023-03-29','32000000'),(3,'2023-05-22','32000000'),(4,'2023-11-22','32000000'),(5,'2024-03-27','208336695')]:
 add2('financial_observations',observation_id='EP5-ERA-F'+str(num),entity_id='E003',metric='ERA_2B_private_fund_assets_field',amount=val,currency='USD',unit='dollars',measurement_date=None,measurement_date_basis='Exact ERA2B-Assets field; filing date is not independently verified measurement date. Distinct from fundGAV/firmRAUM/personal income.',filing_date=day,evidence_status='verified_as_filed_specific_ERA_field',claim_id='EP5-C011')
for row in data['conflicts']:
 if row['conflict_id']=='INF4-X-ENTRYPOINT':
  row['status']='procedural_flag_ambiguity_resolved_legal_history_partly_open'
  row['resolution']='Added2021ADV-W,2022-2024ERA history802-125863 and officialGeneralInstruction15: dualfinalERA/initialSECflags are consistent with described transition. Reported nameupdate verified, but corporate legal-name date, fullapprovalhistory and compliance/timeliness remain unadjudicated. SeeEP5-C001-C004.'
add2('conflict_claims',conflict_id='INF4-X-ENTRYPOINT',claim_id='EP5-C003')
add2('conflict_claims',conflict_id='INF4-X-ENTRYPOINT',claim_id='EP5-C004')
for ident,topic,resolution,cids in [
 ('EP5-X-INFBALANCE','Inferent withdrawal balance-sheet total difference','ADVW1398407W2 reports assets1261506 versus liabilities/equity1261505. One-dollar difference, negative reported equity and unknown measurement date preserved; no corrected figure or insolvency finding.',['EP5-C010']),
 ('CORP5-X-MEBCHANGE','MEB2009change is process-address data, not rename proof','NY dataset amendmentflag identifies processaddress change; no entitynameflag. Datasetdisclaimer and missingcertificate/ownerIDbridge retained.',['CORP5-C001','CORP5-C003','CORP5-C004','CORP5-C005']),
 ('CORP5-X-BANK','United International Bank namesake not joined','GLEIF UnitedInternationalBankNV,CW,LEI549300KNXGPJJTQC2Y92 is not linked to historicalUnitedInternationalBankCorp; no identity/licensing inference.',['CORP5-C008'])]:
 add2('conflicts',conflict_id=ident,topic=topic,status='unresolved_or_rejected_identity_inference',resolution=resolution)
 for cid in cids:add2('conflict_claims',conflict_id=ident,claim_id=cid)
for row in data['claims']:
 cid=row['claim_id']
 if cid.startswith('EMP5-'):row['subject_id']='E021' if cid in ['EMP5-C05','EMP5-C06'] else 'P001'
 if cid.startswith('CORP5-') and cid in ['CORP5-C001','CORP5-C002','CORP5-C003','CORP5-C004','CORP5-C005','CORP5-C006']:row['subject_id']='E004'
 if cid=='CORP5-C008':row['subject_id']='E037'
