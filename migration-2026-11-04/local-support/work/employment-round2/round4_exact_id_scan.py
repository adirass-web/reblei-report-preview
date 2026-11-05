import pathlib,json,csv,hashlib,datetime,re
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');out=root/'continuation-4/employment-inferent';raw=out/'raw';schedule=pathlib.Path('work/employment-round2/schedule-cache/IA_Schedule_A_B_20111105_20241231.csv');base=pathlib.Path('work/inferent-adv-cache/IA_ADV_Base_A_20111105_20241231.csv')
sm=json.loads((root/'continuation-3/employment/raw/EMP4-SCHEDULE-AB-verification.json').read_text());bm=json.loads((root/'continuation-3/inferent/base-a-verification.json').read_text());verify={}
for p,m in [(schedule,sm),(base,bm)]:
 h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==m['uncompressed_sha256'];verify[p.name]=dict(cache_path=str(p),sha256=h,bytes=p.stat().st_size,original_verified_sha256=m['uncompressed_sha256'],verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
inferent_ids={'1166838','1212685','1227321','1231177','1237606','1278683'};matches=[];inferent=[];records=0
with schedule.open(encoding='latin-1',newline='') as f:
 for n,r in enumerate(csv.DictReader(f),1):
  records=n
  if r['OwnerID'].strip()=='4262671':matches.append(dict(csv_record_ordinal=n,**r))
  if r['FilingID'] in inferent_ids:inferent.append(dict(csv_record_ordinal=n,**r))
filingids={r['FilingID'] for r in matches}|inferent_ids;joined=[];basecount=0
with base.open(encoding='latin-1',newline='') as f:
 for n,r in enumerate(csv.DictReader(f),1):
  basecount=n
  if r['FilingID'] in filingids:
   keys=['FilingID','DateSubmitted','1A','1B1','1D','1E1','4A','4B','Signatory','Execution Date','Title'];joined.append(dict(csv_record_ordinal=n,**{k:r.get(k) for k in keys}))
for name,data in [('exact-ownerid-4262671-all-ia-schedule-ab.json',matches),('inferent-six-filings-all-ia-schedule-ab.json',inferent),('matched-base-a-filing-joins.json',joined)]: (raw/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
inferent_exact=[r for r in inferent if r['OwnerID'].strip()=='4262671'];inferent_name=[r for r in inferent if re.sub('[^A-Z0-9]','',r['Full Legal Name'].upper()) in {'BLEICHMICHAELEDWARD','MICHAELEDWARDBLEICH'}]
summary=dict(logged_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Complete recovered IA Schedule A/B and IA Base A members only; ERA tables not scanned',schedule_records_scanned=records,base_records_scanned=basecount,exact_ownerid_matches=len(matches),matched_filingids=sorted({r['FilingID'] for r in matches}),inferent_filingids=sorted(inferent_ids),inferent_records=len(inferent),inferent_exact_id_matches=len(inferent_exact),inferent_fullname_matches=len(inferent_name),matched_firms=sorted({(r['1E1'],r['1A']) for r in joined if r['FilingID'] in {x['FilingID'] for x in matches}}),cache_verification=verify)
(out/'scan-verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2));print('MATCHED_FIRM_ROWS')
for r in joined:
 if r['FilingID'] in {x['FilingID'] for x in matches}:print(json.dumps(r))
print('INFERENT_ALL_ROWS')
for r in inferent:print(json.dumps(r))
