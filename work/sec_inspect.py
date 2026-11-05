from pathlib import Path
import re,xml.etree.ElementTree as E,json
for p in Path('outputs/evidence').glob('sec-*.txt'):
 if '.pdf.' in p.name:continue
 t=p.read_text(); m=re.search(r'<XML>\s*(.*?)\s*</XML>',t,re.S)
 if not m:continue
 x=E.fromstring(m.group(1));print('\nFILE',p.name)
 if x.find('primaryIssuer') is not None:
  for k in ['primaryIssuer/entityName','primaryIssuer/entityType','primaryIssuer/yearOfInc/value','primaryIssuer/issuerPreviousNameList/previousName','offeringData/typeOfFiling/dateOfFirstSale/value','offeringData/offeringSalesAmounts/totalAmountSold','offeringData/investors/totalNumberAlreadyInvested']:
   print(k,x.findtext(k))
  print('Related',[(E.tostring(n,encoding='unicode')) for n in x.findall('relatedPersonsList/relatedPersonInfo/relatedPersonName')])
 else:
  for n in x.iter():
   tag=n.tag.split('}')[-1]
   if tag in ['periodOfReport','reportCalendarOrQuarter','name','title','signatureDate','signature','isAmendment','amendmentType','tableValueTotal','tableEntryTotal','txTitle','txPrintedSignature','txAsOfDate']:
    print(tag,n.text)
