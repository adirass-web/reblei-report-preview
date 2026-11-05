import pathlib,json,csv,hashlib,datetime,re,collections
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');out=root/'continuation-4/employment-inferent';raw=out/'raw';shared=root/'continuation-4/entrypoint-history/raw';schedule=pathlib.Path('work/round4-era-cache/ERA_Schedule_A_B_20111105_20241231.csv');base=pathlib.Path('work/round4-era-cache/ERA_ADV_Base_20111105_20241231.csv');verify={}
for p,mfile in [(schedule,'era-schedule-ab-verification.json'),(base,'era-base-verification.json')]:
 m=json.loads((shared/mfile).read_text());h=hashlib.sha256(p.read_bytes()).hexdigest();assert h==m['uncompressed_sha256'];verify[p.name]=dict(cache_path=str(p),sha256=h,bytes=p.stat().st_size,verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
matches=[];records=0
with schedule.open(encoding='latin-1',newline='') as f:
 for n,r in enumerate(csv.DictReader(f),1):
  records=n
  if r['OwnerID'].strip()=='4262671':matches.append(dict(csv_record_ordinal=n,**r))
ids={r['FilingID'] for r in matches};joined=[];inferentbase=[];basecount=0
with base.open(encoding='latin-1',newline='') as f:
 for n,r in enumerate(csv.DictReader(f),1):
  basecount=n
  if r['FilingID'] in ids or r['1E1'].strip()=='292027':
   keys=['FilingID','DateSubmitted','1A','1B1','1D','1E1','Signatory','Execution Date','Title'];selected=dict(csv_record_ordinal=n,**{k:r[k] for k in keys});joined.append(selected)
   if r['1E1'].strip()=='292027':inferentbase.append(selected)
inferentids={r['FilingID'] for r in inferentbase};inferent=[]
if inferentids:
 with schedule.open(encoding='latin-1',newline='') as f:
  for n,r in enumerate(csv.DictReader(f),1):
   if r['FilingID'] in inferentids:inferent.append(dict(csv_record_ordinal=n,**r))
for name,data in [('exact-ownerid-4262671-all-era-schedule-ab.json',matches),('matched-era-base-filing-joins.json',joined),('inferent-all-era-base-rows.json',inferentbase),('inferent-all-era-schedule-ab-rows.json',inferent)]: (raw/name).write_text(json.dumps(data,indent=2),encoding='utf-8')
summary=dict(logged_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scope='Complete recovered ERA Schedule A/B and ERA Base members',schedule_records_scanned=records,base_records_scanned=basecount,exact_ownerid_matches=len(matches),matched_filingids=sorted(ids),inferent_base_matches=len(inferentbase),inferent_filingids=sorted(inferentids),inferent_schedule_records=len(inferent),inferent_exact_id_matches=sum(r['OwnerID'].strip()=='4262671' for r in inferent),inferent_fullname_matches=sum(re.sub('[^A-Z0-9]','',r['Full Legal Name'].upper()) in {'BLEICHMICHAELEDWARD','MICHAELEDWARDBLEICH'} for r in inferent),matched_firms=sorted({(r['1E1'],r['1A']) for r in joined if r['FilingID'] in ids}),cache_verification=verify)
(out/'era-scan-verification.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary,indent=2));print('MATCHED_ROLE_ROWS')
for r in matches:print(json.dumps(r))
print('MATCHED_BASE_ROWS')
for r in joined:print(json.dumps(r))
