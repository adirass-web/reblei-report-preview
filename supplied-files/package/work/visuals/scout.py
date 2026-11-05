"""Regenerate the eight Scout figures from the accepted evidence index only.

The plot coordinates are presentation choices. Financial values are read from
accepted normalized facts, with exact Decimal reconciliation before plotting.
"""
from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import json
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.ticker import FuncFormatter


PALETTE = {"Assets": "#2563A6", "Liabilities": "#B46A00",
           "Equity / capital": "#087F6D", "Scenarios": "#7953A6",
           "Unknown / unavailable": "#6B7280"}
ATTENTION = "#A61B50"
INK = "#17212F"


def _wrap(s, width=68):
    return "\n".join(textwrap.fill(part, width) for part in s.split("\n"))


def _money(v):
    d = Decimal(str(v))
    return ("−" if d < 0 else "") + "$" + f"{abs(d):,.0f}"


def _axes(ax, ylabel="USD millions"):
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color="#E4E7EB", linewidth=.7)
    ax.set_ylabel(ylabel)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.tick_params(labelsize=11)


def _card(ax, xy, width, height, text, color, size=12):
    ax.add_patch(FancyBboxPatch(xy, width, height,
                 boxstyle="round,pad=0.015,rounding_size=0.025",
                 facecolor="white", edgecolor=color, linewidth=1.5))
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text,
            ha="center", va="center", fontsize=size, color=INK)


def _arrow(ax, start, end, color=None):
    ax.annotate("", end, start, arrowprops=dict(arrowstyle="->",
                color=color or PALETTE["Equity / capital"], lw=1.5))


def _waterfall(labels, values, totals, title, colors, notes=None):
    fig, ax = plt.subplots(figsize=(10, 6.5))
    cumulative = Decimal(0)
    endpoints = []
    for i, (value, total, color) in enumerate(zip(values, totals, colors)):
        value = Decimal(str(value))
        if total:
            bottom, height = Decimal(0), value
            cumulative = value
        else:
            bottom, height = min(cumulative, cumulative + value), abs(value)
            cumulative += value
        ax.bar(i, float(height / 1000000), bottom=float(bottom / 1000000),
               color=color, edgecolor=INK, linewidth=.6,
               hatch="//" if not total and value < 0 else None, width=.65)
        ax.text(i, float((bottom + height) / 1000000) + .27,
                _money(value), ha="center", va="bottom", fontsize=11)
        endpoints.append(float(cumulative / 1000000))
        if i and not total:
            ax.plot([i - .675, i - .325], [endpoints[i-1]] * 2,
                    color=PALETTE["Unknown / unavailable"], lw=1)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_title(title, loc="left", fontsize=16, fontweight="bold", pad=22)
    _axes(ax)
    ax.set_ylim(0, max(endpoints) * 1.2)
    if notes:
        fig.text(.105, .025, _wrap(notes, 95), fontsize=11, color=INK)
    fig.subplots_adjust(left=.11, right=.98, bottom=.25, top=.85)
    return fig


def build(index: dict, output: Path) -> list[dict]:
    """Return/write a manifest; ``output`` is the presentation directory."""
    output = Path(output)
    directory = output / "figures" / "scout"
    directory.mkdir(parents=True, exist_ok=True)
    records = {r["id"]: r for r in index["records"]}
    documents = {r["id"]: r for r in index["documents"]}
    manifests = []

    def record(id):
        r = records[id]
        if r.get("dossier_id") != "scout":
            raise ValueError(f"Wrong lane: {id}")
        if "deferred" in r.get("collection", "") or r.get("disposition") == "deferred":
            raise ValueError(f"Deferred record: {id}")
        return r

    def amount(id):
        r = record(id)
        if r.get("value_decimal") is None:
            raise ValueError(f"No accepted numeric value: {id}")
        return Decimal(r["value_decimal"])

    def row(id, label, condition="Reported firm amount; no personal allocation.", **extra):
        r = record(id)
        return dict(label=label, value_decimal=r.get("value_decimal"),
                    amount_raw=r.get("amount_raw"),
                    date_basis=r.get("as_of") or
                        (f"{r.get('period_start')} to {r.get('period_end')}"
                         if r.get("period_end") else r.get("date_basis") or r.get("date")),
                    unit=r.get("unit", "USD"), conditions=condition,
                    source_record_ids=[id] + ([r["source_record_id"]]
                        if r.get("source_record_id") else []), **extra)

    def calc(id):
        r = record(id)
        assert r["evaluation"]["status"] == "reconciled", id
        assert Decimal(r["evaluation"]["residual"]) == 0, id
        return r

    def save(id, title, summary, limitation, anchor, appendix, kind, table,
             sources, fig, legend=None):
        ids = sorted(set(sources + [s for r in table for s in r["source_record_ids"]]))
        # Check the selected records and their complete accepted dependency graph.
        seen = set()
        def closure(id):
            if id in seen:
                return
            seen.add(id)
            r = record(id)
            for citation in r.get("source_citations", []):
                if citation.startswith("doc:"):
                    docid = citation[4:].split("#")[0]
                    assert documents[docid]["dossier_id"] == "scout", citation
            for dep in r.get("dependencies", []):
                closure(dep)
        for source in ids:
            closure(source)
        prefix = f"figures/scout/{id}"
        entry = dict(id=id, lane="scout", title=title, summary=summary,
                     limitation=limitation, section_anchor=anchor, appendix=appendix,
                     svg=prefix + ".svg", png=prefix + ".png", csv=prefix + ".csv",
                     json=prefix + ".json", table=table, source_record_ids=ids,
                     kind=kind, legend=legend or {**PALETTE, "Key finding / source difference": ATTENTION},
                     alt=f"{title}. {summary} Limitation: {limitation}")
        fig.savefig(directory / f"{id}.svg", format="svg", facecolor="white",
                    metadata={"Date": None, "Creator": "Scout evidence figures"})
        fig.savefig(directory / f"{id}.png", dpi=160, facecolor="white",
                    metadata={"Software": "Scout evidence figures"})
        plt.close(fig)
        (directory / f"{id}.json").write_text(
            json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        fields = list(dict.fromkeys(k for r in table for k in r))
        with (directory / f"{id}.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fields)
            writer.writeheader()
            for r in table:
                writer.writerow({k: json.dumps(v, ensure_ascii=False)
                                 if isinstance(v, (list, dict)) else v for k, v in r.items()})
        svg = ET.parse(directory / f"{id}.svg")
        assert any(e.tag.endswith("}text") for e in svg.iter()), id
        assert not any(e.tag.rsplit("}", 1)[-1] in {"script", "foreignObject"}
                       for e in svg.iter()), id
        manifests.append(entry)

    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 12,
                         "svg.fonttype": "none", "svg.hashsalt": "scout-accepted-v1",
                         "text.parse_math": False,
                         "axes.labelcolor": INK, "text.color": INK,
                         "xtick.color": INK, "ytick.color": INK}):
        # 1. Dated documentary snapshots are separate from undated capture bands.
        ownership = [
            ("prof-scout-reorganization", "Before 2012-08-31", "NAYS LLC and MEB NY Inc → Scout", "Prior owners; percentages unstated in note."),
            ("prof-scout-reorganization", "From 2012-08-31", "NAYS LLC and MEB NY Inc → Finch → Scout", "Finch owns 100% of Scout; NAYS/MEB split unstated in note."),
            ("prof-scout-2013-parent", "As of 2013-12-31", "Finch → Scout", "Wholly owned subsidiary in 2013 financial statements."),
            ("prof-scout-direct-band", "Reported start 2009-05", "Bleich direct in Scout", "Less than 5%; distinct from indirect interests."),
            ("prof-scout-michael-meb-band", "Reported start 2009-05", "Bleich in MEB", "75% or more; intervening level, not ultimate Scout percentage."),
            ("prof-scout-meb-finch-band", "Reported start 2012-08", "MEB through Finch", "50% but less than 75%."),
            ("prof-scout-nays-finch-band", "Reported start 2012-08", "NAYS through Finch", "25% but less than 50%."),
            ("prof-scout-niv-nays-band", "Reported start 2009-05", "Niv through NAYS", "25% but less than 50%."),
            ("prof-scout-finch-band", "Reported start 2012-08", "Finch direct in Scout", "75% or more; separate BrokerCheck category."),
        ]
        table = [dict(label=label, relationship=relation, amount_raw=record(id).get("ownership_raw"),
                     value_decimal=None, date_basis=date, unit="ownership disclosure",
                     conditions=condition, source_record_ids=[id])
                 for id, date, relation, condition in ownership
                 for label in [relation]]
        fig, axs = plt.subplots(3, 1, figsize=(10, 12), gridspec_kw={"height_ratios": [1.1, 1.4, 2.6]})
        for ax in axs:
            ax.set_xlim(0, 10); ax.set_ylim(0, 3); ax.axis("off")
        fig.suptitle("Scout ownership: dated notes and separately scoped bands", x=.04,
                     ha="left", fontsize=16, fontweight="bold", y=.98)
        axs[0].text(0, 2.7, "Financial-note history • before August 31, 2012", fontsize=13, fontweight="bold")
        _card(axs[0], (.1, .7), 3.5, 1.2, "NAYS LLC + MEB NY Inc\nPercentages unstated", PALETTE["Unknown / unavailable"])
        _card(axs[0], (6.2, .7), 3.5, 1.2, "Scout Trading LLC", PALETTE["Equity / capital"])
        _arrow(axs[0], (3.7, 1.3), (6.1, 1.3))
        axs[1].text(0, 2.8, "Financial-note history • from August 31, 2012", fontsize=13, fontweight="bold")
        _card(axs[1], (.1, 1), 3, 1.2, "NAYS + MEB\nFinch split unstated", PALETTE["Unknown / unavailable"])
        _card(axs[1], (3.8, 1), 2.4, 1.2, "Finch", PALETTE["Equity / capital"])
        _card(axs[1], (7, 1), 2.7, 1.2, "Scout", PALETTE["Equity / capital"])
        _arrow(axs[1], (3.15, 1.6), (3.75, 1.6)); _arrow(axs[1], (6.25, 1.6), (6.95, 1.6))
        axs[1].text(6.6, 2.4, "100%", ha="center", fontsize=12)
        axs[1].text(0, .25, "2013-12-31 statements also identify Finch as wholly owning parent.", fontsize=12)
        axs[2].text(0, 2.9, "Scout BrokerCheck • capture date unknown; relationship starts shown", fontsize=12, fontweight="bold")
        bands = [("May 2009", "Bleich direct in Scout", "Less than 5%"),
                 ("May 2009", "Bleich in MEB", "75% or more"),
                 ("Aug 2012", "MEB through Finch", "50% to <75%"),
                 ("Aug 2012", "NAYS through Finch", "25% to <50%"),
                 ("May 2009", "Niv through NAYS", "25% to <50%"),
                 ("Aug 2012", "Finch direct in Scout", "75% or more")]
        for i, (date, relation, band) in enumerate(bands):
            y = 2.45 - i * .38
            axs[2].text(.05, y, date, fontsize=11)
            axs[2].text(1.8, y, relation, fontsize=12)
            axs[2].text(6.7, y, band, fontsize=12, color=PALETTE["Equity / capital"])
            axs[2].axhline(y - .12, color="#E4E7EB", lw=.7)
        fig.text(.05, .03, "Bands are retained at each disclosed level; no multiplication or personal asset allocation.", fontsize=12)
        fig.subplots_adjust(left=.05, right=.98, top=.94, bottom=.07, hspace=.25)
        save("scout-historical-ownership", "Historical Scout ownership disclosures",
             "Financial notes date the Finch reorganization to August 31, 2012 and identify Finch as wholly owning Scout in 2013. BrokerCheck bands are shown separately at their disclosed levels.",
             "BrokerCheck capture dates are unknown. Relationship-start dates are historical disclosures; bands are not exact ultimate ownership. No firm asset or distribution is allocated to Bleich.",
             "historical-profile-roles-and-ownership", False, "dated-ownership-panels", table, [], fig)

        # 2. Five independently reconciled snapshots, with a separate equity scale.
        table = []; values = []
        for year in range(2009, 2014):
            c = calc(f"calc-scout-{year}-balance-equation")
            asset, liab, equity = c["comparison_target"], c["operands"]["v0"], c["operands"]["v1"]
            assert amount(asset) == amount(liab) + amount(equity)
            values.append((float(amount(asset)/1000000), float(amount(liab)/1000000), float(amount(equity)/1000000)))
            table.extend(row(id, label, year=str(year)) for id, label in [(asset,"Assets"),(liab,"Liabilities"),(equity,"Members' capital")])
        fig, (ax, eq) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [2, 1.2]})
        xs = list(range(5))
        ax.bar(xs, [v[1] for v in values], label="Liabilities", color=PALETTE["Liabilities"], hatch="//")
        ax.bar(xs, [v[2] for v in values], bottom=[v[1] for v in values], label="Members' capital", color=PALETTE["Equity / capital"])
        ax.scatter(xs, [v[0] for v in values], marker="D", color=PALETTE["Assets"], s=55, label="Assets = total height", zorder=3)
        for i,v in enumerate(values):
            ax.text(i, v[0]+4, f"${v[0]:.2f}m", ha="center", fontsize=11)
        ax.set_title("Year-end liabilities + members' capital = assets", loc="left", fontsize=16, fontweight="bold", pad=20)
        ax.set_xticks(xs, range(2009,2014)); _axes(ax); ax.set_ylim(0,190)
        ax.legend(loc="upper left", fontsize=11, frameon=False)
        eq.bar(xs, [v[2] for v in values], color=PALETTE["Equity / capital"])
        eq.set_xticks(xs, range(2009,2014)); _axes(eq); eq.set_ylim(0,11)
        eq.set_title("Members' capital • separate scale", loc="left", fontsize=13)
        for i,v in enumerate(values):
            eq.text(i,v[2]+.3,f"${v[2]:.2f}m",ha="center",fontsize=11)
        fig.subplots_adjust(left=.1,right=.98,bottom=.08,top=.91,hspace=.55)
        save("scout-balance-snapshots", "Five Scout balance sheets reconcile at reported precision",
             "For every December 31 from 2009 through 2013, reported liabilities plus members' capital equal assets. The lower panel gives capital its own scale; exact dollars appear in the data table.",
             "These are historical firm-level gross balances. Members' capital differs from personal net worth and from regulatory capital; no owner allocation is inferred.",
             "balance-sheets-and-available-operations", False, "stacked-balance-and-capital", table,
             [f"calc-scout-{y}-balance-equation" for y in range(2009,2014)], fig)

        # 3. Compare like flow periods; retain two unavailable periods explicitly.
        table = []; profit=[]; cash=[]
        for year in range(2009,2012):
            p = calc(f"calc-scout-{year}-" + ("income-less-expenses" if year==2009 else "net-income"))["comparison_target"]
            c = calc(f"calc-scout-{year}-operating-cash")["comparison_target"]
            profit.append(float(amount(p)/1000000)); cash.append(float(amount(c)/1000000))
            table.extend(row(id, label, "2009 is February 5–December 31 inception period; 2010/2011 are calendar years.",year=str(year)) for id,label in [(p,"Net income / (loss)"),(c,"Operating cash flow")])
        for year in [2012,2013]:
            table.extend(dict(label=label, value_decimal=None, amount_raw=None, date_basis=f"Year {year}",unit="USD",conditions="Full flow statement absent from supplied copy; unavailable, not zero.",source_record_ids=["fin-scout-finding-missing-flow-statements"],year=str(year)) for label in ["Net income / (loss)","Operating cash flow"])
        fig,ax=plt.subplots(figsize=(10,6.5))
        ax.bar([x-.18 for x in range(3)],profit,.34,label="Net income / (loss)",color=PALETTE["Equity / capital"])
        ax.bar([x+.18 for x in range(3)],cash,.34,label="Operating cash flow",color=PALETTE["Assets"],hatch="//")
        for i in range(3):
            for dx,v in [(-.18,profit[i]),(.18,cash[i])]:
                ax.text(i+dx,v+(.2 if v>=0 else -.25),f"{v:.2f}",ha="center",va="bottom" if v>=0 else "top",fontsize=11)
        for x in [3,4]:
            ax.add_patch(Rectangle((x-.4,-6.5),.8,13,fill=False,hatch="..",edgecolor=PALETTE["Unknown / unavailable"],lw=1))
            ax.text(x,0,"Full flow\nstatements\nunavailable",ha="center",va="center",fontsize=11,bbox=dict(facecolor="white",edgecolor="none",pad=4))
        ax.axhline(0,color=INK,lw=1); ax.set_ylim(-7,8);ax.set_xlim(-.6,4.6)
        ax.set_xticks(range(5),["2009*","2010","2011","2012","2013"]);_axes(ax)
        ax.set_title("Reported profit and operating cash flow diverge",loc="left",fontsize=16,fontweight="bold",pad=34)
        ax.text(0,1.025,"Key finding: profits in 2010/2011 coexist with operating cash outflows",
                transform=ax.transAxes,fontsize=11,fontweight="bold",color=ATTENTION)
        ax.legend(loc="upper left",fontsize=11,frameon=False)
        fig.text(.1,.025,"* 2009 covers February 5–December 31, not a full calendar year. Labels: USD millions.",fontsize=11)
        fig.subplots_adjust(left=.1,right=.98,bottom=.15,top=.88)
        save("scout-profit-operating-cash", "Profit versus operating cash flow, 2009–2013 coverage",
             "Key finding: operating cash flow is negative in all three supplied flow periods, while reported 2010 and 2011 net income is positive. 2012 and 2013 are explicitly unavailable.",
             "2009 is the shorter inception period. The final 2011 net-income figure is used, distinct from the income subtotal also labeled 'Net Income' in the source. Missing flow statements cannot be treated as zero or reconstructed from balance changes.",
             "cash-presentation-and-missing-flows",False,"profit-and-cash-bars",table,
             ["fin-scout-finding-missing-flow-statements","fin-scout-finding-income-capital-2009-2011"],fig)

        # 4. One accepted aggregate members' capital bridge.
        capital_ids=["norm-b2-0076","norm-b2-0078","norm-b2-0077","norm-b2-0079"]
        capital=[amount(id) for id in capital_ids]
        assert capital[0]+capital[1]+capital[2]==capital[3]
        calc("calc-scout-2011-capital-bridge")
        table=[row(id,label,"Aggregate firm members' capital; no member-specific receipt established.") for id,label in zip(capital_ids,["Opening capital","Net income","Distributions","Closing capital"])]
        fig=_waterfall(["Opening\n2010-12-31","2011\nnet income","2011 aggregate\ndistributions","Closing\n2011-12-31"],capital,[True,False,False,True],"2011 members' capital bridge",[PALETTE["Equity / capital"]]*4,"All amounts are firm aggregates. Distributions are not allocated to Bleich or any other named member.")
        save("scout-2011-capital-waterfall","2011 members' capital: opening balance to closing balance",
             "$6,138,252 opening capital plus $5,469,261 net income less $2,859,153 aggregate distributions equals $8,748,360 closing capital.",
             "This accepted arithmetic bridge is firm-level. It does not identify distribution recipients or establish personal income or receipts.",
             "balance-sheets-and-available-operations",False,"capital-waterfall",table,["calc-scout-2011-capital-bridge","fin-scout-finding-aggregate-capital-transactions"],fig)

        # 5. Equal-spaced chronology cards: spacing is explicitly not elapsed time.
        events=[
          ("2013-01-28","CBOE 12-0059","Two-sided quotes • censure + $10,000 firm fine","Settlement; firm reports paid 2013-02-04",["prof-matter-cboe-quote","b4-007-12","b4-007-13"]),
          ("2013-06-26","CBOE 12-0099 / 12-0126","CCO / principal registration • censure + $7,500 firm fine","Settlement; no payment proof inferred",["prof-matter-cboe-registration","b4-007-8"]),
          ("2014-05-23","CBOE 14-0018","Rule 611 policies / surveillance • censure + $5,000 firm fine","Settlement; no payment proof inferred",["prof-matter-cboe-trade-through","b4-007-5"]),
          ("2014-07-17","Business cessation / BDW","BrokerCheck cessation; AWC reports BDW filing","Nasdaq membership termination separately 2014-08-18",["prof-scout-ceased"]),
          ("2015-04-01","Nasdaq execution / election","Bleich signs as Scout Managing Member","Quarterly payment election over four years; no receipts",["prof-scout-awc-signature","fin-scout-finding-fine-election"]),
          ("2015-04-07","Nasdaq AWC 20100243866-01","Regulation SHO / supervision • censure + $3,000,000 firm fine","Consent without admission or adjudication; completion unknown",["prof-matter-nasdaq","norm-b1-9-12","fin-scout-finding-fine-election"]),
        ]
        table=[]
        for date,matter,text,evidence,event_ids in events:
            monetary=next((record(id) for id in event_ids if record(id).get("value_decimal") is not None),None)
            table.append(dict(label=matter,date_basis=date,
                              value_decimal=monetary.get("value_decimal") if monetary else None,
                              amount_raw=monetary.get("amount_raw") if monetary else None,
                              unit="USD fine" if monetary else "dated event",
                              conditions=f"{text}. {evidence}. Firm respondent; no personal fine.",source_record_ids=event_ids))
        fig,ax=plt.subplots(figsize=(10,10.5));ax.set_xlim(0,10);ax.set_ylim(-.2,7.9);ax.axis("off")
        ax.text(0,7.65,"Scout regulatory chronology and payment-evidence limits",fontsize=16,fontweight="bold")
        ax.text(0,7.15,"Chronological rows • equal spacing does not represent elapsed time",fontsize=11,color=PALETTE["Unknown / unavailable"])
        ax.plot([1.7,1.7],[.6,6.6],color=PALETTE["Liabilities"],lw=1.5)
        for i,(date,matter,text,evidence,_) in enumerate(events):
            y=6.5-i*1.16
            ax.text(0,y+.08,date,fontsize=12,fontweight="bold",va="top")
            ax.scatter([1.7],[y],marker="s" if "election" in matter else "o",s=65,color=PALETTE["Scenarios"] if "election" in matter else PALETTE["Unknown / unavailable"] if "cessation" in matter else PALETTE["Liabilities"])
            ax.text(2.05,y+.12,matter,fontsize=12,fontweight="bold",va="top")
            ax.text(2.05,y-.18,_wrap(text,72),fontsize=11,va="top")
            ax.text(2.05,y-.54,_wrap(evidence,76),fontsize=11,va="top",color=PALETTE["Unknown / unavailable"])
        fig.text(.06,.035,"Nasdaq: investigated 2010-01-01–2012-03-16; applicable membership period\n2011-11-09–2012-03-16. Scout is the respondent; Bleich is a representative signatory.",fontsize=11)
        fig.subplots_adjust(left=.05,right=.98,bottom=.12,top=.97)
        save("scout-regulatory-timeline","Scout firm regulatory chronology and payment evidence",
             "Three CBOE settlements precede the 2015 Nasdaq AWC. The quote-fine payment is a firm-reported statement. Nasdaq's $3 million sanction and payment election remain distinct from receipt or completion evidence.",
             "All four matters identify Scout as respondent. Bleich's representative signature does not impose a personal fine. The Nasdaq AWC is consented without admission or adjudication. Supplied evidence establishes no current balance or payment completion; chronology spacing is not elapsed time.",
             "chronology-and-regulatory-record",False,"regulatory-timeline",table,[],fig)

        # 6. Principal snapshots plus a source-reported transaction; no full cash bridge.
        debt_ids=["norm-b2-0116","norm-b2-0192","norm-b3-r0212"]
        table=[row(id,"Subordinated principal", "Year-end reported principal; lender/member identity not inferred.") for id in debt_ids]
        table.append(row("norm-b3-r0215","Reported principal repayment to NAYS","2013 note reports principal repayment plus unquantified unpaid interest; not independently authenticated."))
        assert amount(debt_ids[1])-amount("norm-b3-r0215")==amount(debt_ids[2])
        fig,(ax,note)=plt.subplots(2,1,figsize=(10,7.5),gridspec_kw={"height_ratios":[2,1]})
        ax.bar(range(3),[float(amount(id)/1000000) for id in debt_ids],width=.55,color=PALETTE["Liabilities"],hatch="//")
        ax.set_xticks(range(3),["2011-12-31","2012-12-31","2013-12-31"]);_axes(ax);ax.set_ylim(0,11)
        for i,id in enumerate(debt_ids):ax.text(i,float(amount(id)/1000000)+.3,_money(amount(id)),ha="center",fontsize=12)
        ax.set_title("Subordinated debt: reported principal snapshots",loc="left",fontsize=16,fontweight="bold",pad=20)
        note.axis("off")
        note.text(0,.85,"2013-10-08 • reported principal repayment to NAYS: $5,000,000",fontsize=13,fontweight="bold",transform=note.transAxes)
        note.text(0,.52,"$9,000,000 − $5,000,000 = $4,000,000 reconciles endpoints only.",fontsize=12,transform=note.transAxes)
        note.text(0,.19,"Unpaid interest is unquantified; complete 2012/2013 debt cash movements\nare not reconstructible from the supplied copies.",fontsize=12,transform=note.transAxes)
        fig.subplots_adjust(left=.11,right=.98,bottom=.06,top=.9,hspace=.35)
        save("scout-subordinated-debt","Subordinated principal and the reported 2013 repayment",
             "Reported year-end subordinated principal is $9 million in 2011, $9 million in 2012 and $4 million in 2013. The 2013 note reports $5 million principal repaid to NAYS on October 8 plus unquantified unpaid interest.",
             "Endpoint arithmetic is not a complete gross borrowing or cash-flow bridge. Repayment is source-reported, not independently authenticated. The unnamed member in earlier notes is not identified as Bleich; unpaid interest is unknown, not zero.",
             "subordinated-debt-member-balances-and-parent-payments",True,"debt-snapshots",table,["fin-scout-finding-subdebt-repayment","fin-scout-finding-missing-flow-statements"],fig)

        # 7. Regulatory-capital steps, each read from the accepted supplementary schedule.
        ids=["norm-b2-0128","norm-b2-0129","norm-b2-0135","norm-b2-0137","norm-b2-0138","norm-b2-0141","norm-b2-0142"]
        vals=[amount(id) for id in ids]
        assert vals[0]+vals[1]-vals[2]-vals[3]==vals[4]
        assert vals[4]-vals[5]==vals[6]
        calc("calc-scout-2011-net-capital")
        labels=["Ownership capital","Eligible subordinate liabilities","Nonallowable assets deduction","Securities haircuts deduction","Adjusted net capital","Required capital","Excess net capital"]
        table=[row(id,label,"2011-12-31 regulatory schedule. Deductions shown as source magnitudes; plotted as subtraction." if i in [2,3,5] else "2011-12-31 regulatory schedule; not a measure of personal net worth.") for i,(id,label) in enumerate(zip(ids,labels))]
        fig=_waterfall(["Ownership\ncapital","Eligible\nsubdebt","Nonallowable\nassets","Securities\nhaircuts","Adjusted\nnet capital","Required\ncapital","Excess\nnet capital"],[vals[0],vals[1],-vals[2],-vals[3],vals[4],-vals[5],vals[6]],[True,False,False,False,True,False,True],"2011 regulatory capital bridge",[PALETTE["Equity / capital"],PALETTE["Liabilities"],PALETTE["Assets"],PALETTE["Equity / capital"],PALETTE["Equity / capital"],PALETTE["Equity / capital"],PALETTE["Equity / capital"]],"Regulatory capital includes eligible subordinated liabilities and specific deductions. It is distinct from equity and personal wealth.")
        # A retained $1 source difference in a separate table is not a bridge adjustment.
        sector=record("calc-scout-2011-common-sector-total")
        sector_sum=sum(amount(id) for id in sector["operands"].values())
        reported=amount(sector["comparison_target"])
        assert sector_sum==Decimal(sector["evaluation"]["exact_result"])
        assert sector_sum-reported==Decimal(sector["evaluation"]["residual"])==Decimal(-1)
        table.extend(row(id,"Common-stock sector component", "Separate fair-value table; retained source difference, not an adjustment to regulatory capital.") for id in sector["operands"].values())
        table.append(row(sector["comparison_target"],"Reported common-stock subtotal", "Separate fair-value table; retained source difference, not an adjustment to regulatory capital."))
        table.append(dict(label="Sum of eleven displayed common-stock sectors",value_decimal=str(sector_sum),amount_raw=None,date_basis="2011-12-31",unit="USD",conditions="Accepted calculation result; one dollar below reported subtotal. No balancing entry or materiality conclusion.",source_record_ids=[sector["id"],"fin-scout-finding-sector-one-dollar"]))
        fig.set_size_inches(10,8.5)
        fig.subplots_adjust(bottom=.36)
        fig.texts[0].set_position((.105,.2))
        fig.text(.105,.055,"Source difference • separate 2011 common-stock table\nEleven sector rows sum to $500,977; reported subtotal is $500,978.\nThe $1 difference is retained; no balancing entry or materiality conclusion.",
                 fontsize=11,fontweight="bold",color=ATTENTION,
                 bbox=dict(boxstyle="round,pad=.6",facecolor="white",edgecolor=ATTENTION,linewidth=1.4))
        save("scout-2011-regulatory-capital","2011 regulatory capital: equity, eligible debt and deductions",
             "$8,748,360 ownership capital plus $9,000,000 eligible subordinate liabilities, less $1,064,476 nonallowable assets and $578,431 haircuts, gives $16,105,453 adjusted net capital. Deducting $224,902 required capital leaves $15,880,551 excess. Source difference: a separate common-stock table's eleven sector rows sum to $500,977 versus the reported $500,978 subtotal.",
             "This is the supplied December 31, 2011 regulatory schedule. Regulatory capital differs from members' capital, liquid cash and personal net worth. Deduction magnitudes are plotted as subtraction. The separate $1 common-stock source difference is retained without a balancing entry, adjustment to this bridge or materiality conclusion.",
             "regulatory-capital-retained-differences-and-fine-illustration",True,"regulatory-capital-waterfall",table,["calc-scout-2011-net-capital","fin-scout-finding-ppe-fairvalue-capital"],fig)

        # 8. Supplied-copy statement coverage; missing statements never become zero.
        table=[]
        categories=["Balance sheet","Operations","Members' capital\nrollforward","Cash flows"]
        for year in range(2009,2014):
            c=calc(f"calc-scout-{year}-balance-equation")
            for j,label in enumerate(categories):
                available= j==0 or year<=2011
                sources=[c["comparison_target"]] if j==0 else ([f"calc-scout-{year}-operating-cash"] if j==3 and available else [f"calc-scout-{year}-"+("income-less-expenses" if year==2009 else "net-income")] if j==1 and available else [f"calc-scout-{year}-"+("shown-capital-components" if year==2009 else "capital-bridge")] if j==2 and available else ["fin-scout-finding-missing-flow-statements"])
                table.append(dict(label=label.replace("\n"," "),year=str(year),value_decimal=None,amount_raw=None,date_basis="February 5–December 31, 2009 inception period" if year==2009 else f"Calendar year {year}; balance at December 31",unit="statement coverage",conditions="Supplied" if available else "Full statement absent; notes and endpoint balances do not replace flow statements.",status="Supplied" if available else "Unavailable",source_record_ids=sources))
        fig,ax=plt.subplots(figsize=(10,6));ax.set_xlim(-.5,4.5);ax.set_ylim(3.6,-.8)
        for r in table:
            x=int(r["year"])-2009;y=[s.replace("\n"," ") for s in categories].index(r["label"]);yes=r["status"]=="Supplied"
            ax.add_patch(Rectangle((x-.43,y-.33),.86,.66,facecolor="white",edgecolor=PALETTE["Assets"] if yes else PALETTE["Unknown / unavailable"],hatch=None if yes else "..",lw=1.4))
            ax.text(x,y,"✓ Supplied" if yes else "— Missing",ha="center",va="center",fontsize=11,color=PALETTE["Assets"] if yes else PALETTE["Unknown / unavailable"],bbox=dict(facecolor="white",edgecolor="none",pad=1))
        ax.set_xticks(range(5),["2009*","2010","2011","2012","2013"]);ax.xaxis.tick_top()
        ax.set_yticks(range(4),categories);ax.tick_params(length=0,pad=10,labelsize=12)
        for s in ax.spines.values():s.set_visible(False)
        fig.suptitle("Statement coverage in the supplied annual-report copies",x=.04,ha="left",fontsize=16,fontweight="bold",y=.97)
        fig.text(.04,.07,"* 2009 is the inception period. The file named 'Annual Report 2010 Remarks.pdf'\nsupplies 2009 flows. A separate 2009 balance-sheet copy is not another year.\n2012/2013 notes contain selected amounts, but the full flow statements are absent.",fontsize=11)
        fig.subplots_adjust(left=.23,right=.98,bottom=.27,top=.8)
        save("scout-statement-coverage","Coverage of five years of supplied Scout statements",
             "Balance sheets are supplied for all five 2009–2013 year ends. Full operations, members' capital and cash-flow statements are available for 2009–2011; their 2012/2013 counterparts are absent from the supplied copies.",
             "2009 covers inception February 5–December 31 and is contained in a file labeled 2010 Remarks. The separate 2009 condition copy is not a sixth year. Missing full statements do not mean no activity; selected note disclosures cannot reconstruct annual flows.",
             "basis-and-reading-guide",True,"statement-coverage-matrix",table,["fin-scout-finding-missing-flow-statements"],fig)

    assert len(manifests)==8
    (directory/"manifest.json").write_text(json.dumps(manifests,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifests


if __name__ == "__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    manifest=build(json.loads(args.index.read_text(encoding="utf-8")),args.output)
    print(f"Generated {len(manifest)} Scout figures with SVG, PNG, CSV and JSON; source closure and exact reconciliations passed.")
