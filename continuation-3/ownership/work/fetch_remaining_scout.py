import pathlib,requests,json,hashlib,datetime,fitz
root=pathlib.Path(r'V:\Codex\2026-11-04\referenced-chatgpt-conversation-this-is-an-3\outputs\ReBlei\investigations\2026-11-04-official-records\continuation-3\ownership')
meta=json.loads((root/'raw/scout-submissions.json').read_text())['filings']['recent']; logs=json.loads((root/'request-log.json').read_text())
for i,form in enumerate(meta['form']):
 if meta['filmNumber'][i] in ['14048639','10027661'] or form not in ['X-17A-5','X-17A-5/A','13F-HR']: continue
 film=meta['filmNumber'][i]; acc=meta['accessionNumber'][i]
 url='https://www.sec.gov/Archives/edgar/vprr/'+film[:4]+'/'+film+'.pdf' if form!='13F-HR' else 'https://www.sec.gov/Archives/edgar/data/1474522/'+acc.replace('-','')+'/primary_doc.xml'
 at=datetime.datetime.now(datetime.timezone.utc).isoformat(); ident='scout-'+meta['reportDate'][i][:4]+'-'+form.replace('/','-')
 try:
  r=requests.get(url,headers={'User-Agent':'Financial public record research/1.0'},timeout=30); pdf=r.content.startswith(b'%PDF');p=root/'raw'/(ident+('.pdf' if pdf else '.xml' if form=='13F-HR' and r.status_code==200 else '.response.txt'));p.write_bytes(r.content)
  row={'source_id':'CORP4-'+ident.upper(),'url':url,'file':'continuation-3/ownership/raw/'+p.name,'sha256':hashlib.sha256(r.content).hexdigest(),'retrieved_at_utc':at,'http_status':r.status_code,'content_type':r.headers.get('content-type'),'bytes':len(r.content),'accession_id':acc,'filing_date':meta['filingDate'][i],'period_end':meta['reportDate'][i],'film_number':film,'form':form,'source_class':'official_original' if r.status_code==200 else 'official_access_error_not_substantive_evidence','response_headers':dict(r.headers)}
  if pdf:
   doc=fitz.open(p);row['pdf_pages']=len(doc);(root/'raw'/(ident+'-text.txt')).write_text('\n'.join('PHYSICAL PAGE '+str(j+1)+'\n'+' '.join(pg.get_text().split()) for j,pg in enumerate(doc)),encoding='utf-8')
  logs.append(row);print(ident,r.status_code,len(r.content),flush=True)
 except Exception as e: logs.append({'source_id':'CORP4-'+ident.upper(),'url':url,'retrieved_at_utc':at,'error':str(e)});print(ident,type(e).__name__,flush=True)
(root/'request-log.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
for name in ['scout2009-annual','scout2013-annual']:
 doc=fitz.open(root/'raw'/(name+'.pdf'));(root/'raw'/(name+'-text.txt')).write_text('\n'.join('PHYSICAL PAGE '+str(j+1)+'\n'+' '.join(pg.get_text().split()) for j,pg in enumerate(doc)),encoding='utf-8')
