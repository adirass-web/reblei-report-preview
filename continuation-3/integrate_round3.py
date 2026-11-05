
from pathlib import Path
p=Path('work/build_continuation.py')
s=p.read_text(encoding='utf-8')
old="+[('continuation-2',x) for x in ['employment','inferent','ownership','litigation']]:"
new="+[('continuation-2',x) for x in ['employment','inferent','ownership','litigation']]+[('continuation-3',x) for x in ['inferent','employment','ownership','award-followup']]:"
assert old in s
s=s.replace(old,new)
s += '''
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
'''
p.write_text(s,encoding='utf-8')
p=Path('work/build_index.py');s=p.read_text(encoding='utf-8').replace('baseline and two continuation source/index reviews','baseline and three continuation source/index reviews');p.write_text(s,encoding='utf-8')
print('Round3 source integration and dated observations added; build awaits final specialist manifests.')

