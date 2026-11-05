import json,pathlib,hashlib,datetime
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-3/employment';p=base/'claims.json';a=json.loads(p.read_text(encoding='utf-8-sig'));c=next(x for x in a if x['claim_id']=='EMP4-C08')
locs={
'EMP4-BASE-A-ORIGINAL':'IA_ADV_Base_A_20111105_20241231.csv; exact firm field1E1=164729; FilingIDs993846,1019291,1070803 and their DateSubmitted fields (2016-03-18,2016-06-17,2017-03-30). This table supplies filing/firm/date joins, not Schedule B ownership rows.',
'EMP4-SCHEDULE-AB-ORIGINAL':'IA_Schedule_A_B_20111105_20241231.csv; Schedule B rows for FilingIDs993846,1019291,1070803; Full Legal Name, Entity in Which, Ownership Code, Status Acquired. Omission is bounded to every Schedule A/B row matching each FilingID.',
'EMP4-OPHIR-FILING-HISTORY':'Selected Base A derivative: FilingIDs993846,1019291,1070803, exactCRD164729 and DateSubmitted. Filing/date correlation only.',
'EMP4-OPHIR-SCHEDULE-ROWS':'Selected Schedule A/B derivative: all rows for FilingIDs993846,1019291,1070803; Schedule B MEB NY INC/FINCH LLC and NAYS LLC/FINCH LLC rows, Ownership Code, and the bounded absence of NAYS LLC or Dror Niv rows in1019291 and1070803.',
'EMP4-OPHIR-2017-ADV':'Physical PDF page20, Schedule B, MEB NY INC in FINCH LLC CodeE and Bleich Owner/MEB NY INC CodeE. This PDF corroborates the March2017 snapshot only, not the March/June2016 historical rows.'}
c['evidence']=[dict(document_id=s,locator=locs[s],**({'physical_pages':[20]} if s=='EMP4-OPHIR-2017-ADV' else {})) for s in c['source_ids']]
c['locators']=[locs[s] for s in c['source_ids']]
p.write_text(json.dumps(a,indent=2),encoding='utf-8')
# Claims are not included as an original source and have no preexisting checksum manifest.
ids={x['document_id'] for x in json.loads((base/'sources.json').read_text(encoding='utf-8-sig'))}
assert len(a)==9 and all(e['document_id'] in ids for e in c['evidence']);assert len(c['evidence'])==len(c['source_ids'])==5
print('EMP4-C08 per-source evidence entries updated; nine claims retained. claims SHA256',hashlib.sha256(p.read_bytes()).hexdigest())
