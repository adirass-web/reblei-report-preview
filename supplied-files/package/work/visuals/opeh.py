"""Deterministic, source-scoped OPEH figures; no account roll-forward is performed.

Run with system Python (Matplotlib): opeh.py --index data/evidence-index.json
--output presentation. The public build(index, output) returns manifest entries.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from decimal import Decimal
import json
import os
from pathlib import Path
import textwrap
import xml.etree.ElementTree as ET

os.environ.setdefault("MPLCONFIGDIR", "/tmp/reblei-opeh-matplotlib")
os.environ.setdefault("XDG_CACHE_HOME", "/tmp/reblei-opeh-cache")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

COLORS = {"assets": "#2563A6", "liabilities": "#B46A00", "equity": "#087F6D",
          "scenarios": "#7953A6", "unknown": "#6B7280", "attention": "#A61B50"}
INK = "#172B40"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                     "svg.fonttype": "none", "svg.hashsalt": "opeh-visuals-v1",
                     "axes.unicode_minus": False, "text.parse_math": False})


def wrap(value, width=70):
    return "\n".join(textwrap.fill(line, width) for line in str(value).split("\n"))


def canvas(title, subtitle, height=7.3):
    fig = plt.figure(figsize=(10, height), facecolor="white")
    ax = fig.add_axes([.055, .055, .89, .81])
    ax.set(xlim=(0, 1), ylim=(0, 1)); ax.axis("off")
    fig.text(.055, .952, title, fontsize=18, fontweight="bold", color=INK, va="top")
    fig.text(.055, .905, wrap(subtitle, 100), fontsize=11, color="#475569", va="top")
    return fig, ax


def card(ax, x, y, w, h, heading, body, color="unknown", fontsize=12, dashed=False):
    c = COLORS.get(color, color)
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.012",
                              facecolor="white", edgecolor=c, linewidth=1.5,
                              linestyle="--" if dashed else "-"))
    ax.add_patch(Rectangle((x, y), .008, h, facecolor=c, linewidth=0))
    ax.text(x+.025, y+h-.025, heading, fontsize=13, fontweight="bold", va="top", color=c)
    ax.text(x+.025, y+h-.075, body, fontsize=fontsize, va="top", color=INK, linespacing=1.45)


def money(value):
    return "$" + format(Decimal(str(value)), ",.2f")


class Sources:
    def __init__(self, index):
        self.index = index
        self.records = {r["id"]: r for r in index["records"]}

    def get(self, record_id):
        if record_id not in self.records:
            raise ValueError(f"Missing accepted record {record_id}")
        r = self.records[record_id]
        if r["dossier_id"] != "opeh":
            raise ValueError(f"Cross-lane or deferred record {record_id}")
        return r

    def value(self, record_id):
        r = self.get(record_id)
        return r["evaluation"]["display_result"] if r.get("evaluation") else r["value_decimal"]

    def row(self, record_id, label, date_basis=None, conditions=None, **extra):
        r = self.get(record_id)
        ev = r.get("evaluation") or {}
        return dict(label=label, source_record_id=record_id,
                    value=ev.get("display_result", r.get("value_decimal")),
                    exact_result=ev.get("exact_result", r.get("value_decimal")),
                    amount_raw=r.get("amount_raw"),
                    date_basis=date_basis or r.get("calculation_scope") or r.get("date_roles") or r.get("event_date"),
                    conditions=conditions or r.get("assumptions") or r.get("statement"),
                    status=ev.get("status", r.get("evidentiary_status")), **extra)

    def closure(self, ids):
        seen = set()
        def visit(record_id):
            if record_id in seen:
                return
            r = self.get(record_id); seen.add(record_id)
            for dependency in r.get("dependencies", []):
                visit(dependency)
        for record_id in ids:
            visit(record_id)
        return sorted(seen)


def obligation(s):
    title = "One note principal, two named makers"
    summary = ("The January 11, 2018 note records one $2,233,007 principal for Michael E. Bleich and Alexis K. Bleich, "
               "with OPEH LLC as holder. Section 8 describes predecessor corporate-obligation and personal-guaranty capacity.")
    limitation = ("No equal maker allocation or additional predecessor principal is created. Predecessor/guaranty instruments, "
                  "funding trail and unique identity bridge to a regulated person are absent; the note date does not prove a new cash advance.")
    fig, ax = canvas(title, "Instrument capacities and recital; connecting lines describe roles, not cash movement.", 7.5)
    card(ax, .04, .73, .92, .21, "PREDECESSOR CONTEXT — amounts and earlier dates unknown",
         "Ophir Partners LLC corporate obligation to OPEH\nMakers’ personal guaranty recited in section 8", "unknown")
    ax.plot([.5, .5], [.63, .715], color=COLORS["unknown"], ls="--")
    ax.text(.52, .665, "note tendered in satisfaction / discharge (recital)", fontsize=11, va="center", color=INK)
    card(ax, .04, .34, .92, .27, "JANUARY 11, 2018 NOTE — ONE collective obligation",
         "One documented principal: " + money(s.value("norm-b1-34-35")) +
         "\nMichael E. Bleich + Alexis K. Bleich — named makers\nOPEH LLC — holder", "attention", 14)
    card(ax, .04, .04, .92, .23, "BOUNDARIES",
         "No individual shares allocated; no second principal added.\nCash advance and later payment status are unknown.\nNames in this instrument do not resolve regulated-person identity.", "unknown")
    ids = ["finding-opeh-one-principal", "finding-opeh-identity", "prof-opeh-corporate-predecessor", "prof-opeh-maker-identity", "norm-b1-34-35"]
    table = [s.row(i, s.get(i).get("concept", s.get(i).get("assertion_type", i))) for i in ids]
    return fig, dict(id="opeh-one-obligation", title=title, summary=summary, limitation=limitation,
                     section_anchor="parties-capacity-and-collateral", appendix=False, kind="capacity_diagram", table=table, source_record_ids=ids)


def chronology(s):
    title = "Procedural dates and the later administrative correction"
    summary = ("The source sequence runs from the 2018 note and creditor request to discontinuance without prejudice and without costs. "
               "The November 30 order, filed December 3, marked the motion moot and case disposed. December 2020 notices are a separate administrative correction.")
    limitation = ("The request was not a money award. Discontinuance supplies no payment, settlement consideration, release or later balance. "
                  "The December 10, 2020 correction does not establish reopening or extend the September 27, 2018 monetary scenario endpoint.")
    fig, ax = canvas(title, "Dated source events; spacing is for readability and does not measure elapsed time.", 10.4)
    entries = [
        ("event-opeh-note-20180111", "JAN 11, 2018", "Note as of date; delivery/loan alleged.\nPredecessor and guaranty recital qualifies funding description."),
        ("event-opeh-scheduled-maturity", "SEP 1, 2018", "Scheduled maturity; earlier transfer unknown.\nSubsequent Business Day clause applies to payment."),
        ("event-opeh-asserted-balance-20180917", "SEP 17, 2018", "Asserted accounting cutoff / requested interest start.\nDay-boundary convention unresolved."),
        ("event-opeh-demand-20180925", "SEP 25–27, 2018", "Demand Sep 25; affidavit apparently sworn Sep 26;\nsummons and CPLR 3213 motion filed Sep 27."),
        ("event-opeh-discontinuance-20181017", "OCT 17, 2018", "Notice discontinues without prejudice and without costs."),
        ("b1-16-18", "NOV 20 / 28, 2018", "Administrative notice / working-copy adjournment.\nNo monetary ruling recorded."),
        ("event-opeh-order-20181130", "NOV 30 / DEC 3, 2018", "Order date / filing date: motion moot, case disposed.\nNo requested money award appears."),
    ]
    ax.plot([.025, .025], [.25, .965], color=COLORS["assets"], lw=2)
    for n, (_, date, body) in enumerate(entries):
        y = .955 - n*.107
        ax.plot(.025, y, marker="o", ms=8, color=COLORS["assets"])
        ax.text(.06, y+.012, date, color=COLORS["assets"], weight="bold", fontsize=12, va="top")
        ax.text(.06, y-.022, body, fontsize=12, va="top", color=INK, linespacing=1.3)
    card(ax, .04, .02, .92, .17, "SEPARATE ADMINISTRATIVE INSET — DECEMBER 9–10, 2020",
         "Voluntary neutral-evaluation mailing, then next-day correction:\nerroneously sent to disposed matters; disregard / no further action.\nNo reopening or later accrual established.", "unknown", 12, True)
    ids = [e[0] for e in entries] + ["event-opeh-affidavit-20180926", "event-opeh-motion-20180927", "event-opeh-order-filed-20181203", "event-opeh-adr-notice-20201209", "event-opeh-adr-correction-20201210"]
    table = [s.row(i, s.get(i).get("event_type", "administrative adjournment")) for i in ids]
    return fig, dict(id="opeh-procedural-timeline", title=title, summary=summary, limitation=limitation,
                     section_anchor="instrument-and-procedural-chronology", appendix=False, kind="procedural_timeline", table=table, source_record_ids=ids)


def request(s):
    title = "The creditor’s requested components"
    summary = ("OPEH requested $2,233,007 principal and asserted $155,070 accrued interest, plus 15% / $930.42 daily from September 17, 2018 "
               "and unquantified fees/costs. The demand addition reconciles to $2,388,077; the daily amount reconciles after cent rounding.")
    limitation = ("These are creditor assertions and component checks, not an award or established balance. The $155,070 accrual period, "
                  "rounding method and operative default date remain unresolved. Unknown fees are not zero and no current balance is projected.")
    fig, ax = canvas(title, "USD; demand addition and motion request retain their different source dates.", 7.8)
    principal = s.value("norm-b1-25-26"); interest = s.value("norm-b1-25-26-01")
    total = s.value("calc-opeh-demand-addition")
    ax.text(.02, .965, "SEPTEMBER 25 DEMAND — component addition only", fontsize=12, weight="bold", color=INK)
    p = float(Decimal(principal)/Decimal(total))
    ax.add_patch(Rectangle((.02, .78), .96*p, .12, facecolor=COLORS["liabilities"]))
    ax.add_patch(Rectangle((.02+.96*p, .78), .96*(1-p), .12, facecolor="white", hatch="////", edgecolor=COLORS["liabilities"]))
    ax.text(.04, .84, "Principal  " + money(principal), color="white", fontsize=14, weight="bold", va="center")
    ax.text(.98, .72, "Asserted interest  " + money(interest), ha="right", color=COLORS["liabilities"], fontsize=12)
    ax.text(.02, .64, "Demand components = " + money(total), fontsize=17, color=INK, weight="bold")
    card(ax, .03, .32, .94, .23, "SEPTEMBER 27 MOTION — further relief requested",
         "From September 17, 2018: 15% per annum / $930.42 per day\nCent-rounded daily arithmetic reconciles; actual default is unresolved.", "scenarios")
    card(ax, .03, .04, .94, .21, "UNQUANTIFIED AND UNRESOLVED",
         "Fees / collection costs: unknown amount\nNo transaction ledger, award or current account balance established.", "unknown", dashed=True)
    ids = ["norm-b1-25-26", "norm-b1-25-26-01", "norm-b1-25-26-02", "norm-b1-25-26-03", "calc-opeh-demand-addition", "calc-opeh-per-diem", "finding-opeh-component-checks"]
    table = [s.row(i, s.get(i).get("concept", s.get(i).get("purpose", i))) for i in ids]
    table.append(s.row("b1-25-26", "Fees and costs", date_basis="Motion filed 2018-09-27", conditions="Requested but unquantified; unknown is not zero", amount=None))
    return fig, dict(id="opeh-creditor-request", title=title, summary=summary, limitation=limitation,
                     section_anchor="source-amounts-and-component-arithmetic", appendix=False, kind="requested_components", table=table, source_record_ids=ids+["b1-25-26"])


def rounding(s):
    title = "Day inclusion and rounding change the comparison"
    summary = ("On unchanged $2,233,007 principal at 10% actual/360, 249 elapsed days gives $154,449.65; 250 date labels gives $155,069.93. "
               "The accepted optional whole-dollar or daily-cent conventions on 250 days can reproduce the creditor’s $155,070 assertion.")
    limitation = ("Every branch is conditional: January 11 accrual start, no payments/fees and no completed annual capitalization boundary are assumed. "
                  "The note selects neither endpoint inclusion nor interim rounding. Numerical agreement does not establish the claimant’s method or an overcharge; its worksheet is absent.")
    fig, ax = canvas(title, "January 11 to September 17, 2018; all values are accepted scenario outputs, not amounts found due.", 8.3)
    cols = ["Day basis", "Rounding boundary", "Interest", "Comparison to assertion"]
    specs = [
        ("calc-opeh-regular-249", "249 elapsed", "Final cents", "Claim higher by $620.35"),
        ("calc-opeh-regular-250", "250 labels; both endpoints", "Final cents", "Claim higher by $0.07"),
        ("calc-opeh-regular-250-whole-dollar", "250 labels; both endpoints", "Final whole dollars", "Reproduces $155,070"),
        ("calc-opeh-regular-250-daily-cent", "250 labels; both endpoints", "Daily cents, then × days", "Reproduces $155,070"),
        ("calc-opeh-regular-249-daily-cent", "249 elapsed", "Daily cents, then × days", "Does not reproduce claim"),
    ]
    rows = [[days, boundary, money(s.value(i)), comparison] for i, days, boundary, comparison in specs]
    t = ax.table(cellText=[[wrap(v, 21) for v in row] for row in rows], colLabels=[wrap(c, 22) for c in cols],
                 colWidths=[.26, .25, .19, .30], cellLoc="left", loc="upper center", bbox=[0, .31, 1, .66])
    t.auto_set_font_size(False); t.set_fontsize(11)
    for (r, c), cell in t.get_celld().items():
        cell.set_edgecolor("#CBD5E1"); cell.PAD=.08
        cell.set_facecolor("#F1ECF8" if r in [3,4] else ("#EEF2F6" if r==0 else "white"))
        if r==0: cell.set_text_props(weight="bold", color=INK)
        if r in [1,2] and c==3:
            cell.set_edgecolor(COLORS["attention"]); cell.set_linewidth(2)
            cell.set_text_props(color=COLORS["attention"],weight="bold")
    card(ax, .02, .015, .96, .23, "BOUNDARY AND DIAGNOSTIC LIMITS",
         "Implied-day diagnostic: " + str(s.value("calc-opeh-implied-days")) + " days (algebra only).\n"
         "If the base includes September 17, additional interest from that date\nneeds a nonoverlapping boundary explanation; the worksheet is absent.", "unknown", 12)
    ids = [r[0] for r in specs] + ["calc-opeh-claim-gap-249", "calc-opeh-claim-gap-250", "calc-opeh-implied-days", "calc-opeh-regular-daily", "finding-opeh-interest-boundaries"]
    table = [s.row(i, s.get(i).get("purpose", i)) for i in ids]
    return fig, dict(id="opeh-rounding-day-count", title=title, summary=summary, limitation=limitation,
                     section_anchor="interest-boundaries-and-rounding", appendix=False, kind="rounding_matrix", table=table, source_record_ids=ids)


def calendar(s):
    title = "Three conditional calendar branches through filing"
    summary = ("All branches end September 27, 2018. The creditor’s asserted September 17 switch gives independently recomputed interest $163,753.85 "
               "(249 regular / 10 default days); weekdays only gives September 3 due, September 17 cure end, September 18 switch and $163,443.71 (250/9); "
               "additionally excluding September 3 gives September 4 due, September 18 cure end, September 19 switch and $163,133.57 (251/8).")
    limitation = ("These are not determinations of default or verified New York legal calendars. Assumptions: no earlier transfer; unchanged principal/no payments or fees; "
                  "January 11 accrual start; due day excluded from cure, full tenth Business Day allowed, switch next calendar day; no capitalization at maturity/switch and no anniversary before filing. "
                  "Complete holiday/bank-closure inputs and controlling notice/waiver/election construction are missing. The 15% rate replaces 10%, with the shared boundary counted once.")
    fig, ax = canvas(title, "September 2018 sensitivity; aligned dates show possible timing, without establishing default.", 10.8)
    specs = [
        ("17", "A · CREDITOR’S ASSERTED SWITCH", "Due / cure end: undetermined", "Switch September 17", "Independent recomputation; 249 regular + 10 default days"),
        ("18", "B · WEEKDAYS ONLY", "Due September 3 → cure ends September 17", "Switch September 18", "250 regular + 9 default days; holiday exclusions unverified"),
        ("19", "C · ADDITIONALLY EXCLUDE SEPTEMBER 3", "Due September 4 → cure ends September 18", "Switch September 19", "251 regular + 8 default days; September 3 exclusion assumed"),
    ]
    table=[]; ids=["finding-opeh-calendar", "calc-opeh-rate-switch-day"]
    xpos=lambda day:.075+.85*(day-1)/26
    for day in [1,5,10,15,20,25,27]:
        x=xpos(day)
        ax.plot([x,x],[.30,.93],color="#E2E8F0",lw=.8,zorder=0)
        ax.text(x,.95,str(day),ha="center",fontsize=11,color=INK)
    ax.text(.025,.987,"SEP",fontsize=11,color=INK,weight="bold")
    for n, (day, heading, due, switch, basis) in enumerate(specs):
        y=.81-n*.22
        interest_id=f"calc-opeh-switch-{day}-interest"; total_id=f"calc-opeh-switch-{day}-total"
        switch_day=int(day)
        ax.text(.025,y+.09,heading,fontsize=12,weight="bold",color=COLORS["scenarios"])
        ax.text(.975,y+.055,"Interest "+money(s.value(interest_id)),fontsize=12,weight="bold",ha="right",color=INK)
        # The chart covers September only; the accepted regular-day totals also
        # include the January-to-August interval, stated beneath each lane.
        ax.plot([xpos(1),xpos(switch_day)],[y,y],color=COLORS["scenarios"],lw=4,zorder=2)
        ax.plot([xpos(switch_day),xpos(27)],[y,y],color=COLORS["attention"],lw=5,zorder=2)
        ax.plot(xpos(switch_day),y,marker="^",markersize=11,color=COLORS["attention"],zorder=4)
        ax.plot(xpos(27),y,marker="o",markersize=8,mfc="white",mec=INK,mew=1.5,zorder=4)
        ax.text(xpos(switch_day),y-.031,"Switch "+day,fontsize=11,color=COLORS["attention"],ha="center",va="top")
        ax.text(xpos(27),y-.031,"File 27",fontsize=11,color=INK,ha="center",va="top")
        if n:
            due_day=3 if n==1 else 4; cure_day=17 if n==1 else 18
            ax.plot(xpos(due_day),y,marker="s",markersize=9,color=COLORS["liabilities"],zorder=5)
            ax.plot(xpos(cure_day),y,marker="D",markersize=9,mfc="white",mec=COLORS["scenarios"],mew=2,zorder=5)
            ax.text(xpos(due_day),y+.022,"Due "+str(due_day),fontsize=11,color=COLORS["liabilities"],ha="center",va="bottom")
            ax.text(xpos(cure_day)-.01,y+.022,"Cure end "+str(cure_day),fontsize=11,color=COLORS["scenarios"],ha="right",va="bottom")
        else:
            ax.text(xpos(2),y+.025,"Due / cure end unknown",fontsize=11,color=COLORS["unknown"],va="bottom")
        ax.text(.025,y-.083,basis,fontsize=11,color="#475569")
        ids += [interest_id,total_id]
        table += [s.row(i, heading, conditions=s.get(i)["assumptions"], due_and_cure=due, switch_date="2018-09-"+day) for i in [interest_id,total_id]]
    ax.text(.025,.255,"■ Due   ◇ Cure end   ▲ 15% switch   ○ Filing endpoint   — 10% before switch",fontsize=11,color=INK)
    ax.text(.025,.218,"One day later at 15% lowers hypothetical interest by $310.14.",fontsize=12,color=COLORS["attention"],weight="bold")
    card(ax, .025, .015, .95, .165, "COMMON ASSUMPTIONS — all three branches",
         "No earlier transfer / payments / fees; January 11 start; no capitalization.\nExclude due day; full tenth Business Day; switch the following day.\n15% replaces 10%; shared boundary once; holidays/closures unverified.\nControlling notice/waiver/election construction remains unresolved.", "unknown", 11)
    # Include the accepted endpoint and claimant-component sensitivities as data,
    # without making an extra calendar branch or a new financial calculation.
    for i in ["calc-opeh-regular-scheduled", "calc-opeh-regular-weekday", "calc-opeh-regular-holiday", "calc-opeh-claim-filing-interest", "calc-opeh-claim-filing-total", "calc-opeh-rate-switch-day"]:
        ids.append(i); table.append(s.row(i, s.get(i)["purpose"]))
    return fig, dict(id="opeh-calendar-branches", title=title, summary=summary, limitation=limitation,
                     section_anchor="calendar-and-rate-switch-scenarios", appendix=False, kind="conditional_calendar", table=table, source_record_ids=sorted(set(ids)))


def triggers(s):
    title = "Contract triggers and the missing notice evidence"
    summary = ("The contract separates scheduled/earlier-transfer maturity, payment cure of ten Business Days, other-covenant cure after written notice, "
               "acceleration by delivered written election, and 15% interest while an Event of Default continues after cure. Section 8 governs notice methods.")
    limitation = ("Demand dated September 25 is marked Via Federal Express and delivery is alleged, but independent receipt/tracking is absent. "
                  "Express notice/election clauses coexist with sections 5/16 waivers, including an assignment-notice exception. No controlling construction or enforceability conclusion is selected; notice-dependent timing remains not testable with a null result.")
    fig, ax = canvas(title, "Clause map; separate cards preserve separate conditions and do not establish that any trigger occurred.", 10.4)
    cards = [
        ("MATURITY — scheduled or earlier transfer", "September 1, 2018; earlier property sale/transfer unknown.\nNon-Business Day payment shifts to the subsequent Business Day.", "liabilities"),
        ("PAYMENT DEFAULT — applicable cure", "Ten Business Days to cure payment default.\nOperative due date and applicable holiday/closure calendar unresolved.", "scenarios"),
        ("OTHER COVENANT DEFAULT — written notice", "Ten Business Days after written notice.\nDistinct from the payment-cure provision.", "scenarios"),
        ("ACCELERATION — delivered written election", "Express delivery/election term; section 8 written methods.\nDemand legend / delivery assertion lacks independent receipt or tracking.", "unknown"),
        ("DEFAULT INTEREST — separate condition", "15% actual/360, compounded annually, while default continues\nafter applicable cure; does not itself resolve notice or waiver interaction.", "scenarios"),
    ]
    for n,(heading,body,color) in enumerate(cards):
        card(ax,.025,.80-n*.17,.95,.145,heading,body,color,12)
    ax.text(.035,.045, "Unresolved: sections 5/16 waivers ↔ express sections 7/8 notice/election terms.\nNotice-dependent calculation: NOT TESTABLE; result remains null.", color=COLORS["unknown"], fontsize=12, weight="bold", va="top")
    ids=["finding-opeh-terms", "finding-opeh-notice", "calc-opeh-notice-effective", "event-opeh-demand-20180925"]
    table=[s.row(i,s.get(i).get("purpose",i)) for i in ids]
    return fig, dict(id="opeh-contract-notice-gaps", title=title, summary=summary, limitation=limitation,
                     section_anchor="contract-terms-and-notice-limitations", appendix=True, kind="contract_conditions", table=table, source_record_ids=ids)


def coverage(s):
    title = "Source occurrence and calculation-status counts"
    summary = ("The OPEH lane has 21 source occurrences representing 20 unique documents. The note appears under two filenames. "
               "Among 25 accepted calculations, two component checks reconcile, 21 are conditional and two are not testable.")
    limitation = ("Counts describe provenance and calculation status, not independent corroboration, confidence, probability or separate debts. "
                  "Not-testable notice timing and later-balance results remain null. No present-day accrual is inferred; monetary scenarios stop September 27, 2018.")
    docs=[d for d in s.index["documents"] if d["dossier_id"]=="opeh"]
    occurrences=[o for o in s.index["occurrences"] if o["dossier_id"]=="opeh"]
    calcs=[r for r in s.index["records"] if r["dossier_id"]=="opeh" and r["collection"]=="calculations"]
    counts=Counter(r["evaluation"]["status"] for r in calcs)
    assert len(docs)==20 and len(occurrences)==21 and counts=={"reconciled":2,"conditional":21,"not_testable":2}
    fig,ax=canvas(title,"Raw counts only — neither probabilities nor ratings of allegations.",8.2)
    rows=[("Source occurrences",len(occurrences),"assets","//"), ("Unique documents",len(docs),"assets",""),
          ("Reconciled component checks",counts["reconciled"],"equity",".."),
          ("Conditional calculations",counts["conditional"],"scenarios","//"),
          ("Not-testable calculations",counts["not_testable"],"unknown","xx")]
    for n,(label,value,color,hatch) in enumerate(rows):
        y=.88-n*.145
        ax.text(.01,y+.055,label,fontsize=12,color=INK)
        ax.add_patch(Rectangle((.01,y-.005),.83*value/25,.045,edgecolor=COLORS[color],facecolor="white",hatch=hatch,lw=1.7))
        ax.text(.86,y+.017,str(value),fontsize=15,color=COLORS[color],weight="bold",va="center")
    ax.text(.01,.08,"25 accepted calculations = 2 reconciled + 21 conditional + 2 not testable.\nDuplicate filenames and repeated material do not add independent debts.",fontsize=12,color=INK,linespacing=1.5)
    ids=[r["id"] for r in calcs]+["document-"+d["id"] for d in docs]
    table=[dict(label="Source occurrences",value=str(len(occurrences)),source_record_ids=["document-"+d["id"] for d in docs],
                occurrence_ids=[o["occurrence_id"] for o in occurrences],date_basis="supplied packet",conditions="Provenance count; not corroboration"),
           dict(label="Unique documents",value=str(len(docs)),source_record_ids=["document-"+d["id"] for d in docs],date_basis="supplied packet",conditions="Document identity count; note duplicate retained as occurrence")]
    table += [s.row(r["id"],r["purpose"]) for r in calcs]
    return fig,dict(id="opeh-coverage-status",title=title,summary=summary,limitation=limitation,
                    section_anchor="source-basis-and-reading-boundaries",appendix=True,kind="count_panels",table=table,source_record_ids=ids)


def validate_numeric_sources(s):
    """Fail on changed accepted operands/results rather than silently inventing data."""
    expected={"norm-b1-34-35":"2233007", "norm-b1-25-26":"2233007", "norm-b1-25-26-01":"155070",
              "norm-b1-25-26-02":"0.15", "norm-b1-25-26-03":"930.42", "calc-opeh-demand-addition":"2388077.00",
              "calc-opeh-per-diem":"930.42", "calc-opeh-claim-gap-249":"620.35", "calc-opeh-claim-gap-250":"0.07",
              "calc-opeh-regular-249":"154449.65", "calc-opeh-regular-250":"155069.93",
              "calc-opeh-regular-250-whole-dollar":"155070", "calc-opeh-regular-250-daily-cent":"155070.00",
              "calc-opeh-regular-249-daily-cent":"154449.72", "calc-opeh-implied-days":"250.000112",
              "calc-opeh-switch-17-interest":"163753.85", "calc-opeh-switch-18-interest":"163443.71", "calc-opeh-switch-19-interest":"163133.57",
              "calc-opeh-switch-17-total":"2396760.85", "calc-opeh-switch-18-total":"2396450.71", "calc-opeh-switch-19-total":"2396140.57"}
    for i,value in expected.items():
        assert s.value(i)==value,(i,s.value(i),value)
    assert Decimal(s.value("norm-b1-25-26"))+Decimal(s.value("norm-b1-25-26-01"))==Decimal(s.value("calc-opeh-demand-addition"))
    for i in ["calc-opeh-notice-effective", "calc-opeh-later-balance"]:
        assert s.value(i) is None and s.get(i)["evaluation"]["status"]=="not_testable"


def build(index: dict, output: Path) -> list[dict]:
    s=Sources(index); validate_numeric_sources(s)
    output=Path(output); folder=output/"figures"/"opeh"; folder.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for builder in [obligation,chronology,request,rounding,calendar,triggers,coverage]:
        fig,entry=builder(s)
        entry.update(lane="opeh",legend=COLORS.copy(),alt=entry["summary"]+" "+entry["limitation"])
        entry["source_record_ids"]=sorted(set(entry["source_record_ids"]))
        closure=s.closure(entry["source_record_ids"])
        stem=entry["id"]
        for extension in ["svg","png","json","csv"]:
            entry[extension]=f"figures/opeh/{stem}.{extension}"
        fig.savefig(output/entry["svg"],metadata={"Date":None,"Creator":"OPEH supplied-file visual generator"})
        fig.savefig(output/entry["png"],dpi=160,metadata={"Software":"OPEH supplied-file visual generator"})
        plt.close(fig)
        tree=ET.parse(output/entry["svg"])
        assert tree.findall(".//{http://www.w3.org/2000/svg}text"),"SVG must preserve text"
        for node in tree.iter():
            assert node.tag.split("}")[-1] not in {"script","foreignObject"}
            for attribute,value in node.attrib.items():
                assert not attribute.lower().startswith("on")
                if attribute.endswith("href"):
                    assert value.startswith("#"),"No external SVG resources"
        data=dict(figure_id=stem,lane="opeh",summary=entry["summary"],limitation=entry["limitation"],
                  table=entry["table"],source_record_ids=entry["source_record_ids"],
                  dependency_record_ids=closure,
                  accepted_records=[s.get(i) for i in entry["source_record_ids"]])
        (output/entry["json"]).write_text(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
        columns=list(dict.fromkeys(k for row in entry["table"] for k in row))
        with (output/entry["csv"]).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=columns); writer.writeheader()
            for row in entry["table"]:
                writer.writerow({k:json.dumps(v,ensure_ascii=False,sort_keys=True) if isinstance(v,(dict,list)) else v for k,v in row.items()})
        manifest.append(entry)
    (folder/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
    return manifest


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index",type=Path,required=True); parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=build(json.loads(args.index.read_text()),args.output)
    print(json.dumps({"lane":"opeh","figures":len(result),"ids":[e["id"] for e in result]},indent=2))
