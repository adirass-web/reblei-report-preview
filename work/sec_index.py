import pathlib,json,hashlib,re,xml.etree.ElementTree as E,datetime
p=pathlib.Path('outputs/sec-sources.json'); docs=json.loads(p.read_text()); claims=[]
for d in docs:
 if d.get('status_code')!=200:d['record_class']='retrieval_attempt';continue
 d['record_class']='preserved_official_document';d['pdf_page_numbering']='physical, 1-based' if d.get('pdf_pages') else None
 f=pathlib.Path(d['file'])
 if f.suffix=='.txt':
  t=f.read_text();acc=re.search(r'ACCESSION NUMBER:\s*(\S+)',t);fd=re.search(r'FILED AS OF DATE:\s*(\d+)',t)
  if acc:d['accession_id']=acc[1];d['document_id']='SEC-SUB-'+acc[1]
  if fd:d['filing_date']=datetime.datetime.strptime(fd[1],'%Y%m%d').date().isoformat()
 elif f.suffix=='.pdf':
  d.update(document_id='SEC-ADV-313946-20261015',filing_date='2026-10-15',form='ADV Part 1A Other-Than-Annual Amendment',sec_number='801-130798',crd='313946',cik='1992519',derived_text_file=d['file']+'.txt',derived_text_sha256=hashlib.sha256(pathlib.Path(d['file']+'.txt').read_bytes()).hexdigest())
 elif 'submissions-' in f.name:d['document_id']='SEC-HISTORY-'+f.stem.split('-')[-1]
 d['claim_links']=[]

def claim(id,statement,docid,locator,status='verified_as_filed',**kw):
 c=dict(claim_id=id,statement=statement,document_id=docid,locator=locator,status=status,**kw);claims.append(c)
 for d in docs:
  if d.get('document_id')==docid:d.setdefault('claim_links',[]).append(id)
adv='SEC-ADV-313946-20261015'
claim('SEC-C001','EntryPoint Capital, LLC identifies firm CRD313946, SEC801-130798 and CIK1992519.',adv,'physical PDF p1; Item1A,D,E')
claim('SEC-C002','Michael Edward Bleich, CRD4262671, is listed as Chief Investment Officer with status acquired05/2023, control personY, ownership codeNA (less than5%).',adv,'physical PDF p26; ScheduleA')
claim('SEC-C003','Michael Edward Bleich is listed as member of EntryPoint GP LLC from07/2023, ownership codeC (25% to less than50%), control personY.',adv,'physical PDF p27; ScheduleB')
claim('SEC-C004','Michael Edward Bleich is listed as limited partner of EntryPoint Partners, LP from07/2023, codeC (25% to less than50%), control personY.',adv,'physical PDF p27; ScheduleB')
claim('SEC-C005','EntryPoint Partners, LP is listed as direct member of EntryPoint Capital from10/2020, codeE (75% or more), control personY.',adv,'physical PDF p26; ScheduleA')
claim('SEC-C006','EntryPoint GP LLC is listed with status GENERAL PARTNER from10/2020, codeNA, control personY. Retain designation as filed; do not conflate with EP Fund GP LLC.',adv,'physical PDF p26; ScheduleA')
claim('SEC-C007','EntryPoint reports total discretionary RAUMUSD999157153 across4 accounts, nondiscretionaryUSD0, and non-US client RAUMUSD533470137.',adv,'physical PDF p8; Item5F2a-f,5F3',measurement_date='2026-09-30',filing_date='2026-10-15',currency='USD',value=999157153,metric='firm_RAUM')
claim('SEC-C008','The filing expressly states regulatory assets under management are measured as of9/30/2026.',adv,'physical PDF p27; ScheduleD Miscellaneous')
claim('SEC-C009','EP Third Moment Master Fund, LP is listed as Cayman fund805-7203779905, with EP Fund GP, LLC and feeder funds EP Third Moment Fund, LLC805-8039696809 and EP Third Moment International, LP805-5004504749.',adv,'physical PDF pp15-17; ScheduleD7B1A1-7')
claim('SEC-C010','EP Third Moment Master Fund reported current gross asset valueUSD799157153; this is separate from firm RAUM.',adv,'physical PDF p17; ScheduleD7B1A11',currency='USD',value=799157153,metric='private_fund_gross_asset_value',measurement_date=None,measurement_date_note='Field says current gross asset value; p27 specifies Sept30 for RAUM only. Do not silently assign the same date to this metric.')
claim('SEC-C011','Walleye Opportunities Master Fund Ltd805-3011135543 is disclosed under ScheduleD7B2; Walleye Capital LLC SEC801-113731 provides the full private-fund information.',adv,'physical PDF p21; ScheduleD7B2',relationship_limit='7B2 reporting relationship; no ownership or employment conclusion')
claim('SEC-C012','EP Fund GP LLC is a financial-industry related person disclosed by EntryPoint.',adv,'physical PDF p14; ScheduleD7A')
claim('SEC-C013','EntryPoint FormADV identifies Lawrence Edward Leibowitz CRD2024745 as CEO from10/2020 and Andrew Louis Alkon CRD5079758 as CCO/COO/CFO from05/2023.',adv,'physical PDF p26; ScheduleA')
claim('SEC-C014','The filing reports no information filed in its criminal, regulatory-action and civil-judicial-action DRP pages; this is not a universal no-event finding.',adv,'physical PDF p27; DRP Pages')
claim('SEC-C015','ScheduleB discloses Lawrence Edward Leibowitz as member of EntryPoint GP LLC from10/2020 codeC; Richard A.Desich Irrevocable2005 SD Trust as member from11/2024 codeC; South Dakota Trust Company as trustee of that trust from12/2020 codeF.',adv,'physical PDF p27; ScheduleB',privacy_limit='Professional ownership chain only; no familial inference')

for cik in [2016250,2016251,1555295]:
 hist=json.loads(pathlib.Path(f'outputs/evidence/sec-submissions-{cik}.json').read_text()); rec=hist['filings']['recent'];
 claim('SEC-H'+str(cik),f"SEC submission history identifies CIK{cik} as {hist['name']}, with filings "+', '.join(rec['accessionNumber'])+'.','SEC-HISTORY-'+str(cik),'JSON $.name, $.cik, $.filings.recent')
for d in docs:
 if d.get('status_code')!=200 or not d.get('file','').endswith('.txt'):continue
 text=pathlib.Path(d['file']).read_text();m=re.search(r'<XML>\s*(.*?)\s*</XML>',text,re.S)
 if not m:continue
 x=E.fromstring(m[1]);pi=x.find('primaryIssuer')
 if pi is None:continue
 cik=int(pi.findtext('cik'));acc=d['accession_id'];cid='SEC-D-'+acc;issuer=pi.findtext('entityName');prev=pi.findtext('issuerPreviousNameList/previousName')
 claim(cid, f"{issuer}: issuer CIK{cik}, jurisdiction{pi.findtext('jurisdictionOfInc')}, entityType{pi.findtext('entityType')}, incorporation year{pi.findtext('yearOfInc/value')}, prior name{prev}.",d['document_id'],'XML /edgarSubmission/primaryIssuer',entity_type_conflict=('name ends LP but entityType=Corporation; registry verification pending' if cik==2016251 else None))
 rp=[]
 for r in x.findall('relatedPersonsList/relatedPersonInfo'):
  n=r.find('relatedPersonName');name=' '.join(v for v in [n.findtext('firstName'),n.findtext('middleName'),n.findtext('lastName')] if v and v!='--');roles=[i.text for i in r.findall('relatedPersonRelationshipList/relationship')];rp.append(dict(name=name,roles=roles,clarification=r.findtext('relationshipClarification')))
 claim(cid+'-ROLES',f'FormD related persons for {issuer}: '+json.dumps(rp)+'.',d['document_id'],'XML /edgarSubmission/relatedPersonsList',related_persons=rp)
 od=x.find('offeringData');val=int(od.findtext('offeringSalesAmounts/totalAmountSold'));cnt=int(od.findtext('investors/totalNumberAlreadyInvested'));fs=od.findtext('typeOfFiling/dateOfFirstSale/value');claim(cid+'-FIN',f'{issuer} reports total amount soldUSD{val} and investor count{cnt}; offering sizeindefinite; this is offering activity, notNAV orRAUM.',d['document_id'],'XML /edgarSubmission/offeringData/offeringSalesAmounts, investors, typeOfFiling/dateOfFirstSale',currency='USD',metric='FormD_cumulative_amount_sold',value=val,investor_count=cnt,first_sale_date=fs,filing_date=d['filing_date'],measurement_date=None)
 if cik==1555295:claim(cid+'-SIG','Michael Bleich signed as Director on2012-07-31; SEC filing date2012-08-01. Related-person full nameMichael Edward Bleich supports identity linkage, supplemented by Ophir firm records.',d['document_id'],'XML /edgarSubmission/offeringData/signatureBlock; relatedPersonsList',signature_date='2012-07-31',filing_date='2012-08-01')
p.write_text(json.dumps(docs,indent=2),encoding='utf8');pathlib.Path('outputs/sec-claims.json').write_text(json.dumps(claims,indent=2),encoding='utf8')
print('Preserved official documents',sum(d.get('status_code')==200 for d in docs),'attempts',sum(d.get('status_code')!=200 for d in docs),'claims',len(claims))
