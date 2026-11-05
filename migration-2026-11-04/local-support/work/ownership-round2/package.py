import json, hashlib, datetime
from pathlib import Path
root=Path('outputs/ReBlei/investigations/2026-11-04-official-records')
p=root/'continuation-2/ownership'
e=p/'evidence'
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(f): return json.loads(f.read_text(encoding='utf-8-sig'))
def h(f): return hashlib.sha256(f.read_bytes()).hexdigest()
s=[]
for ln in ['download-log.json','gleif-download-log.json','gleif-more-log.json']:
 for r in read(e/ln):
  r['document_id']='CORP3-'+(r.get('file') or str(len(s))).split('.')[0]
  r['source_class']='official_registry_law_or_fee' if r['document_id'].startswith('CORP3-cayman') else 'official_GLEIF_public_API'
  r['failure_logs']=[] if not r.get('error') else [r['error']]
  if r.get('file'): r['file']=(e/r['file']).relative_to(root).as_posix()
  s.append(r)
for fn,u in [('cima-third-moment.html','https://www.cima.ky/search-entities-cima?AuthorizationType=All&Searching=Third%20Moment&ajax=Y'),('cima-third-underscore.html','https://www.cima.ky/search-entities-cima?Searching=Third_Moment&AuthorizationType=All&ajax=Y'),('cima-entrypoint.html','https://www.cima.ky/search-entities-cima?Searching=EntryPoint&AuthorizationType=All&ajax=Y')]:
 f=e/fn
 s.append({'document_id':'CORP3-'+f.stem,'url':u,'file':f.relative_to(root).as_posix(),'sha256':h(f),'retrieved_at_utc':datetime.datetime.fromtimestamp(f.stat().st_mtime,datetime.timezone.utc).isoformat(),'timestamp_basis':'file-write time from acquisition call; not server timestamp','source_class':'official_CIMA_public_search_response','failure_logs':['Response contains search controls, reCAPTCHA fields, table headers and no entity rows. A successful validated entity search is not established; do not treat as a negative search.']})
f=e/'sec-adv-archive-page.extract.json'; a=read(f)
s.append({'document_id':'CORP3-sec-adv-archive-page','url':a['url'],'file':f.relative_to(root).as_posix(),'sha256':h(f),'recorded_at_utc':a['recorded_at_utc'],'provider_acquired_at':a['provider_acquired_at'],'source_class':'official_SEC_page_provider_extraction','failure_logs':[]})
s.append({'document_id':'CORP3-sec-adv-part1-head','url':'https://www.sec.gov/files/adv-filing-data-20111105-20241231-part1.zip','file':None,'sha256':None,'attempted_on_utc':'2026-11-04','recorded_at_utc':now,'source_class':'official_SEC_archive_access_attempt','http_status':403,'failure_logs':['Direct HEAD returned 403 Forbidden. No archive bytes retrieved by this worker. Historical bulk work handed to parent/coordinating agent; not repeated here.']})
for f in e.glob('*.txt'):
 origin=e/(f.stem+'.pdf')
 s.append({'document_id':'CORP3-'+f.stem+'-text','url':next(x['url'] for x in s if x.get('file')==origin.relative_to(root).as_posix()),'file':f.relative_to(root).as_posix(),'sha256':h(f),'generated_at_utc':datetime.datetime.fromtimestamp(f.stat().st_mtime,datetime.timezone.utc).isoformat(),'source_class':'derived_text_from_preserved_official_PDF','derived_from':'CORP3-'+f.stem,'failure_logs':[]})
queries=[['EP Third Moment Cayman CIMA','Third Moment International Cayman Gazette','EntryPoint Cayman monetary authority'],['EP Fund GP EntryPoint SEC','OPEH Ophir Bleich SEC','EntryPoint GP Delaware file number'],['site:cima.ky Third Moment','site:gazettes.gov.ky Third Moment','site:gov.ky EP Third Moment'],['site:sec.gov Ophir Partners Finch','site:reports.adviserinfo.sec.gov Ophir Partners','site:sec.gov Bleich OPEH'],['site:cima.ky mutual funds list download','site:gov.ky gazette Third Moment','Cayman general registry company search fees'],['site.ciregistry.ky partnership search fee','Cayman General Registry search fee'],['Third Moment International gazette','Ophir Partners Beaufort gazette','EntryPoint Cayman partnership registration'],['SEC ADV Schedule B historical download','SEC adv filing data 2017 ownership'],['GLEIF EntryPoint Capital legal entity','GLEIF EP Third Moment','GLEIF Ophir Partners Finch']]
logs=read(p/'search-log.json')
for r,q in zip(logs,queries): r['search_queries']=q; r['result_treatment']='Discovery only. Non-official and namesake results are not evidence of a subject relationship.'
for r in s:
 if r['source_class']=='official_GLEIF_public_API':
  j=read(root/r['file']);r['locators']=['meta.pagination','data[].attributes.entity.legalName','data[].attributes.entity.registeredAs','data[].attributes.entity.jurisdiction'];r['result_total']=j['meta']['pagination']['total'];r['golden_copy_publish_date']=j['meta']['goldenCopy']['publishDate']
claims=[
 {'claim_id':'CORP3-C01','statement':'No subject-specific Cayman registration certificate, registration statement or CIMA entity record was obtained in this continuation. Empty CIMA response tables do not establish that the funds are unregistered.','status':'unresolved_access_limit','source_ids':['CORP3-cima-third-moment','CORP3-cima-third-underscore','CORP3-cima-entrypoint'],'locators':['HTML table header and recaptchaSE/hiddenRecaptcha fields']},
 {'claim_id':'CORP3-C02','statement':'Cayman Exempted Limited Partnership Act (2025 Revision) section 9 requires a filed statement naming general partners and supporting incorporation/registration documents for corporate/partnership GPs; subsection 9(2) makes records and filed statements open to public inspection, and section 12 permits any person to require certified certificates or registered statements for a fee.','status':'verified_general_official_record_scope','source_ids':['CORP3-cayman-elp-act-2025'],'locators':['Physical PDF pp10-12: s9(1)(e),s9(2),s9(5),s9(7),s10,s12(1)']},
 {'claim_id':'CORP3-C03','statement':'The exact outstanding Cayman proof is EP Third Moment International LP and Master Fund LP registration certificates plus original registered statements and subsequent GP/name changes. Those could resolve legal form and the GP corporate identifier if the required supporting corporate document is accessible; they would not automatically prove Bleich ultimate economic ownership.','status':'explicit_research_inference_record_target','source_ids':['CORP3-cayman-elp-act-2025'],'locators':['s9(1)(a),(d),(e),s9(5),(7),s10,s12; physical pp10-12']},
 {'claim_id':'CORP3-C04','statement':'The preserved official Cayman fee schedule quotes general search CI$30/US$36.59 and certification/copy CI$150/US$182.93. These are published individual service fees; no total order price is asserted and no service was purchased.','status':'verified_published_fee_snapshot','source_ids':['CORP3-cayman-elp-fee-schedule'],'locators':['Physical PDF p1 CERTIFICATION section12(1),p2 GENEAL SEARCH FEE and COPY OF DOCUMENT']},
 {'claim_id':'CORP3-C05','statement':'The eight preserved GLEIF legal-name filters supplied no responsive subject record. EntryPoint Solutions Oy (Finland), Third Moment Capital Pty Ltd (Australia), and Finch variants with different names/IDs are excluded rather than joined to the investigation. This is bounded database-query coverage, not proof that the target entities lack LEIs.','status':'verified_bounded_search_results','source_ids':['CORP3-gleif-entrypoint','CORP3-gleif-third-moment','CORP3-gleif-ophir','CORP3-gleif-ep-fund-gp','CORP3-gleif-finch-llc','CORP3-gleif-nays','CORP3-gleif-meb-ny','CORP3-gleif-opeh'],'locators':['meta.pagination.total;data[].attributes.entity legalName,registeredAs,jurisdiction']},
 {'claim_id':'CORP3-C06','statement':'The SEC official archive landing page supplies Form ADV Part1 bulk historical archives through December31,2024 and routes January2025 onward to IAPD. This worker could not inspect the 2011-2024 Part1 archive because a direct HEAD returned403. No new historical ownership change is established here.','status':'verified_archive_route_access_limited','source_ids':['CORP3-sec-adv-archive-page','CORP3-sec-adv-part1-head'],'locators':['Opening paragraph and Form ADV Part1 Data Files list; HEAD failure']}
]
for name,obj in [('sources.json',s),('claims.json',claims),('search-log.json',logs)]: (p/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
checks=[]
for r in s:
 if r.get('file'): checks.append({'document_id':r['document_id'],'sha256_verified':h(root/r['file']).lower()==r['sha256'].lower()})
assert all(x['sha256_verified'] for x in checks)
(p/'verification.json').write_text(json.dumps({'checked_at_utc':now,'source_count':len(s),'claim_count':len(claims),'checks':checks},indent=2),encoding='utf-8')
print(json.dumps({'sources':len(s),'claims':len(claims),'hashes_verified':len(checks)}))
