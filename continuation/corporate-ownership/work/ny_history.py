import requests,pathlib,hashlib,json,datetime,time
root=pathlib.Path('continuation/corporate-ownership');p=root/'sources.json';sources=json.loads(p.read_text());s=requests.Session();s.headers['User-Agent']='Mozilla/5.0 (compatible; PublicRecordsResearch/1.0)'
def get(id,dataset,params):
 url='https://data.ny.gov/resource/'+dataset+'.json';r=s.get(url,params=params,timeout=40);rec=dict(document_id=id,url=r.url,http_status=r.status_code,retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),bytes=len(r.content),file=None,sha256=None,dataset=dataset,query=params,source_class='NY government open-data response; not official Department record or certified status proof')
 if r.status_code==200:
  f=root/'evidence'/f'{id}.json';f.write_bytes(r.content);rec.update(file=str(f).replace('\\','/'),sha256=hashlib.sha256(r.content).hexdigest());j=r.json();rec['response_rows']=len(j);print(id,json.dumps(j,indent=2));sources.append(rec);return j
 sources.append(rec);print(id,r.status_code);return []
a=get('CORP2-NY-TARGET-FILINGS','63wc-4exh',{'$select':'corpid_num,film_num,date_filed,approved_date,eff_date,for_inc_date,entitytype,documenttype,corp_name,juris','$where':"corpid_num in ('3772241','6795220','4790401','4790408') OR upper(corp_name) like '%OPEH%' OR upper(corp_name) like '%EP FUND GP%'",'$limit':'1000','$order':'corpid_num,date_filed'})
ids=sorted(set(str(x['corpid_num']) for x in a)|{'3772241','6795220','4790401','4790408'});where='corpid_num in ('+','.join("'"+i+"'" for i in ids)+')'
for ds,id,select in [('3gg2-jgnp','CORP2-NY-TARGET-STATUS','corpid_num,film_num,date_filed,mod_cert_code,status'),('ekwr-p59j','CORP2-NY-TARGET-NAMES','corpid_num,film_num,date_filed,name_type,name_status,corp_name')]:
 get(id,ds,{'$select':select,'$where':where,'$limit':'1000','$order':'corpid_num,date_filed'});time.sleep(.3)
p.write_text(json.dumps(sources,indent=2),encoding='utf8')
