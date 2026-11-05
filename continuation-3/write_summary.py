
from pathlib import Path
import json
root=Path('.')
p=root/'work/build_continuation.py';s=p.read_text(encoding='utf-8')
s+="\nfor cid in ['LIT4-C01','LIT4-C02','LIT4-C04']:add2('event_claims',event_id='LIT3-E001',claim_id=cid)\n"
p.write_text(s,encoding='utf-8')
summary="""# Round 3 results: historical ownership and registration records

Research cutoff: November 4, 2026. This is a completed research stage with remaining gaps, not full-career or litigation clearance. The user's NYSCEF decision is implemented: no further attempt, CAPTCHA handling or human handoff.

## What the new originals establish

**Scout ownership transition.** Six original SEC annual-report PDFs now cover 2009-2013, including the 2009 amendment. The 2012 audited note says NAYS LLC and MEB NY Inc owned Scout directly until August 31, 2012, when Finch LLC became its sole owner. It says NAYS and MEB owned Finch, but gives no ownership percentages or registry IDs. The 2013 report corroborates Finch as sole parent. BrokerCheck's June 1 common-control date remains separate from the audited transition date. [Originals, accession register and page citations](ownership/report.md).

**Scout corporate financing and Bleich's filing capacities.** The 2013 report records a $5 million principal repayment plus unpaid interest to NAYS on October 8, 2013. Its separate $4 million remaining note has an unnamed lender. Neither is attributed to Bleich personally. The 2009 oath calls Bleich a member and the 2013 oath calls him managing member. These are filing capacities, not employment-start dates.

**Historical Ophir roles and ownership disclosures.** Original SEC historical tables provide dated filings and Schedule A/B records linked by FilingID, with Bleich's full name and CRD 4262671. CEO-only descriptions precede the combined CEO/CCO wording. The single acquired-status date must not be interpreted as the start of both roles. March-to-June 2016 ownership disclosures change MEB NY's Finch band and omit the prior NAYS row; those snapshots do not establish a transaction date, consideration or a complete exit. Earlier MEB INC wording remains distinct from later MEB NY INC pending legal identity evidence. [Employment and ownership snapshots](employment/report.md).

**Inferent's initial registration.** The original March 2018 brochure is now preserved. It describes an initial application and no current client assets, anticipating eligibility within 120 days of effective initial registration. Six historical Part 1 rows are linked to the original filing-type, succession and 120-day tables. Their Item 4A answers are N; that is limited to the retrieved filings and the form's question, not proof no transaction or personnel transfer occurred. The records do not establish Bleich's role or an Ophir merger. [Original brochure and historical rows](inferent/report.md).

**EntryPoint historical ambiguity.** The same CRD 313946 appears in a July 2021 row under ENTRYPOINT CAPITAL / SEC 801-122062 and a June 2024 row under ENTRYPOINT CAPITAL, LLC / SEC 801-130798. The 2021 filing-type row marks Initial SEC Registration Request=Y and leaves Final SEC ERA Report blank; the 2024 row marks BOTH fields Y. No explanation for the dual flags is assumed. This is verified continuity of the CRD field. Corporate legal continuity, the reason for the different names/file numbers and the earlier ERA history remain unresolved.

**Scout award follow-up.** FINRA's exact-case and full-text searches each show the already preserved award 15-02816. No later original confirmation, vacatur, appeal or payment record was obtained. CourtListener requests failed; selected GovInfo opinions do not replace complete dockets. No negative litigation or payment conclusion follows. [Follow-up and search coverage](award-followup/report.md).

## Remaining material gaps

- Official early-career employer and registration intervals for Chase, Lehman and Barclays.
- A direct official Inferent employment, officer or transaction record linking Bleich.
- MEB INC / MEB NY INC legal identity; owner-linked registry numbers and documents; exact transaction terms and dates.
- Cayman legal-form and GP records, and EntryPoint's earlier ERA/name/file-number history.
- Court follow-up to the Scout award and wider investment-management litigation coverage. NYSCEF remains excluded from further access attempts under the user's decision.
- Missing historical brochures and the five inaccessible prior Library documents.

These gaps require different records or access; repeatedly running blocked searches does not resolve them. No account, fee, purchase or external contact was used. Personal civil proceedings and legacy repository materials remain excluded.

## Preservation and review

The same ReBlei branch and investigation folder are retained. All new originals, exact compressed archive members, range metadata, SHA256/CRC verification, target-only derivative extracts, claim links and access logs are preserved. Large original CSVs are reproducibly retained as their exact compressed SEC archive members; expanded work caches are outside the evidence package. This avoids duplicate expanded copies without sacrificing original-byte reconstruction.

Three GPT-6.1 Sol specialists at medium effort handled bounded independent tasks and cross-review. Priority is the exposed tier; no measured savings claim is made. The parent integrates the normalized register and checks all indexed hashes and database references. Review files: [Scout originals](qa-scout.md), [Inferent archive and tables](qa-inferent.md), [Ophir historical tables](qa-employment.md), and [final index](qa-index.md). The scope and limitations in each review govern; no exhaustive court clearance is claimed.
"""
(root/'continuation-3/summary.md').write_text(summary,encoding='utf-8')
p=root/'README.md';s=p.read_text(encoding='utf-8').replace('[Latest round results](continuation-2/summary.md)','[Latest round results](continuation-3/summary.md)\n- [Round 2 results](continuation-2/summary.md)')
s=s.replace('and historicalInferentbrochures.','historical Inferent brochures, Scout audited annual reports, and historical SEC registration/ownership tables.')
p.write_text(s,encoding='utf-8')
p=root/'findings-and-gaps.md';s=p.read_text(encoding='utf-8').replace('[Latest round results](continuation-2/summary.md)','[Latest round results](continuation-3/summary.md)')
s=s.replace('Status acquired04/2012, in March30 2017 ADV','Single combined-row status acquired04/2012 in March30 2017 ADV; not proof CCO began then. Historical CEO-only rows precede combined CEO/CCO wording by March2015')
s=s.replace('## Financial observations','Round 3 now provides the dated Scout direct-to-Finch transition, historical Ophir Schedule A/B changes, and unresolved MEB INC / MEB NY INC wording. It also identifies two historical EntryPoint rows sharing CRD313946 with different SEC file numbers. These are source-specific snapshots, not assumed legal transactions or renames. See [round 3 results and original-record links](continuation-3/summary.md).\n\n## Financial observations')
s=s.replace('Uncompleted work: early-career official employment chain, historical ADV amendments and brochures,','Uncompleted work: early-career official employment chain, remaining historical ADV amendments and brochures beyond the newly recovered Part1 snapshots,')
p.write_text(s,encoding='utf-8')
queue="""# Remaining retrieval queue after round 3

Continue independent official public-record work. The investigation is not complete. Legacy repository materials and personal civil proceedings remain excluded.

| Priority | Missing record or clarification | What is established / next completion gate |
|---|---|---|
| 1 | Individual employment and registration history | FINRA/IAPD public APIs returned zero; firm originals establish identity and roles. Epiq's Lehman RSU schedule is not employment chronology. Seek an independently accessible official individual record or career biography. |
| 1 | MEB INC / MEB NY INC legal identity and corporate transitions | Historical Ophir tables show name and ownership-band differences. Obtain owner-linked filings or legal change records before treating them as one entity, a rename or a transaction. Registry-number matches remain provisional. |
| 1 | Inferent subject affiliation and any Ophir transaction | Initial March2018, July/August2018 brochures and six Part1 rows recovered. No affirmative Bleich role/merger evidence. Item4A N and missing succession rows do not prove no broader transaction. |
| 1 | EntryPoint earlier ERA and legal history | Same CRD313946 appears with801-122062 in2021 and801-130798 in2024. Initial-registration flag is Y in both; Final ERA is blank in2021 and Y in2024. Resolve dual flags and name/file-number changes using originals, without assuming succession. |
| 2 | Scout ownership chronology and financing counterparties | FY2012 note gives August31,2012 Finch transition; BrokerCheck common-control gives June1. FY2013 names NAYS for repayment but leaves remaining lender unnamed. Obtain original ownership/loan records if publicly available. |
| 2 | Investment-management litigation follow-up | FINRA15-02816 award preserved. Exact-case follow-up found the same award only; no later court/payment record established. NYSCEF access gap is accepted by user; no further attempt. No PACER account available. |
| 2 | Cayman legal form, GP and registry originals | EP international LP/Corporation discrepancy remains; certificate/registered-statement/GP-change records specified but not obtained. No paid order or new account authorized. |
| 2 | Missing Ophir247246, EntryPoint1061309 and Inferent2019 brochure originals | Ophir2015-17 selected archive requests403; no career biography recovered. Do not repeat identical blocked paths as new work. |
| 2 | Cboe order/resolution dates and EntryPoint13F discrepancies | Originals preserved. June26/July3,2013 Cboe dates,2024Q3 cover/table discrepancy and2024Q2 amendment treatment remain qualified. |
| 3 | Prior Library documents | Five named files inaccessible; user has no local copies. No claim of reconciliation. |

Clearly labeled official-record inference is authorized. No account creation, purchase, outreach or default-branch merge is authorized. Agents can work with accessible public court sources; they do not supply PACER credentials or bypass human checks. Failed access and bounded no-results never establish absence.
"""
(root/'next-stage-queue.md').write_text(queue,encoding='utf-8')
print('Current summary, boundaries and next records written.')

