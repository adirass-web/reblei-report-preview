import requests,pathlib,datetime,json,hashlib
root=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records');base=root/'continuation-2/employment';ss=json.loads((base/'sources.json').read_text())
u='https://web.archive.org/cdx/search/cdx?url=files.brokercheck.finra.org/individual/individual_4262671.pdf&output=json&filter=statuscode:200&filter=mimetype:application/pdf&collapse=digest'
i='EMP3-WAYBACK-INDEX';t=datetime.datetime.now(datetime.timezone.utc).isoformat();p=base/'raw'/f'{i}.json'
try:
 r=requests.get(u,timeout=35);p.write_bytes(r.content);ss.append(dict(document_id=i,url=u,file=p.relative_to(root).as_posix(),sha256=hashlib.sha256(r.content).hexdigest(),retrieved_at_utc=t,source_class='third_party_archive_index',status='retrieved' if r.status_code==200 else 'access_failure',http_status=r.status_code,size_bytes=len(r.content)));print(r.status_code,r.text[:1000])
except Exception as e:ss.append(dict(document_id=i,url=u,retrieved_at_utc=t,source_class='third_party_archive_index',status='request_failure',error=str(e)));print(str(e))
(base/'sources.json').write_text(json.dumps(ss,indent=2),encoding='utf-8')
