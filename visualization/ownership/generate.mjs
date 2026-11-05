import { instance } from '../.runtime/graphviz/node_modules/@viz-js/viz/dist/viz.js';
import fs from 'node:fs';
import path from 'node:path';
const here=path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Z]:)/,'$1'));
const D=JSON.parse(fs.readFileSync(path.join(here,'data.json'),'utf8'));
const viz=await instance();
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const q=s=>JSON.stringify(s);
const palette=['#175d69','#425b9c','#8a5b24'];
const font='Arial';
const W=2250;
const txt=(x,y,s,size=23,fill='#25374a',weight='normal')=>`<text x="${x}" y="${y}" fill="${fill}" font-family="Arial, sans-serif" font-size="${size}" font-weight="${weight}">${esc(s)}</text>`;
const lines=(x,y,arr,size=23,gap=32,fill='#25374a')=>arr.map((s,i)=>txt(x,y+i*gap,s,size,fill)).join('');
let metrics=[];
function graph(s,version,i){
 const c=palette[i];let out=`digraph "${s.id}_${version}" { graph [rankdir=${version==='b'?'LR':'TB'}, bgcolor="transparent", pad="0.18", nodesep="0.45", ranksep="0.68", mindist="1.0", overlap=false, sep="+25", splines=polyline, fontname="Arial"]; node [shape=box, style="rounded,filled", fillcolor="#f4f7fa", color="#c5d1db", fontname="Arial", fontsize=21, margin="0.20,0.13", penwidth=1.3]; edge [fontname="Arial", fontsize=18, color="${c}", fontcolor="#25374a", penwidth=1.8, arrowsize=0.8];\n`;
 {
 const positions={scout:{b:'-3.5,0!',meb:'0,2!',finch:'3.5,0!',firm:'0,-2!',nays:'7.5,0!',niv:'11.5,0!'},ophir:{b:'0,-2!',meb:'-3.5,0!',finch:'0,2!',firm:'3.5,0!'},entrypoint:{b:'0,0!',gp:'5,0!',partners:'0,-4!',firm:'-5,0!'}};
 for(const [id,name] of Object.entries(s.nodes))out+=`${id} [label=${q(name)}, ${version==='c'?`pos="${positions[s.id][id]}", pin=true,`:""} ${id==='b'?`fillcolor="${c}", color="${c}", fontcolor="white"`:id==='firm'?`fillcolor="#e6edf3", penwidth=2.2`:''}];\n`;
 for(const e of s.edges){let label=`${e.ownership_band}\n${e.acquired_status} · ${e.claim_id}`;out+=`${e.from} -> ${e.to} [label=${q(label)}${(e.from==='b'&&e.to==='firm')?', constraint=false':''}];\n`;}
 }
 return out+'}\n';
}
for(const version of ['a','b','c']){
 const H={a:1580,b:2040,c:2380}[version];
 const title={a:'Three dated ownership hierarchies',b:'Ownership flows across dated lanes',c:'Radial maps of disclosed ownership'}[version];
 let svg=`<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}"><title>DRAFT ${version.toUpperCase()} — ${title}; research cut-off 2026-11-04; historical Scout, Ophir 2017-03-30, EntryPoint 2026-10-15</title><desc>Fourteen selected disclosed ownership relationships in three separately dated panels. Ownership bands are ranges. Every selected relationship reports control yes, separately from percentage ownership. Corporate identity joins remain unresolved. See evidence-map.md.</desc><rect width="100%" height="100%" fill="#ffffff"/>`;
 svg+=txt(66,62,`DRAFT ${version.toUpperCase()}   /   OWNERSHIP DISCLOSURES`,23,'#627486','bold');
 svg+=txt(66,112,title,42,'#142b40','bold');
 svg+=txt(66,155,'CRD 4262671 · Source cut-off 04 Nov 2026 · Separate snapshots · Selected relationships',24,'#586b7d');
 svg+=txt(66,201,'Solid arrows: owner → owned entity. Ownership bands appear on the arrows.',23);
 svg+=txt(66,233,'Control: all selected ownership rows report yes / Y. Professional roles are stated separately below.',23);
 const tall=version==='a';
 for(let i=0;i<3;i++){
 const s=D.snapshots[i],x=tall?66+i*711:66,y=tall?271:271+i*(version==='c'?600:490),pw=tall?684:2118,ph=tall?1000:(version==='c'?580:470),c=palette[i];
 svg+=`<rect x="${x}" y="${y}" width="${pw}" height="${ph}" rx="12" fill="#fafcfe" stroke="#d8e1e8" stroke-width="2"/><rect x="${x}" y="${y}" width="${pw}" height="8" rx="4" fill="${c}"/>`;
 svg+=txt(x+22,y+47,s.title,tall?25:26,c,'bold');svg+=txt(x+22,y+80,s.date+' · Firm CRD '+['151990','164729','313946'][i],tall?17:22,'#627486');
 const dot=graph(s,version,i);fs.writeFileSync(path.join(here,`ownership-${version}-${s.id}.dot`),dot);
 const g=viz.renderString(dot,{format:'svg',engine:version==='c'?'neato':'dot'});fs.writeFileSync(path.join(here,`ownership-${version}-${s.id}.graph.svg`),g);
 const vb=g.match(/viewBox="([^"]+)"/)[1].split(/\s+/).map(Number);const inner=g.slice(g.indexOf('> ',g.indexOf('<svg'))+1);let body=g.replace(/^[\s\S]*?<svg[^>]*>/,'').replace(/<\/svg>\s*$/,'');
 body=body.replace(/id="([^"]+)"/g,(_,id)=>`id="${version}-${s.id}-${id}"`);
 const bx=x+16,by=y+(tall?101:88),bw=pw-32,bh=tall?710:(version==='c'?390:285);
 const scale=Math.min(bw/vb[2],bh/vb[3]);const ox=bx+(bw-vb[2]*scale)/2,oy=by+(bh-vb[3]*scale)/2;
 svg+=`<g transform="translate(${ox} ${oy}) scale(${scale})">${body}</g>`;
 metrics.push({version,panel:s.id,graphWidth:vb[2],graphHeight:vb[3],scale,minTextPx:18*scale});
 const ty=tall?y+842:y+(version==='c'?510:405);
 const role=s.roles;svg+=txt(x+22,ty,role,tall?19:21,'#25374a');svg+=txt(x+22,ty+31,s.source,tall?20:21,'#627486');
 if(tall){svg+=txt(x+22,ty+65,'Control yes / Y ≠ percentage ownership',20,'#627486');}
 }
 const footY={a:1320,b:1780,c:2140}[version];
 svg+=`<path d="M66 ${footY-23}H2184" stroke="#d8e1e8" stroke-width="2"/>`;
 svg+=lines(66,footY,['EntryPoint GP LLC: Schedule A says GENERAL PARTNER · code NA · control Y · acquired 10/2020 [SEC-C006].','This is an as-filed role note; no GP-to-partnership target is inferred. EP Fund GP LLC is a separate name.'],22,30);
 svg+=lines(66,footY+78,['Bands cannot be multiplied into an exact personal stake. Acquired-status dates are not verified transaction or employment dates.','The MEB INC / MEB NY INC identity join is unresolved. Registry identifiers remain provisional and are omitted. Inferent is unverified and unconnected.'],22,30);
 svg+=txt(66,H-38,'Scout schedule bands differ from other historical narratives; dates remain unresolved. Ophir CEO/CCO acquired field does not independently date CCO duties.',21,'#627486');
 svg+='</svg>';fs.writeFileSync(path.join(here,`ownership-${version}.svg`),svg);
}
fs.writeFileSync(path.join(here,'layout-metrics.json'),JSON.stringify(metrics,null,2));
console.log(JSON.stringify(metrics,null,2));
