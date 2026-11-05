from pathlib import Path
import shutil,json,hashlib,datetime,subprocess,sqlite3
src=Path('outputs').resolve();repo=(src/'ReBlei').resolve();dst=(repo/'investigations'/'2026-11-04-official-records').resolve()
assert dst.is_relative_to(repo) and repo.name=='ReBlei'
dst.mkdir(parents=True,exist_ok=True)
# Only independently generated paths are copied. Existing repository root research is neither read nor indexed.
for item in src.iterdir():
 if item.name=='ReBlei' or item.suffix=='.zip':continue
 if item.is_file():shutil.copy2(item,dst/item.name)
 elif item.name in ('evidence','tables'):shutil.copytree(item,dst/item.name,dirs_exist_ok=True)
shutil.copytree(Path('work'),dst/'work',dirs_exist_ok=True)
base=subprocess.check_output(['git','-C',str(repo),'rev-parse','origin/main'],text=True).strip()
meta={'research_cutoff':'2026-11-04','prepared_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repository':'adirass-web/ReBlei','branch':'research/bleich-official-records-2026-11-04','folder':'investigations/2026-11-04-official-records','base_commit':base,'existing_repository_research_used':False,'personal_civil_proceedings_included':False,'full_career_investigation_complete':False,'validation':json.loads((dst/'validation.json').read_text(encoding='utf8')),'preservation_note':'Original response bytes and rendered captures are distinguished in index. Derived text is separate. SHA256SUMS covers package files except itself.'}
(dst/'archive-manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf8')
files=sorted(x for x in dst.rglob('*') if x.is_file() and x.name!='SHA256SUMS.txt')
manifest=[hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.relative_to(dst).as_posix() for f in files]
(dst/'SHA256SUMS.txt').write_text('\n'.join(manifest)+'\n',encoding='utf8')
for line in manifest:
 h,r=line.split('  ',1);assert hashlib.sha256((dst/r).read_bytes()).hexdigest()==h
j=json.loads((dst/'evidence-index.json').read_text(encoding='utf8'))
for x in j['tables']['documents']:assert hashlib.sha256((dst/x['file_path']).read_bytes()).hexdigest()==x['sha256']
c=sqlite3.connect(dst/'evidence-index.sqlite');assert not c.execute('PRAGMA foreign_key_check').fetchall();assert c.execute('PRAGMA integrity_check').fetchone()[0]=='ok';c.close()
print(json.dumps({'folder':str(dst),'files_verified':len(files),'source_documents_verified':len(j['tables']['documents']),'base_commit':base,'existing_root_material_used':False},indent=2))
