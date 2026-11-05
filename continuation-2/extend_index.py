from pathlib import Path
p=Path('work/build_continuation.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("for branch in ['early-employment','corporate-ownership','inferent','investment-litigation']:\n folder=ROOT/'continuation'/branch", "for stage,branch in [('continuation',x) for x in ['early-employment','corporate-ownership','inferent','investment-litigation']]+[('continuation-2',x) for x in ['employment','inferent','ownership','litigation']]:\n folder=ROOT/stage/branch")
s=s.replace("origin_register='continuation/'+branch", "origin_register=stage+'/'+branch")
s=s.replace("branch+' request log'", "stage+'/'+branch+' request log'")
s=s.replace("lid='CONT-REQUEST-LOG-'+branch", "lid='REQUEST-LOG-'+stage+'-'+branch")
s=s.replace("raw_claims.append((branch,x))", "raw_claims.append((stage+'/'+branch,x))")
s=s.replace("if branch!='investment-litigation':continue", "if branch!='continuation/investment-litigation':continue")
s=s.replace("x.get('provider') or x.get('service') or x.get('database') or 'continuation/'+branch", "x.get('provider') or x.get('service') or x.get('database') or x.get('method') or stage+'/'+branch")
s=s.replace("x.get('queries') or x.get('query')", "x.get('queries') or x.get('search_queries') or x.get('query')")
s=s.replace("or x.get('timestamp_utc') or (logs.get", "or x.get('timestamp_utc') or x.get('logged_at_utc') or (logs.get")
s=s.replace("coverage_limit=x.get('coverage_limit') or 'Bounded", "coverage_limit=x.get('coverage_limit') or x.get('limits') or 'Bounded")
s=s.replace("'continuation specialist claim; bounded independent review in continuation/qa.md and qa-events.md'", "stage+' specialist claim; independent review scope in that stage QA reports'")
s+='''\n# Round2: one new arbitration, not another regulatory penalty.\nfor row in data['events']:row['claimant_entity_id']=None
for row in data['events']:
 if row['event_id']=='EVT-E005':
  row['case_number']='20100243866-02';row['resolution_date']='2016-02-25'
  row['disposition']='Nasdaq AWC accepted without admitting or denying findings and without adjudication; censure and joint FINRA/Nasdaq fine'
  row['note']='Original Nasdaq acceptance date2016-02-25. Joint fineUSD675000 includesUSD337500Nasdaq, not an additional fine. Sanctions effective date to be set byFINRAstaff; payment/undertaking completion not verified.'
add2('events',event_id='LIT3-E001',respondent_entity_id='E020',event_type='firm_arbitration_award_identity_join_inferred',authority='FINRA Office of Dispute Resolution',case_number='15-02816',initiated_date='2015-10-22',resolution_date='2016-11-18',fine_amount=None,currency='USD',disposition='Wedbush ordered to pay Scout damages,interest,filing-fee reimbursement; counterclaim and unspecified relief including attorneys fees denied.',personal_sanction_attribution='No Bleich party or personal sanction in award. ScoutCRD151990join probable inference from multiple officialrecords.',note='Resolution field uses FINRAindex/service date; signature dates2016-11-16. Legal date of award for interest unresolved. No payment,appeal,confirmation,vacatur or satisfaction verified.',claimant_entity_id='E001')
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
'''
p.write_text(s,encoding='utf-8')
p=Path('work/build_index.py');s=p.read_text(encoding='utf-8-sig');s=s.replace('respondent_entity_id TEXT REFERENCES entities(entity_id),event_type TEXT','respondent_entity_id TEXT REFERENCES entities(entity_id),claimant_entity_id TEXT REFERENCES entities(entity_id),event_type TEXT')
s=s.replace("'schema_version':1", "'schema_version':2")
s=s.replace("'independent_qa_scope':'specialist originals, brochures, 13F anomaly and bounded final normalized index second pass; see independent-qa.md, not every filing audited'", "'independent_qa_scope':'baseline and two continuation source/index reviews; see independent-qa.md and each continuation QA report. Not exhaustive court/history clearance.'")
p.write_text(s,encoding='utf-8')
