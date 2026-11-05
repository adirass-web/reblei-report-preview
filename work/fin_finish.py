from pathlib import Path
import json,re,xml.etree.ElementTree as E,hashlib,datetime
op=Path('outputs/financial-observations.json');obs=json.loads(op.read_text())
for o in obs:
 if o['observation_type']!='13F_cover_summary':continue
 t=Path(o['file']).read_text();matches=re.findall(r'<XML>\s*(.*?)\s*</XML>',t,re.S);x=E.fromstring(matches[0]);[setattr(e,'tag',e.tag.split('}')[-1]) for e in x.iter()]
 o['sec_file_number_as_filed']=x.findtext('formData/coverPage/secFileNumber');o['form13f_file_number']=x.findtext('formData/coverPage/form13FFileNumber');o['usable_for_comparison']=not o['is_amendment']
 if o['accession_id']=='0001992519-24-000008':
  z=E.fromstring(matches[1]);[setattr(e,'tag',e.tag.split('}')[-1]) for e in z.iter()];rows=z.findall('infoTable');total=sum(int(row.findtext('value')) for row in rows)
  o['status']='quarantined_internal_inconsistency';o['raw_values_verified_as_filed']=True;o['usable_for_comparison']=False;o['conflict_id']='FIN-CONFLICT-2024Q3-COVER';o['reconciliation']=dict(method='Count second embeddedXML /informationTable/infoTable nodes; sum integer value child over same nodes',actual_table_rows=len(rows),information_table_value_sum_raw=total,currency='USD',unit='nearest US dollar',derived_not_cover_value=True,conclusion='Cover count and cover value do not match supplied information table; cause undetermined. No silent correction.',coverage='This anomalous filing only; other information tables not audited in this bounded cover-summary stage')
  o['limitations']+=' Cover summary internally conflicts with information table. Exclude raw cover value from charts/trends or fund-size analysis.'
op.write_text(json.dumps(obs,indent=2),encoding='utf8')
sp=Path('outputs/financial-sources.json');sources=json.loads(sp.read_text())
for d in sources:
 if d.get('file') and d['file'].endswith('.pdf'):
  d['source_class']='official SEC form and instructions';d['preserved_format']='original PDF';d['derived_text_file']=d['file']+'.txt';d['derived_text_sha256']=hashlib.sha256(Path(d['file']+'.txt').read_bytes()).hexdigest();d['pdf_page_numbering']='physical, 1-based'
sp.write_text(json.dumps(sources,indent=2),encoding='utf8')
log=[dict(search_id='search_a1bca9da9d3e6e9d66aa87f787b434e8',service='Parallel Search',session_id='cde307ef-23a4-46ce-96b7-6c8ab8411194',queries=['site:sec.gov Form 13F nearest dollar','site:sec.gov 13F amendment new holdings instructions'],objective='Official SEC13F dollar units and amendment treatment',result_urls_used=['https://www.sec.gov/info/edgar/forms/form13f.pdf','https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f'],discovery_only=True,note='Search excerpts identified official instructions and FAQ. Original SEC instructions downloaded at https://www.sec.gov/files/form13f.pdf. FAQ direct download returned403; use preserved instructions for substantive evidence.',log_written_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())]
Path('outputs/financial-search-log.json').write_text(json.dumps(log,indent=2),encoding='utf8')
rows=[]
for o in obs:
 if o['observation_type']=='13F_cover_summary':rows.append(f"|{o['measurement_date']}|{o['filing_date']}|{o['accession_id']}|{o['form']}|{o['table_entry_total']:,}|{o['value']:,}|{o.get('amendment_type') or ('QUARANTINED: internal mismatch' if o.get('conflict_id') else 'Original report')}|")
report='''# Financial specialist — original SEC collection and observations

Research cut-off: November4,2026. This stage independently retrieved public SEC records; no pre-existing repository material was consulted. All figures below describe what records report, with specified units and limits.

## Collection completed

All **15 filings** in the independently preserved SEC submissions response for EntryPoint Capital, LLC, CIK1992519, are now preserved as original complete-submission text. Four were already acquired during SEC discovery; eleven additional originals were downloaded in this stage. They comprise **12 Form13F submissions** (11 original quarterly reports plus one amendment) and **3 N-PX submissions**. The retrieved response lists no older-history file. This defines the collected history, not a claim that no other records exist.

New acquisition metadata is in `financial-sources.json`; previously preserved originals remain indexed in `sec-sources.json`. This stage does not mutate those earlier files. Hashes for all12 newly preserved successful responses (11filings plus official instructions PDF) were checked. The unsuccessful direct FAQ request is logged separately in the same acquisition array. A Parallel Search discovery log is in `financial-search-log.json`.

## Units and interpretation

Original SEC Form13F instructions, preserved as `evidence/fin-form13f-instructions.pdf` (14physical pages), specify **US dollars rounded to the nearest dollar**, not thousands. See physicalp6, SpecialInstructions6(c) and8; p13 summary-page value total; p14 information-table value column. The retrieved document bears form revision07-23 onp1. Parallel Search also located SEC FAQ36's explanation that the nearest-dollar rule took effectJanuary3,2023; the FAQ's original HTML could not be downloaded, so the preserved form instructions supply the original-source unit proof.

These totals represent the securities reported on each Form13F. They are not firmRAUM, full net/gross portfolio assets, fundNAV, personal wealth, revenues, fees or performance. Changes in reported values do not establish investment returns. Investor and account identities cannot be inferred from these summaries.

Original instructions physicalpp4–5, SpecialInstruction3, distinguish restatements from additions. A NEW HOLDINGS amendment supplements a same-period report; its value is not a replacement full-period total. No amendment totals have been blindly added here, and no reconstructed2024Q2 holdings total is asserted.

## Form13F cover observations

Each row retains raw cover fields with scale multiplier1. Original files, document IDs, exact XML locators and interpretation flags are in `financial-observations.json`.

|Report period|Filed|Accession|Form|Raw cover entries|Raw cover valueUSD|Treatment|
|---|---|---|---|---:|---:|---|
'''+ '\n'.join(rows)+'''

### Material internal inconsistency:2024Q3

Original accession **0001992519-24-000008**, filedNovember13,2024 forSeptember30,2024, reports `tableEntryTotal=175789` and `tableValueTotal=594` in its cover-summary XML. These are confirmed raw fields, not an extraction substitution. The filing's second embeddedXML information table contains **594 entries**; summing its raw integer `value` fields gives **175,789,004USD** under the applicable nearest-dollar instructions.

The cover and table therefore conflict. Cause is undetermined; no automatic correction or wrongdoing inference is made. The raw cover observation remains preserved but is marked **quarantined_internal_inconsistency**, unusable for comparison. The separately labelled count/sum reconciliation is recorded within that observation. This narrow reconciliation was performed because the cover anomaly was detected; other information tables were not position-by-position audited during this bounded cover-summary stage.

The original [complete submission](https://www.sec.gov/Archives/edgar/data/1992519/000199251924000008/0001992519-24-000008.txt) is preserved at `evidence/fin-1992519-0001992519-24-000008.txt`. This discrepancy should remain an explicit conflict in the consolidated register and receive independent QA.

### Period and amendment caveats

The August13,2026 amendment **0001992519-26-000006** concerns **June30,2024**, amendmentNo1, typeNEW HOLDINGS, notJune2026. It reports536 new entries and146,855,443USD on its own summary. Its latest filing date does not make it the latest portfolio period.

The latest original holdings report in the retrieved history is **June30,2026**, accession0001992519-26-000007, filedAugust13,2026, reporting768 entries and412,064,875USD. No September30,2026 Form13F appears in that retrieved response. As ofNovember4,2026, the standard45-day quarter-end filing window has not elapsed; the absence should not be labelled delinquency. GeneralInstructions1 and3, physicalp1, describe that filing window.

Earlier cover pages sometimes retain SEC file number802-125863, while later pages report801-130798. The exact value as filed is retained in each observation. Registration history and any stale-field interpretation require separate evidence; these are not interchangeable identifiers silently rewritten across history.

## FormD observations reused without downloading duplicates

Nine cumulative offering observations from original full submissions are included in the same observations JSON: four for each EP Third Moment feeder and one initial Ophir master notice. Their source documents/hashes remain in `sec-sources.json`.

|Issuer|Filed|Accession|Cumulative soldUSD|Reported investors|
|---|---|---|---:|---:|
'''
for o in obs:
 if o['observation_type']=='FormD_cumulative_offering':report+=f"|{o['entity_name']}|{o['filing_date']}|{o['accession_id']}|{o['value']:,}|{o['investor_count']}|\n"
report+='''
Each amount is the issuer's cumulative amount sold in that notice. Do not sum amendments, treat cumulative proceeds as currentNAV, or infer unique natural-person investors. No separate measurement date is stated; filing date is preserved independently rather than silently converted to a measurement date. Ophir's2012 notice reports first sale yet to occur; zero at that time does not show permanent failure to raise funds.

## Limits and next work

The observations JSON contains **21 observations**:12 cover summaries (one quarantined) and9FormD notices. This stage does not estimate fees, carried interests, ownership income, flows or performance, reconstruct amended holdings, or audit the remaining information tables. The original complete submissions retain those tables for subsequent work. This bounded collection is complete against the retrieved15-filing EntryPoint submissions list; broader full-career financial coverage remains dependent on additional entities and historical records.
'''
Path('outputs/specialist-financial.md').write_text(report,encoding='utf8')
print('Financial report saved;21observations;15EntryPoint originals preserved;one cover-summary conflict quarantined.')
