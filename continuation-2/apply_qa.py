import pathlib,json,fitz
root=pathlib.Path('.')
p=root/'continuation-2/litigation/claims.json';d=json.loads(p.read_text(encoding='utf-8'));x=next(x for x in d if x['claim_id']=='LIT3-C12');x['statement']=x['statement'].replace('USD675000 paid jointly','USD675000 payable jointly').replace('a supervisory-procedure revision undertaking.','a supervisory-procedure revision undertaking with registered-principal attestation within60businessdays of acceptance.');p.write_text(json.dumps(d,indent=2),encoding='utf-8')
p=root/'continuation-2/litigation/report.md';s=p.read_text(encoding='utf-8-sig');s=s.replace('and a supervisory-procedure revision undertaking (p8).','and a supervisory-procedure revision undertaking requiring registered-principal attestation within 60 business days of acceptance (p8). Wedbush consented without admitting or denying the findings, before a hearing and without adjudication. The sanctions-effective date was to be set separately by FINRA staff (p9).');p.write_text(s,encoding='utf-8')
src=json.loads((root/'continuation-2/inferent/sources.json').read_text(encoding='utf-8-sig'))
for x in src:
 if x['document_id'] in ['INF3-BRO-20180705','INF3-BRO-20180831']:
  print(x['document_id'],x['file']);d=fitz.open(root/x['file']);print(d[3].get_text()[-2600:])
