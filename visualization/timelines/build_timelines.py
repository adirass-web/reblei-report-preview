from pathlib import Path
import os,sys,json,re,textwrap,datetime
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT.parent/'.runtime/python'))
os.environ['MPLCONFIGDIR']=str(ROOT/'.cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','pdf.fonttype':42,'axes.unicode_minus':False,'text.parse_math':False})
BG='#F6F4EF'; INK='#162C38'; MUTED='#52636C'; LINE='#CFD7D7'
COL={'Role disclosure':'#007C83','Regulatory / award':'#B05B3C','Firm / administration':'#5263A0'}
E=[]
def add(id,date,precision,firm,kind,title,detail,claims,basis):
 E.append(dict(id=id,date=date,precision=precision,firm=firm,category=kind,title=title,detail=detail,claim_ids=claims.split(),date_basis=basis))
add('T01','2009-05','month','Scout','Role disclosure','Scout: CEO / managing member','Acquired-status May 2009; less than 5% direct ownership; control reported.','ID-C003','Month in FINRA firm ownership/executive row; axis placement uses month midpoint only, not a known day or hiring date.')
add('T02','2009-05-20','day','Scout','Firm / administration','Scout: formation reported','Delaware formation date reported in FINRA firm record.','ID-C002','Firm-reported formation date; not Bleich employment date.')
add('T03','2012-08-01','day','Ophir','Role disclosure','Ophir: CEO disclosed','ERA filing; acquired-status April 2012. Execution date was July 31.','EMP5-C03','DateSubmitted for ERA FilingID656739; acquired-status month remains separate.')
add('T04','2013-01-28','day','Scout','Regulatory / award','Scout: Cboe settlement order','Censure and $10,000 firm fine; matter 12-0059.','LIT-C004','Original Cboe order date.')
add('T05','2014-05-23','day','Scout','Regulatory / award','Scout: Cboe settlement order','Censure and $5,000 firm fine; matter 14-0018.','LIT-C006','Original Decision Accepting Offer of Settlement date.')
add('T06','2014-07-17','day','Scout','Firm / administration','Scout: business ceased','Firm-reported cessation; registration ended separately on September 19.','ID-C010','Firm business-cessation date, distinct from registration termination and personal departure.')
add('T07','2015-03-25','day','Ophir','Role disclosure','Ophir: CEO + CCO disclosed','First retrieved combined-title snapshot; April 2012 field does not date CCO start.','EMP4-C05','FilingID884710 submission date; first retrieved combined title, not a proved appointment date.')
add('T08','2015-04-07','day','Scout','Regulatory / award','Scout: Nasdaq AWC accepted','Censure and $3m firm fine; no separate personal sanction on Bleich.','EVT-C001 EVT-C002','Nasdaq AWC acceptance date, case20100243866-01; settlement without admitting or denying, without adjudication.')
add('T09','2016-02-25','day','Scout context','Regulatory / award','Wedbush: separate AWC accepted','Wedbush is respondent; Scout named as clearing client.','LIT3-C11','Acceptance date of Wedbush AWC20100243866-02; a separate respondent and action.')
add('T10','2016-11-18','day','Scout context','Regulatory / award','Scout / Wedbush: award served (signed 16 Nov)','USD237,594 damages + interest; USD1,250 reimbursement. Payment unknown; Scout ID join inferred.','LIT3-C04 LIT3-C05 LIT3-C07 LIT4-C01 LIT3-C10','FINRA Date of Service / index Date of Award November18; signatures November16. Legal interest boundary unresolved. Scout CRD join is official-record inference; award has no CRD or Bleich name.')
add('T11','2017-06-29','day','Ophir','Firm / administration','Ophir: withdrawal filed','Reports advisory cessation June 23; Bleich signed as CCO June 23.','EP5-C005','ADV-W FilingID1123733 filed June29; reported cessation and signature dated June23; not dissolution or personal departure.')
add('T12','2021-12-10','day','EntryPoint','Firm / administration','EntryPoint: withdrawal filed','Business Ceased = N; firm cites continued-registration eligibility.','EP5-C004','ADV-W FilingID1583338 filing date; administrative explanation, not disciplinary finding or closure.')
add('T13','2022-05-12','day','EntryPoint','Firm / administration','EntryPoint: initial ERA report','Exempt-reporting-adviser filing under SEC file 802-125863.','EP5-C001 EP5-C002','FilingID1649417 DateSubmitted; initial ERA filing classification, not a new entity or proved legal rename.')
add('T14','2023-11-22','day','EntryPoint','Role disclosure','EntryPoint: Bleich roles disclosed','CIO acquired May 2023; GP member / LP acquired July 2023.','EMP5-C04','ERA FilingID1782387 submission date; status months in Schedule A/B, not proved hiring dates.')
add('T15','2024-06-27','day','EntryPoint','Firm / administration','EntryPoint: one dual-flag filing','Initial SEC request + final ERA report; approval date not established.','EP5-C003 EP5-C001','FilingID1869875 DateSubmitted; both flags belong to one filing; procedural interpretation is official-record inference.')
add('T16','2026-10-15','day','EntryPoint','Role disclosure','EntryPoint: latest reviewed ADV','CIO and GP / LP roles retained; acquired months remain May / July 2023.','SEC-C001 SEC-C002 SEC-C003 SEC-C004','October15,2026 Form ADV filing snapshot; not a new appointment.')
# Immutable pinned appendix provides complete claim wording and locators.
claims=(ROOT.parent/'inputs/claims.md').read_text(encoding='utf-8-sig')
evidence=json.loads((ROOT.parent/'inputs/evidence-index.json').read_text(encoding='utf-8-sig'))
for e in E:
 e['claim_records']={}
 for c in e['claim_ids']:
  m=re.search(r'^## '+re.escape(c)+r'\s*\n(.*?)(?=^<a id=|\Z)',claims,re.M|re.S)
  assert m,c
  e['claim_records'][c]=m.group(1).strip()
meta={'source_commit':'0d9bdb80d7c4e21a38e798eac58ea71e375ee5fb','research_cutoff':'2026-11-04','observations':E,'selected_count':len(E),'note':'All three drafts use this identical selection; no employment tenure bars. T01 uses approximate month midpoint; all other points use the stated date basis.'}
(ROOT/'data.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def txt(fig,x,y,s,size=11,color=INK,weight='normal',**kw):
 return fig.text(x,y,s,fontsize=size,color=color,fontweight=weight,**kw)
def date(e): return datetime.date.fromisoformat(e['date']+'-15' if e['precision']=='month' else e['date'])
def ds(e): return date(e).strftime('%b %Y' if e['precision']=='month' else '%d %b %Y')
def header(fig,letter,name,subtitle):
 fig.patch.set_facecolor(BG)
 txt(fig,.045,.962,'MICHAEL EDWARD BLEICH  /  CRD 4262671',11,MUTED,'bold')
 txt(fig,.045,.926,f'{letter}  |  {name}',27,INK,'bold')
 txt(fig,.045,.895,subtitle,12,MUTED)
 for j,(k,c) in enumerate(COL.items()):
  txt(fig,.045+j*.29,.865,'●  '+k,10,c,'bold')
def footer(fig,editorial=False):
 txt(fig,.045,.072,'READING LIMITS',10,INK,'bold')
 txt(fig,.045,.052,('Month-precision status is not an exact hiring date. Equal editorial spacing conveys sequence, not elapsed time.' if editorial else '◆ = month-precision status (approximate placement); other points follow displayed dates. No employment tenure bars.'),10,MUTED)
 txt(fig,.045,.035,'Chase / Lehman / Barclays dates and the Inferent role remain unresolved; no inferred tenure or transition is drawn.',10,MUTED)
 txt(fig,.045,.017,'Draft • 16 selected observations • Cut-off 04 Nov 2026 • Source commit 0d9bdb80 • Full claim / source map: evidence-map.md',9,MUTED)
def save(fig,n):
 for ext in ('svg','pdf','png'): fig.savefig(ROOT/f'timeline-{n}.{ext}',dpi=170,facecolor=BG)
 plt.close(fig)
def axisstyle(ax):
 ax.set_xlim(datetime.date(2009,1,1),datetime.date(2027,1,1))
 ax.xaxis.set_major_locator(mdates.YearLocator(2));ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
 ax.tick_params(axis='x',labelsize=10,colors=MUTED,length=0,pad=9)
 ax.grid(axis='x',color=LINE,lw=.7,zorder=0)
 ax.set_yticks([])
 for s in ax.spines.values():s.set_visible(False)
 ax.set_facecolor(BG)
# A: three category lanes, per-observation rows, true calendar x.
fig=plt.figure(figsize=(23,20)); header(fig,'A','Calendar lanes','A common calendar axis separates role disclosures, firm actions and administrative records. Horizontal distance represents elapsed time.')
ax=fig.add_axes([.045,.135,.49,.69]);axisstyle(ax)
ordered=[e for cat in COL for e in E if e['category']==cat];ax.set_ylim(-.8,len(E)+1)
ypos={e['id']:len(E)-1-i for i,e in enumerate(ordered)}
for e in ordered:
 y=ypos[e['id']];col=COL[e['category']]
 ax.hlines(y,datetime.date(2009,1,1),datetime.date(2027,1,1),color=LINE,lw=.5)
 ax.scatter([date(e)],[y],s=85,marker='D' if e['precision']=='month' else 'o',color=col,edgecolor=BG,zorder=4)
 ax.annotate(e['id'],(date(e),y),xytext=(0,11),textcoords='offset points',ha='center',color=col,fontsize=8,fontweight='bold')
 fy=.135+.69*(y+.8)/(len(E)+1.8)
 txt(fig,.56,fy+.008,f"{e['id']}   {ds(e)}  ·  {e['title']}",12,col,'bold')
 txt(fig,.56,fy-.008,e['detail'],9.5)
 txt(fig,.56,fy-.021,' / '.join(e['claim_ids']),8,MUTED)
for cat in COL:
 yy=[ypos[e['id']] for e in ordered if e['category']==cat]
 ax.axhspan(min(yy)-.45,max(yy)+.45,color=COL[cat],alpha=.035)
footer(fig);save(fig,'a')
# B: chronological editorial sequence in two columns, equal row spacing.
fig=plt.figure(figsize=(20,19));header(fig,'B','Chronological reading','Read down the left column, then down the right. Equal spacing is editorial: this timeline is NOT to scale.')
for i,e in enumerate(E):
 col=i//8;row=i%8;x=.052+col*.48;y=.81-row*.086
 color=COL[e['category']]
 fig.add_artist(plt.Line2D([x+.006,x+.006],[y-.059,y+.012],transform=fig.transFigure,color=LINE,lw=2))
 txt(fig,x,y,f'{i+1:02}',13,color,'bold',bbox=dict(facecolor=BG,edgecolor='none',pad=2))
 txt(fig,x+.037,y,ds(e).upper(),10,color,'bold')
 txt(fig,x+.037,y-.022,e['title'],15,INK,'bold')
 txt(fig,x+.037,y-.042,textwrap.fill(e['detail'],66),10.5)
 txt(fig,x+.037,y-.068,e['id']+'  |  '+' / '.join(e['claim_ids']),8.5,MUTED)
footer(fig,editorial=True);save(fig,'b')
# C: firm small multiples on identical full calendar axes, each dot has its own row.
fig=plt.figure(figsize=(24,18));header(fig,'C','Firm record panels','Three firm panels share the same 2009–2027 calendar scale. Sparse years remain visible; rows organize observations within each firm.')
groups=[('Scout / related matters',[e for e in E if e['firm'].startswith('Scout')]),('Ophir Partners',[e for e in E if e['firm']=='Ophir']),('EntryPoint Capital',[e for e in E if e['firm']=='EntryPoint'])]
for k,(name,events) in enumerate(groups):
 bottom=[.54,.335,.12][k];h=[.27,.14,.15][k]
 ax=fig.add_axes([.045,bottom,.45,h]);axisstyle(ax);ax.set_ylim(-.7,len(events)-.4)
 txt(fig,.045,bottom+h+.01,name.upper(),13,INK,'bold')
 for i,e in enumerate(events):
  y=len(events)-1-i;color=COL[e['category']]
  ax.hlines(y,datetime.date(2009,1,1),datetime.date(2027,1,1),color=LINE,lw=.5)
  ax.scatter([date(e)],[y],s=65,color=color,marker='D' if e['precision']=='month' else 'o',zorder=3)
  ax.annotate(e['id'],(date(e),y),xytext=(8,0),textcoords='offset points',va='center',fontsize=8,color=color,fontweight='bold')
  fy=bottom+h*(y+.7)/(len(events)+.3)
  txt(fig,.52,fy+.006,f"{e['id']}  ·  {ds(e)}  ·  {e['title']}",11.5,color,'bold')
  txt(fig,.52,fy-.004,e['detail'],9.5)
  txt(fig,.52,fy-.012,' / '.join(e['claim_ids']),8,MUTED)
footer(fig);save(fig,'c')
# Complete local source map, extracted verbatim from pinned appendix.
maptext=['# Timeline evidence map','',f"Source commit: `{meta['source_commit']}`. Research cut-off: 2026-11-04.",'','All three drafts use the same 16 observations. Claims retain their exact pinned wording and all source locators below. Record-hosting is not independent adjudication. Files are not new research.','', 'T01 is a month-precision status observation plotted at the midpoint of May only for layout. The exact day is unknown. All others use their explicitly described date basis. Scout award identity join is an inference; no Bleich name or Scout CRD appears in the award.','']
for e in E:
 maptext += [f"## {e['id']} — {e['title']}",'',f"Displayed date: **{e['date']}** ({e['precision']} precision).",'',f"Date basis: {e['date_basis']}",'',e['detail'],'']
 for c,v in e['claim_records'].items(): maptext += [f'### {c}','',v,'']
# Retained-file links from claims were relative to inputs' root; preserve actual target by prefix.
mapout='\n'.join(maptext).replace('](../evidence/','](../../evidence/').replace('](../continuation','](../../continuation').replace('](documents.md#','](../../dossier/documents.md#').replace('](conflicts-and-gaps.md#','](../../dossier/conflicts-and-gaps.md#')
(ROOT/'evidence-map.md').write_text(mapout+'\n',encoding='utf-8')
(ROOT/'.gitignore').write_text('.cache/\n__pycache__/\n',encoding='utf-8')
print('Generated',len(E),'observations; 9 figure files; data and source map.')






