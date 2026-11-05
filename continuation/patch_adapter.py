from pathlib import Path
p=Path('work/build_continuation.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace('new_claims=set(); raw_claims=[]; branches={}','new_claims=set(); raw_claims=[]; branches={}; failed_sources={}')
s=s.replace("or x.get('page_count'),retrieved_at_utc", "or x.get('page_count') or (x.get('physical_pages') if isinstance(x.get('physical_pages'),int) else None),retrieved_at_utc")
s=s.replace("  add2('retrieval_attempts'", "  if docid is None:failed_sources[old]=folder/'sources.json'\n  add2('retrieval_attempts'")
s=s.replace("'locator':x.get('locator'),'physical_pages'", "'locator':x.get('locator') or '; '.join(x.get('locators',[])),'physical_pages'")
s=s.replace("did=e.get('document_id') or e.get('source_id');assert did in aliases,('unresolved evidence',cid,did)","""did=e.get('document_id') or e.get('source_id')
   if did not in aliases and did in failed_sources:
    fp=failed_sources[did]; lid='CONT-REQUEST-LOG-'+branch
    if not any(r['document_id']==lid for r in data['documents']):
     add2('documents',document_id=lid,authority='researcher retrieval log',title=branch+' request log',document_type='JSON request metadata',source_class='request_log_not_original_case_record',official_url=None,file_path=fp.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(fp.read_bytes()).hexdigest(),filing_date=None,period_end=None,accession_id=None,pdf_pages=None,retrieved_at_utc=None,preservation_status='Researcher request log; no claim that failed original was saved',metadata_json=json.dumps({'purpose':'Documents failed requests only'}))
    aliases[did]=lid;e['locator']='sources.json record '+did+'; '+str(e.get('locator',''))
   assert did in aliases,('unresolved evidence',cid,did)""")
s=s.replace("rows2(logs,'batches','search_logs','searches')","rows2(logs,'batches','search_logs','searches','logs')")
s=s.replace("x.get('provider') or x.get('database')", "x.get('provider') or x.get('service') or x.get('database')")
s=s.replace("or x.get('timestamp_utc') or (logs.get('prepared_at_utc')", "or x.get('timestamp_utc') or (logs.get('logged_at_utc') or logs.get('prepared_at_utc')")
# Add candidate IDs and bounded relationships using already evidenced claims.
s += '''\n# New corporate IDs remain provisional mappings to regulatory names.\nfor entity,scheme,value,cid in [
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
'''
p.write_text(s,encoding='utf-8')
