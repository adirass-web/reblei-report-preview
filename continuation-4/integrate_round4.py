
from pathlib import Path
p=Path('work/build_continuation.py');s=p.read_text(encoding='utf-8')
old="+[('continuation-3',x) for x in ['inferent','employment','ownership','award-followup']]:"
new="+[('continuation-3',x) for x in ['inferent','employment','ownership','award-followup']]+[('continuation-4',x) for x in ['entrypoint-history','employment-inferent','corporate-identity','investment-litigation']]:"
assert old in s;s=s.replace(old,new)
s+='''
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
'''
p.write_text(s,encoding='utf-8')
p=Path('work/build_index.py');s=p.read_text(encoding='utf-8').replace('baseline and three continuation source/index reviews','baseline and four continuation source/index reviews');p.write_text(s,encoding='utf-8')
print('Round4 integration added; rebuild after final source QA.')

