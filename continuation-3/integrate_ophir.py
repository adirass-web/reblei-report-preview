
from pathlib import Path
p=Path('work/build_continuation.py');s=p.read_text(encoding='utf-8')
s += '''
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
'''
p.write_text(s,encoding='utf-8');print('Ophir snapshots added, without invented transaction or role-start dates.')

