from pathlib import Path
import json
root=Path('.')
files=[p for p in root.rglob('*') if p.is_file()]
print('files',len(files),'totalMiB',round(sum(p.stat().st_size for p in files)/1048576,2))
print('largest',[(str(p),round(p.stat().st_size/1048576,2)) for p in sorted(files,key=lambda x:x.stat().st_size,reverse=True)[:6]])
for p in root.glob('continuation/**/*.md'):
 s=p.read_text(encoding='utf-8-sig'); assert '\ufffd' not in s,('replacement character in report',str(p))
print('All continuation Markdown UTF8 checked')
