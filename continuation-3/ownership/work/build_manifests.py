
from pathlib import Path
import json,hashlib,datetime
root=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records')
out=root/'continuation-3/ownership'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sources=read(out/'request-log.json')
meta=read(out/'raw/scout-submissions.json')['filings']['recent']
for s in sources:
 s['authority']='SEC'
 s['title']=s['source_id'].replace('CORP4-','')
 if s['source_id'] in ['CORP4-SCOUT2013-ANNUAL','CORP4-SCOUT2009-ANNUAL']:
  film='14048639' if '2013' in s['source_id'] else '10027661';i=meta['filmNumber'].index(film)
  s.update(accession_id=meta['accessionNumber'][i],filing_date=meta['filingDate'][i],period_end=meta['reportDate'][i],film_number=film)
 s['preservation_note']='Original HTTP response bytes; substantive only if official_original. Filing dates differ from EDGAR acceptance timestamps; both retained in submissions metadata.'
for ident,name,cls in [('CORP4-SEARCH','parallel-discovery.json','discovery_capture_not_case_evidence'),('CORP4-FETCH','parallel-scout-financials.json','provider_transform_of_official_and_third_party_pages_not_original')]:
 p=out/'raw'/name
 sources.append(dict(source_id=ident,url=None,file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),retrieved_at_utc=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),retrieval_timestamp_basis='local preservation time; actual provider acquisition times retained in payload',source_class=cls,authority='Parallel Search',title=name))
prior=read(root/'evidence-index.json')['tables']['documents']
for ident in ['id-finra-scout-151990','EVT-D002']:
 s=next(x for x in prior if x['document_id']==ident)
 sources.append(dict(source_id=ident,url=s['official_url'],file=s['file_path'],sha256=s['sha256'],retrieved_at_utc=s['retrieved_at_utc'],source_class=s['source_class'],authority=s['authority'],pdf_pages=s['pdf_pages'],preservation_note='Existing independently preserved investigation original reused; not legacy repository evidence'))
C=[]
def claim(n,statement,ev,status='verified_as_filed',subject='E001'):
 C.append(dict(claim_id='CORP4-C'+str(n).zfill(2),subject_id=subject,statement=statement,evidence_status=status,evidence=[dict(document_id=x[0],locator=x[1]) for x in ev]))
claim(1,'SEC submissions metadata identifies SCOUT TRADING, LLC as CIK0001474522 and associates its X-17A-5 filings with SEC file008-68420. That file number matches FINRA Scout CRD151990, establishing the CIK-to-firm join.',[('CORP4-SCOUT-SUBMISSIONS','cik,name,filings.recent.fileNumber/form/filmNumber'),('id-finra-scout-151990','physical page5; CRD151990 SEC8-68420')])
claim(2,'Scout FY2009 original oath names Michael Bleich, with handwritten title member; FY2013 oath names Michael Bleich, with handwritten managing member. These are filing capacities, not role-start or signature dates. Subject linkage is supported by the same firm and FINRA full-name/CRD role record.',[('CORP4-SCOUT2009-ANNUAL','physical page2; title visually checked'),('CORP4-SCOUT2013-ANNUAL','physical page2; title visually checked'),('id-finra-scout-151990','physical pages6,8')],status='verified_oath_content_subject_join_supported_by_official_firm_record',subject='P001')
claim(3,'Scout FY2012 audited note states NAYS LLC and MEB NY Inc owned Scout until August31,2012; as of that date Finch LLC became its100% owner, and Finch was owned by NAYS LLC and MEB NY Inc. The note does not specify their respective Finch percentages, incorporation IDs, or ownership inception dates.',[('CORP4-SCOUT-2012-X-17A-5','physical page6, printed page7, Note1; visually checked')])
claim(4,'Scout FY2013 audited Note1 states Scout is wholly owned by Finch LLC and trades its own funds without holding customer balances. This corroborates the direct parent relationship at December31,2013; it does not establish Finch ultimate ownership percentages.',[('CORP4-SCOUT2013-ANNUAL','physical page7, printed page3, Note1')])
claim(5,'Scout FY2013 Note5 reports repayment of USD5,000,000 of subordinated debt plus any unpaid interest to NAYS LLC on October8,2013. It separately reports a USD4,000,000 subordinate note due2014 at10% per year to an unnamed member. Do not assign the remaining note to NAYS, MEB or Bleich without another record. These are corporate financing facts, not personal income or regulatory penalties.',[('CORP4-SCOUT2013-ANNUAL','physical page11, printed page7, Note5; repayment day8 visually checked')])
claim(6,'Scout FY2012 note gives August31,2012 for the100% Finch ownership transition. FINRA BrokerCheck gives August2012 in ownership schedules and June1,2012 effective date for common-control narrative stating Finch owns Scout and Ophir100%. The dates are preserved separately; no assumption resolves their different timing or meanings.',[('CORP4-SCOUT-2012-X-17A-5','physical page6, Note1'),('id-finra-scout-151990','physical pages6,8,15')],status='unresolved_source_chronology')
claim(7,'The FY2009 original and amendment describe Scout as a FINRA member; FINRA May2016 disciplinary bulletin describes Scout as a Nasdaq member but not a FINRA member in a passage about the separate April7,2015 proceeding. The sentence does not independently establish its membership status throughout the earlier conduct period. The records have different contexts. Historical membership changes or filing error have not been resolved; neither a contradiction nor membership continuity is established.',[('CORP4-SCOUT2009-ANNUAL','physical page10, Note1'),('CORP4-SCOUT-2009-X-17A-5-A','physical page7, Note1'),('EVT-D002','physical page43; paragraph about separate April7,2015 proceeding')],status='unresolved_historical_membership_statements')
claim(8,'Scout FY2009 facing page lists reporting period February5-December31,2009; FINRA reports Delaware establishment May20,2009. The report-period start is not treated as incorporation, employment or regulatory registration start.',[('CORP4-SCOUT2009-ANNUAL','physical page1; period visually checked'),('id-finra-scout-151990','physical page5; date established')],status='date_types_kept_distinct')
claim(9,'Six original annual-report PDFs were recovered: FY2009 original and amendment, and FY2010,2011,2012,2013. Official SEC metadata links their film numbers, filing dates, report dates and accession numbers. The current metadata response also lists one Scout13F-HR accession0001474522-14-000008 filedFebruary14,2014 forDecember31,2013; the attempted original13Fcover returned403 and no holdings conclusion is drawn.',[('CORP4-SCOUT-SUBMISSIONS','filings.recent all9rows; eight paper forms and one13F'),('CORP4-SCOUT-2013-13F-HR','preserved403response; access failure only')],status='verified_metadata_and_bounded_retrieval')
write=lambda p,v:p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
write(out/'sources.json',sources);write(out/'claims.json',C)
logs=[dict(source_system='Parallel Search',query=['Scout Trading 68420 annual report','site:sec.gov Scout Finch financial','site:sec.gov Bleich MEB ownership'],result='Official Scout FINRA report and third-party CIK lead; SEC metadata later independently verified CIK',source_id='CORP4-SEARCH'),dict(source_system='Parallel Search fetch',query=['https://www.sec.gov/Archives/edgar/vprr/1404/14048639.pdf','https://companiesbio.com/CIK-0001474522-company-scout-trading-llc-info.html'],result='Transformed official FY2013 extract and third-party filing lead; original annual PDFs retrieved separately',source_id='CORP4-FETCH')]
logs += [dict(source_system='SEC direct public GET',query=x['url'],retrieved_at_utc=x['retrieved_at_utc'],result=x.get('http_status',x.get('error')),source_id=x['source_id']) for x in read(out/'request-log.json')]
write(out/'search-log.json',logs)
report="""# Scout ownership and annual-report continuation

The original SEC annual reports now establish a dated corporate transition. Scout's FY2012 Note1 (physical page6, printed page7) says NAYS LLC and MEB NY Inc owned Scout until August31,2012, when Finch LLC became its100% owner. It says NAYS and MEB owned Finch, but supplies neither percentages nor corporate registry IDs. This is an as-filed statement in audited financial statements, not an SEC adjudication.

The FY2013 original corroborates Finch as sole parent (physical page7). Its Note5 (physical page11) reports USD5million principal plus unpaid interest repaid to NAYS on October8,2013. A separate USD4million remaining note is owed to an unnamed member; no identity is assigned to that lender. These corporate payments are not Bleich's personal income.

Bleich signs the FY2009 oath as member and FY2013 oath as managing member (physical page2 in each). Those capacities support the established Scout relationship but do not yield an employment start date.

All six PDFs listed below are original SEC response bytes; hashes, retrieval UTC, official URLs and accession/period metadata are in sources.json. No legacy repository document was consulted. Third-party material only supplied a CIK/film-number lead; official SEC submissions independently matched Scout's SEC file number to FINRA.

| Report | Accession | SEC filing date | Film | Physical pages |
|---|---|---|---|---|
"""
for s in sources:
 if s.get('pdf_pages') and s['source_id'].startswith('CORP4-'):
  report+=f"| {s.get('period_end')} {s.get('form','X-17A-5')} | {s.get('accession_id')} | {s.get('filing_date')} | {s.get('film_number')} | {s['pdf_pages']} |\n"
report+="""
Three source qualifications remain explicit. First, August31,2012 in the audited note differs from the June1,2012 effective date accompanying BrokerCheck's common-control description; the ownership schedules say August2012. No effective-date reconciliation is assumed. Second, FY2009 originals call Scout a FINRA member, while the2016 FINRA bulletin describes it as a Nasdaq member but not FINRA in a passage about a separate April7,2015 proceeding. That sentence does not date nonmembership throughout the earlier conduct period; no membership-change history is established. Third, the FY2009 report starts its period February5,2009 whereas FINRA gives establishment May20,2009; neither date is used as Bleich's employment start.

SEC metadata discloses a Scout13F-HR for December31,2013. Its original cover request returned403, so it is indexed as metadata and an access failure, with no holdings or value claim. The FY2009 amendment is preserved separately; no unstated reason for amendment or blanket supersession of all original financial statements is assumed.

The ownership path is stronger, but exact current stakes, the registry-number joins, and the unverified Inferent affiliation remain open. The source statement about no customer balances is limited to the report context; it is not a general compliance conclusion.
"""
(out/'report.md').write_text(report,encoding='utf-8')
print(json.dumps({'sources':len(sources),'claims':len(C),'search_logs':len(logs)}))

