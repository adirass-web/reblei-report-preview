
from pathlib import Path
import json,hashlib,datetime
R=Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records');O=R/'continuation-4/entrypoint-history'
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
sources=read(O/'direct-sources.json')
def add(ident,p,url,cls,at=None,**meta):
 p=Path(p);p=p if p.is_absolute() else R/p
 sources.append(dict(source_id=ident,file=p.relative_to(R).as_posix(),url=url,source_class=cls,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),retrieved_at_utc=at,**meta))
bulkurl='https://www.sec.gov/files/adv-filing-data-20111105-20241231-part1.zip';wurl='https://www.sec.gov/files/advw-20001019-20241231.zip'
for label,ident in [('era-base','EP5-ERA-BASE'),('era-schedule-ab','EP5-ERA-AB')]:
 m=read(O/'raw'/(label+'-verification.json'))
 add(ident,m['compressed_member_file'],bulkurl,'official_original_zip_local_member',m['completed_at_utc'],archive_member=m['member'],verification_file='continuation-4/entrypoint-history/raw/'+label+'-verification.json',uncompressed_sha256=m['uncompressed_sha256'],preservation_note='Exact compressed original; expanded cache outside evidence package; all range slices retained through offsets and hashes.')
for i,ident in enumerate(['EP5-ADVW-MAIN','EP5-ADVW-W15','EP5-ADVW-W18','EP5-ADVW-W2']):
 m=read(O/'raw'/('advw-'+str(i)+'-verification.json'))
 add(ident,O/'raw'/m['file'],wurl,'official_original_csv_payload_from_archive',m['requests'][-1]['completed_at_utc'],archive_member=m['member'],verification_file='continuation-4/entrypoint-history/raw/advw-'+str(i)+'-verification.json',locator_convention='csv_record_ordinal counts header as row1; exact key fields also provided')
 add(ident+'-COMPRESSED',O/'raw'/('advw-'+str(i)+'-member.bin'),wurl,'official_original_zip_local_member',m['requests'][-1]['completed_at_utc'],archive_member=m['member'])
for ident,name,parent in [
 ('EP5-ERA-BASE-SELECT','entrypoint-era-base-selected.json','EP5-ERA-BASE'),
 ('EP5-ERA-AB-SELECT','entrypoint-era-ab-selected.json','EP5-ERA-AB'),
 ('EP5-ERA-TYPES-SELECT','entrypoint-era-filing-types.json','EP5-REF-FILINGTYPES'),
 ('EP5-ADVW-MAIN-SELECT','raw/ADVW_20001019_20241231-selected.json','EP5-ADVW-MAIN'),
 ('EP5-ADVW-W18-SELECT','raw/ADVW_W1_8_20001019_20241231-selected.json','EP5-ADVW-W18'),
 ('EP5-ADVW-W2-SELECT','raw/ADVW_W2_20001019_20241231-selected.json','EP5-ADVW-W2')]:
 add(ident,O/name,None,'derived_target_only_table_extract',derived_from=parent,locator_convention='csv_record_ordinal is header-inclusive row number; literal field values retained. DatesSubmitted timezone unspecified.')
idx=read(R/'evidence-index.json')['tables']['documents']
for ident,file in [
 ('EP5-REF-FILINGTYPES','continuation-3/inferent/raw/ADV_Filing_Types_20111105_20241231.csv'),
 ('EP5-REF-IA-BASE','continuation-3/inferent/raw/IA_ADV_Base_A_20111105_20241231.zip-member.bin'),
 ('EP5-REF-OPHIRADV','evidence/id-sec-ophir-164729-adv.pdf'),
 ('EP5-REF-INFERENTADV','evidence/lead-inferent-292027-adv.pdf'),
 ('EP5-REF-PART1-DIR','continuation-3/inferent/raw/part1bulk-directory.bin')]:
 d=next(x for x in idx if x['file_path']==file)
 add(ident,file,d['official_url'],d['source_class'],d['retrieved_at_utc'],pdf_pages=d.get('pdf_pages'),reused_from=d['document_id'])
for p in sorted((O/'raw').glob('parallel-*.json')):
 add('EP5-'+p.stem.upper(),p,None,'provider_search_or_transform_capture_not_original',datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),timestamp_basis='local preservation time; provider acquired_at retained separately in payload')
for stem in ['advw-eocd','advw-directory']:
 m=read(O/'raw'/(stem+'.request.json'))
 if m.get('file'):add('EP5-'+stem.upper(),O/'raw'/(stem+'.bin'),wurl,'official_original_archive_byte_range',m['completed_at_utc'],request=m)
claims=[]
def c(n,sub,text,ev,status='verified_as_filed'):
 claims.append(dict(claim_id='EP5-C'+str(n).zfill(3),subject_id=sub,statement=text,evidence_status=status,evidence=[dict(document_id=x,locator=y) for x,y in ev]))
c(1,'E003','Exact CRD313946 yields six ERA Base rows: FilingIDs1649417 (2022-05-12),1720321 (2023-03-29),1763200 (2023-05-22),1782387 (2023-11-22),1834697 (2024-03-27),1869875 (2024-06-27). First five show SEC802-125863; last shows801-130798 and also appears in the IA table. These are filing snapshots, not six registrations.',[('EP5-ERA-BASE','1E1=313946; six exact FilingIDs; 1D,DateSubmitted'),('EP5-ERA-BASE-SELECT','all six header-inclusive CSV row ordinals'),('EP5-REF-FILINGTYPES','exact six FilingIDs: initial ERA, annual ERA, other amendments, final ERA+initial SEC')])
c(2,'E003','The May12,2022 ERA row retains ENTRYPOINT CAPITAL in1A/1B1 while1C-Legal and1C-Business areY and1C-New Name isENTRYPOINT CAPITAL, LLC. Later ERA rows use the LLC name. The December2021 withdrawal already used ENTRYPOINT CAPITAL, LLC. Thus the record documents a reported name update, not a proved May2022 corporate legal-name change date or separate legal entity.',[('EP5-ERA-BASE','FilingID1649417 fields1A/1B1/1C; later rows'),('EP5-ADVW-MAIN','FilingID1583338 Full Legal Name')],status='verified_reported_name_update_legal_history_not_resolved')
c(3,'E003','FilingID1869875 marks both Initial SEC Registration Request and Final SEC ERA Report Y. Official Form ADV General Instruction15 describes submitting the final ERA report and SEC registration application in the same filing. Coupled with the preceding ERA history, the dual flags are consistent with a reporting-to-registration transition, not by themselves a filing contradiction. This does not adjudicate eligibility, deadlines, regulatory approval or corporate succession.',[('EP5-REF-FILINGTYPES','FilingID1869875 exact header fields; leading space in Final SEC ERA header preserved'),('EP5-ERA-BASE','preceding CRD313946 ERA rows'),('EP5-adv-instructions2016','physical PDFpage9, General Instruction15'),('EP5-instructions2024','physical PDFpage9, General Instruction15; revision07-24')],status='clearly_labeled_official_record_procedural_inference')
c(4,'E003','EntryPoint ADV-W FilingID1583338 filedDecember10,2021 under SEC801-122062/CRD313946 reports Business Ceased=N. Its stated withdrawal reason is registration as a newly formed adviser under the120-day rule followed by failure to meet eligibility criteria for continued registration. James Pak signs as CFO/CCO onDecember10. This is a firm-filed administrative withdrawal explanation, not a disciplinary sanction or a finding that the business closed.',[('EP5-ADVW-MAIN','exact FilingID1583338; Filing Date, SEC File Number, Business Ceased, Reasons for Withdrawal, signature fields'),('EP5-ADVW-MAIN-SELECT','EntryPoint selected row')])
c(5,'E002','Ophir ADV-W FilingID1123733 filedJune29,2017 reports advisory business ceasedJune23,2017 and no longer conducting advisory activities. Michael Bleich signs as CCO onJune23; the contact title isCEO. ScheduleW1.8 identifies him as custodian/location name for required adviser books and records. These observations do not establish legal dissolution or his personal departure date.',[('EP5-ADVW-MAIN','FilingID1123733; header-inclusive row13611'),('EP5-ADVW-W18','FilingID1123733; header-inclusive row17124; custodian and Description fields')])
c(6,'E021','Inferent ADV-W FilingID1398407 filedMarch21,2020 reports Business Ceased=N and continuation of advisory activities relying on an exemption from registration. Marc Rieffel signs as CCO/CTO. The filing is evidence against treating the registration withdrawal itself as business closure; it does not identify Bleich as an employee or establish the exact exemption or subsequent operations.',[('EP5-ADVW-MAIN','FilingID1398407; Business Ceased, Reasons for Withdrawal, signature fields')])
c(7,'E003','Historical EntryPoint ERA ScheduleB records disclose United Master Investment2,LLC as a CodeC member of EntryPoint GP; United Master,LLC as its CodeE sole member; United International Bank Corp as CodeE sole member of United Master; Richard A.Desich Irrevocable2005SDTrust as CodeE owner of United International Bank Corp; and South Dakota Trust Company as trustee CodeF. These dated March2023-June2024 snapshots add historical intermediaries, not verified current corporate IDs or exact economic entitlements.',[('EP5-ERA-AB','FilingIDs1720321,1763200,1782387,1834697,1869875; exact named ScheduleB rows'),('EP5-ERA-AB-SELECT','matching rows/ordinals'),('EP5-REF-OPHIRADV','physicalpages19-20 codelegend; C25%-<50%,E75%+,Fother')])
c(8,'E003','The May2022 EntryPoint ERA ScheduleA names Jose Laurencio Marques CRD2850248 as OWNER CodeB, James Pak CRD5491200 as CFO/CCO/OWNER CodeNA, and Daniel Charles Lubin CRD2868633 as OWNER CodeB. Later snapshots describe Lubin as CodeC member of EntryPoint GP. A disclosed role/ownership band is not an exact payment or wealth figure; omission from a later snapshot alone does not prove a complete economic exit.',[('EP5-ERA-AB','FilingID1649417 ScheduleA; FilingID1720321 and later ScheduleB Lubin rows'),('EP5-ERA-AB-SELECT','professional names/OwnerID and role/status fields'),('EP5-REF-OPHIRADV','physicalpage19 ScheduleA legend; B10%-<25%,NA<5%')])
c(9,'E021','The exact CRDs for Jose Marques2850248 and James Pak5491200 occur in Inferent2019 and EntryPoint2022 professional records. This establishes disclosed professional overlap for those individuals. It does not prove Bleich employment at Inferent, a merger, a transfer of clients or a corporate succession.',[('EP5-REF-INFERENTADV','physicalpages29-30 ScheduleA/B; exact names and CRDs'),('EP5-ERA-AB','FilingID1649417 OwnerID2850248/5491200')],status='verified_common_professional_identifiers_no_merger_inference')
c(10,'E021','Inferent ADV-W ScheduleW2 for FilingID1398407 reports total assetsUSD1,261,506, total current liabilitiesUSD986,536, long-term debt to othersUSD568,700, total shareholder equityUSD-293,731, and total liabilities/equityUSD1,261,505. Reported sides differ byUSD1. Preserve all figures without correction. The table does not establish the balance-sheet measurement date; these are adviser-company figures, not fundRAUM, Bleich personal finances or a legal insolvency finding.',[('EP5-ADVW-W2','FilingID1398407; header-inclusive row2816; named Assets/Liabilities/Equity fields')],status='verified_as_filed_arithmetic_discrepancy_quarantined')
c(11,'E003','EntryPoint ERA field2B-Assets reportsUSD30,000,000 inMay2022; USD32,000,000 in the three2023 rows; USD208,336,695 inMarch2024. March2024 marks2B3=Y while earlier rows mark2B2=Y. These are the specific ERA private-fund-assets fields; no exact measurement date, fund-level allocation, personal income or compliance conclusion is inferred.',[('EP5-ERA-BASE','six CRD313946 rows;2B-Assets/2B2/2B3; lastJune2024blank'),('EP5-ERA-BASE-SELECT','literal fields and filing dates')],status='verified_specific_ERA_asset_field_measurement_date_unknown')
for x in sources:
 if 'authority' not in x:x['authority']='SEC' if x.get('url') and 'sec.gov' in x['url'] else 'researcher/provider; see source_class'
 if 'title' not in x:x['title']=Path(x.get('file',x['source_id'])).name
ids={x['source_id'] for x in sources};assert len(ids)==len(sources)
for x in claims:
 for e in x['evidence']:assert e['document_id'] in ids,e
for x in sources:
 if x.get('file'):assert hashlib.sha256((R/x['file']).read_bytes()).hexdigest()==x['sha256'],x
write=lambda p,v:p.write_text(json.dumps(v,indent=2,ensure_ascii=False),encoding='utf-8')
write(O/'sources.json',sources);write(O/'claims.json',claims)
logs=[dict(source_system='Parallel Search',query=p.name,result='Provider capture retained; official original records independently retrieved where possible',file=p.relative_to(R).as_posix()) for p in sorted((O/'raw').glob('parallel-*.json'))]
logs += [dict(source_system='SEC direct retrieval',query=x.get('url'),retrieved_at_utc=x.get('retrieved_at_utc'),result=x.get('http_status',x.get('error')),source_id=x['source_id']) for x in read(O/'direct-sources.json')]
logs += [dict(source_system='SEC archive range retrieval',query=read(p).get('url'),searched_at_utc=read(p).get('started_at_utc'),result=read(p).get('http_status'),file=p.relative_to(R).as_posix()) for p in sorted((O/'raw').glob('*.request.json'))]
write(O/'search-log.json',logs)
report="""# Registration history, withdrawal records and historical ownership

This stage adds original ERA and ADV-W tables to the previously recovered registered-adviser data. All statements are attributed as filed. It does not adjudicate regulatory compliance or personal conduct.

## EntryPoint: the missing registration sequence

| Filing | What the original record reports |
|---|---|
| July12,2021,1542238 | Initial SEC application under801-122062 in the earlier IA table. |
| December10,2021,1583338 | Full ADV-W under801-122062. Business Ceased=N. The stated reason is failure to meet continued-registration eligibility after using the newly formed adviser120-day route. |
| May12,2022,1649417 | Initial ERA report,802-125863. Legal/business name-change fields report ENTRYPOINT CAPITAL, LLC, while the retained old-name fields read ENTRYPOINT CAPITAL. The LLC name already occurs in the December2021 withdrawal. |
| March29,2023; May22,2023; November22,2023; March27,2024 | Annual/other ERA amendments under802-125863. |
| June27,2024,1869875 | Initial SEC application AND final ERA report,801-130798. The same filing appears in both source families and must not be counted twice. |

The original2016 and July2024 Form ADV General Instructions, physical page9, describe a final ERA report and application for SEC registration in the same filing. The dual2024 flags are therefore consistent with that reporting transition. This closes the narrow procedural ambiguity, while legal entity history, the exact registration-approval history and any compliance/timeliness assessment still require their own evidence. No automatic conclusion follows about why every eligibility condition changed. See EP5-C001-C004.

## Ophir and Inferent withdrawals mean different things

Ophir's ADV-W1123733, filedJune29,2017, reports advisory activity ceasedJune23,2017. Michael Bleich signs as CCO onJune23 and is named the professional books-and-records custodian. The record is more specific than a registration termination date, but it does not establish corporate dissolution or Bleich's personal employment end. See EP5-C005.

Inferent's ADV-W1398407, filedMarch21,2020, expressly says it was continuing advisory activities while relying on an exemption. Business Ceased isN. Withdrawal alone should therefore not be presented as closure. The record still does not prove Bleich employment or identify the later exemption/operating history. See EP5-C006.

## Historical ownership and professional overlap

March2023-June2024 ERA records add a professional ownership chain: EntryPoint GP <- United Master Investment2 <- United Master <- United International Bank Corp <- Richard A.Desich Irrevocable2005SDTrust, with South Dakota Trust Company as trustee. Each edge retains its own role and ownership code. Exact incorporation/registry identifiers and present ownership remain unproved. Do not turn the trustee field into a numerical beneficial ownership percentage. See EP5-C007.

EntryPoint's May2022 record names Jose Marques, James Pak and Daniel Lubin in ownership/executive capacities. Marques and Pak share exact professional identifiers with the original2019 Inferent filing. That is verified individual overlap, not a Bleich employment or merger inference. The later Lubin GP-member disclosure is distinct from his earlier direct-owner row. See EP5-C008-C009.

## Financial observations with limits

EntryPoint's ERA2B-Assets fields progress from30million inMay2022 to32million in2023 and208,336,695 inMarch2024. These are the specific ERA private-fund-asset observations. Filing dates are not independently verified asset-measurement dates. They are not interchangeable with later firmRAUM or fund gross assets, and do not establish personal income. See EP5-C011.

Inferent's withdrawal balance sheet reports assets1,261,506 and liabilities plus equity1,261,505: a one-dollar discrepancy retained unchanged. Equity is reported as-293,731. The balance-sheet measurement date is not established by the retrieved table. No insolvency-law, misconduct or Bleich-personal-finance conclusion is made. See EP5-C010.

## Preservation and evidence navigation

sources.json and claims.json preserve exact URL, retained-byte SHA256, UTC retrieval, table/member and field locators. Archive member CRC32, sizes, local/central member names and reconstruction metadata were checked. Large ERA originals are preserved as exact compressed ZIP members; expanded work caches are separate. ADV-W original CSV payloads and their compressed members are retained. Target extracts are labeled derivatives.

CSV record ordinals count the header as row1; they are not zero-based data indices. FilingID and CRD are the primary joins. Source submission/signature timestamps have no supplied timezone and are not converted to UTC. Original retrieval timestamps are separately UTC. Full raw responses and failed requests are retained; a403 response is not substantive evidence. No legacy repository sources, private civil matters, NYSCEF, new account, fee or outreach were used.
"""
(O/'report.md').write_text(report,encoding='utf-8')
instructions="""# Instructions: remaining registration and ownership work

1. Obtain EntryPoint's complete2021 application, approval and withdrawal correspondence, then its2022 ERA and2024 transition filing/receipt history. Match CRD313946 and files801-122062,802-125863,801-130798. Reconcile filing, receipt, effective-registration and asset-measurement dates before any eligibility or deadline assessment. Do not infer a violation from this extract alone. Official IAPD/SEC originals are the completion gate; a regulator or firm request needs separate authorization.
2. Obtain EntryPoint's legal name-change/formation records and owner-linked registry documents. The May2022 reporting update and December2021 LLC name are not a corporate certificate. Confirm the legal entity and exact effective dates.
3. Obtain owner-linked records for United Master Investment2 LLC, United Master LLC and United International Bank Corp. Use the exact chain and dated filing IDs; do not merge similarly named banks by name alone. Certificates plus an authoritative ownership bridge are required.
4. Obtain Inferent's post-March2020 exemption basis and subsequent official reporting/registration history. The withdrawal says operations continued; absence from the recovered ERA table does not establish cessation or noncompliance.
5. Obtain the original supporting balance sheet or corrected withdrawal schedule for Inferent1398407. Establish its measurement date and reconcile the one-dollar total difference. Preserve the reported negative equity without a legal insolvency inference.
6. If needed, obtain Ophir's cessation/records-transfer documents and any subsequent business/asset-transfer instrument. ADV-W1123733 establishes only the reported cessation and custodian particulars, not a merger, dissolution or Bleich departure date.

These instructions identify missing records, not authorized requests to third parties. No accounts, purchases or contacts were made.
"""
(O/'remaining-instructions.md').write_text(instructions,encoding='utf-8')
print(json.dumps({'sources':len(sources),'claims':len(claims),'logs':len(logs)}))
