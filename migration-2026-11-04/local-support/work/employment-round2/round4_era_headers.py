import pathlib,json,csv
r=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-4/entrypoint-history/raw')
for f in ['era-base-verification.json','era-schedule-ab-verification.json']:
 d=json.loads((r/f).read_text());print(f,{k:v for k,v in d.items() if k!='requests'})
for f in ['ERA_ADV_Base_20111105_20241231.csv','ERA_Schedule_A_B_20111105_20241231.csv']:
 with pathlib.Path('work/round4-era-cache',f).open(encoding='latin-1',newline='') as h:print(f,next(csv.reader(h)))
