from pathlib import Path
import re,xml.etree.ElementTree as E,json,hashlib,datetime
sources=json.loads(Path('outputs/sec-sources.json').read_text())+json.loads(Path('outputs/financial-sources.json').read_text());obs=[]
for s in sources:
 if s.get('status_code')!=200 or not s.get('file','').endswith('.txt'):continue
 t=Path(s['file']).read_text();m=re.search(r'<XML>\s*(.*?)\s*</XML>',t,re.S)
 if not m:continue
 x=E.fromstring(m[1]);[setattr(e,'tag',e.tag.split('}')[-1]) for e in x.iter()];acc=s.get('accession_id');fd=s.get('filing_date');did=s['document_id']
 if x.find('formData/summaryPage/tableValueTotal') is not None:
  period=x.findtext('formData/coverPage/reportCalendarOrQuarter');date=datetime.datetime.strptime(period,'%m-%d-%Y').date().isoformat();am=x.findtext('formData/coverPage/isAmendment');num=x.findtext('formData/coverPage/amendmentNo');typ=x.findtext('formData/coverPage/amendmentInfo/amendmentType') or x.findtext('formData/coverPage/amendmentType')
  o=dict(observation_id='FIN-13F-'+acc,observation_type='13F_cover_summary',entity_name=x.findtext('formData/coverPage/filingManager/name'),entity_cik='1992519',document_id=did,file=s['file'],url=s['url'],accession_id=acc,filing_date=fd,measurement_date=date,report_period_raw=period,form=x.findtext('headerData/submissionType'),is_amendment=(am=='true'),amendment_flag_raw=am,amendment_number_raw=num,amendment_type=typ,table_entry_total=int(x.findtext('formData/summaryPage/tableEntryTotal')),table_value_total_raw=x.findtext('formData/summaryPage/tableValueTotal'),value=int(x.findtext('formData/summaryPage/tableValueTotal')),currency='USD',unit='US dollars rounded to nearest dollar',scale_multiplier=1,unit_basis_document_id='FIN-13F-INSTRUCTIONS',unit_basis_locator='physical PDF p6 SpecialInstructions6c,8; p13 SummaryPage',metric='13F_information_table_value_total',locator='embedded firstXML /edgarSubmission/formData/coverPage and summaryPage',status='verified_as_filed',other_included_managers_count=x.findtext('formData/summaryPage/otherIncludedManagersCount'),confidential_omitted_raw=x.findtext('formData/summaryPage/isConfidentialOmitted'),signer_name=x.findtext('formData/signatureBlock/name'),signer_title=x.findtext('formData/signatureBlock/title'),limitations='As-filed report total, not net or gross portfolio NAV, firm RAUM, personal assets or performance. Amendment not automatically a replacement or standalone full-period total.')
  # namespace-stripped descendants reveal amendment fields if nested differently
  for e in x.find('formData/coverPage').iter():
   if e.tag=='amendmentType':o['amendment_type']=e.text
   if e.tag=='amendmentNo':o['amendment_number_raw']=e.text
  obs.append(o)
 elif x.find('primaryIssuer') is not None:
  od=x.find('offeringData');obs.append(dict(observation_id='FIN-FORMD-'+acc,observation_type='FormD_cumulative_offering',entity_name=x.findtext('primaryIssuer/entityName'),entity_cik=str(int(x.findtext('primaryIssuer/cik'))),document_id=did,file=s['file'],url=s['url'],accession_id=acc,filing_date=fd,measurement_date=None,form=x.findtext('submissionType'),metric='FormD_cumulative_amount_sold',value=int(od.findtext('offeringSalesAmounts/totalAmountSold')),currency='USD',unit='US dollars',scale_multiplier=1,investor_count=int(od.findtext('investors/totalNumberAlreadyInvested')),offering_amount_raw=od.findtext('offeringSalesAmounts/totalOfferingAmount'),first_sale_date=od.findtext('typeOfFiling/dateOfFirstSale/value'),first_sale_yet_to_occur_raw=od.findtext('typeOfFiling/dateOfFirstSale/yetToOccur'),previous_accession_number=od.findtext('typeOfFiling/newOrAmendment/previousAccessionNumber'),locator='embedded XML /edgarSubmission/offeringData/offeringSalesAmounts,totalNumberAlreadyInvested,typeOfFiling',status='verified_as_filed',limitations='Cumulative amount sold as reported in this notice; not NAV, RAUM, net current capital or period flows. Do not sum amendments. Investor count is issuer count, not verified unique natural persons.'))
obs.sort(key=lambda o:(o['observation_type'],o['entity_cik'],o.get('measurement_date') or o['filing_date'],o['filing_date']))
assert len([o for o in obs if o['observation_type']=='13F_cover_summary'])==12
assert len([o for o in obs if o['observation_type']=='FormD_cumulative_offering'])==9
Path('outputs/financial-observations.json').write_text(json.dumps(obs,indent=2),encoding='utf8')
for o in obs:
 print(o['observation_id'],o['filing_date'],o['measurement_date'],o['value'],o.get('table_entry_total'),o.get('amendment_type'))
fin=json.loads(Path('outputs/financial-sources.json').read_text())
for d in fin:
 if d.get('status_code')==200:
  assert hashlib.sha256(Path(d['file']).read_bytes()).hexdigest()==d['sha256'];d['observation_links']=[o['observation_id'] for o in obs if o['document_id']==d['document_id']]
Path('outputs/financial-sources.json').write_text(json.dumps(fin,indent=2),encoding='utf8')
