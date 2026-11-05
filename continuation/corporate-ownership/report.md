# Corporate ownership continuation â€” official records and candidate resolution

As of November 4, 2026. This continuation consulted only independently collected evidence in this investigation and new official sources. No legacy repository PDFs, ZIPs or prior dossier material were read. No accounts, purchases or outreach were used. The shared browser was unavailable; a separate temporary Chrome session opened public registry records and preserved original HTML response bytes. No CAPTCHA was bypassed.

## Results

Delaware's free public registry now supplies five actual entity-detail records, including two distinct companies with the name Finch LLC. These provide formation dates and file numbers; they do **not** identify shareholders, establish current good standing or prove that each candidate is the company in a regulatory ownership disclosure.

| Official registry name | Delaware file | Formation date | Record / identity treatment |
|---|---|---|---|
| ENTRYPOINT GP LLC |3458887|2020-08-17|Exact-name corporate candidate for the regulatory GP; ownership-ID join remains provisional.|
| ENTRYPOINT PARTNERS, LP |3458856|2020-08-17|Strong corporate candidate; exact name, jurisdiction, kind and formation date correlate with NY DOS6795220. Bleich ownership remains supported by regulatory filings rather than a corporate shareholder/partnership record.|
| FINCH LLC |5142327|2012-04-19|Historically compatible candidate for the entity in Ophir and Scout disclosures. Corporate owner linkage still unproven.|
| FINCH LLC |10521968|2026-02-24|Separate same-name record. Do not merge it with 2012 relationships absent succession/conversion evidence.|
| NAYS, LLC |4688408|2009-05-15|Chronologically compatible exact-name candidate; owner linkage remains regulatory rather than corporate proof.|

All five detail pages state that the display is **not a statement of good standing**. They identify registered agents only, which are service providers rather than evidence of ownership. EntryPoint GP and Partners name Harvard Business Services; historical Finch and NAYS name The Corporation Trust Company; the 2026 Finch names Corporation Service Company. Shared agents do not establish affiliation. Free search also includes inactive entities, so appearance in search does not establish active status.

The registry URL is [Delaware public entity search](https://icis.corp.delaware.gov/Ecorp/EntitySearch/NameSearch.aspx). Records were reached through its ordinary search and entity-detail controls; the same URL is reused by the portal for multiple states of the page. `sources.json` therefore preserves query context, HTTP method, response identifiers, exact bytes, timestamps, hashes and field locators, rather than presenting that generic URL as a unique permalink.

## Ownership relationships actually documented

These are as-filed regulatory representations, distinct from corporate registry proof. Physical PDF pages below are 1-based.

| Relationship | Disclosed band | Acquisition/status date | Original evidence |
|---|---|---|---|
| Finch â†’ Scout Trading |75% or more|08/2012|Scout BrokerCheck physical p6|
| MEB NY â†’ Finch, in Scout report |50% to less than75%|08/2012|Scout physical p8|
| NAYS â†’ Finch, in Scout report |25% to less than50%|08/2012|Scout physical pp8â€“9|
| Bleich CRD4262671 â†’ MEB NY |75% or more|05/2009|Scout physical p8; Ophir ADV p20|
| Dror Niv â†’ NAYS |25% to less than50%|05/2009|Scout physical p9|
| Finch â†’ Ophir Partners |75% or more|04/2012|Ophir March30,2017 ADV physical p19|
| MEB NY â†’ Finch, in Ophir report |75% or more|04/2012|Ophir physical p20|
| EntryPoint Partners â†’ EntryPoint Capital |75% or more|10/2020|EntryPoint October15,2026 ADV physical p26|
| Bleich â†’ EntryPoint GP |25% to less than50%|07/2023|EntryPoint physical p27|
| Bleich â†’ EntryPoint Partners |25% to less than50%|07/2023|EntryPoint physical p27|
| Richard A.Desich Irrevocable2005 SD Trust â†’ EntryPoint GP |25% to less than50%|11/2024|EntryPoint physical p27|
| South Dakota Trust Company â†’ named ownership trust |Trustee, codeF|12/2020|EntryPoint physical p27|

The last two rows preserve the disclosed professional trust intermediary chain without conclusions about family relationships or ultimate beneficiaries. These disclosures do not provide complete cap tables. For example, the Niv row does not establish 100% NAYS ownership. The bands cannot establish an exact effective economic interest in a downstream adviser, or a fee-income amount.

EntryPoint GP LLC and EP Fund GP LLC remain distinct. ScheduleA lists EntryPoint GP with status GENERAL PARTNER; the separate EP Fund GP entity appears in fund management/GP disclosures. Those labels are retained as filed without rewriting legal roles.

### Unresolved band variation

The preserved **Ophir ADV filed March30,2017** reports MEB NY owning at least75% of Finch, with status acquisition04/2012. Scout's retrieved firm report reports50% to less than75%, with relationship established08/2012. This is a real disclosure variation, not proof of a dated ownership change. The acquisition months are not timestamps for every later ownership update. Differing snapshots, scope and stale historical reporting remain possible explanations; none is adopted without evidence.

An important notation limit: **DE in the FormADV ownership schedules means domestic entity**, not Delaware. A Delaware formation jurisdiction must come from a corporate record or other express statement, not that column.

## New York records: useful correlation, limited authority

The primary [New York public inquiry portal](https://apps.dos.ny.gov/publicInquiry/) reset connections in both direct retrieval and the independent browser attempt. No formal target-specific New York registry detail or certificate was obtained.

The official government open-data response supplied these bounded observations:

- **MEB NY Inc., DOS3772241:** certificate of incorporation filed February6,2009; certificate of change September25,2009. The name-history row retains MEB NY Inc. and the status-history rows say Active on those dates. This does not establish current legal status, the contents of the change, or Bleich's shareholder linkage to that DOS number.
- **EntryPoint Partners LP, DOS6795220:** reported Delaware formation August17,2020; authority filed April10,2023, approved April11; publication filed July25,2023, approved July26. Matching Delaware formation date, exact name and legal kind strengthen the cross-state candidate match to DE3458856. The state data do not name Bleich or prove ownership.
- **Ophir Partners Beaufort GP LLC, DOS4790401, and Ophir Partners Beaufort Fund LP, DOS4790408:** reported Delaware formation July14,2015, both NY authority filings July16,2015. These corporate candidates require a separate regulatory-to-registry identifier join. Third-party discovery assertions about Bleich were not treated as evidence.

The NY overview PDF already preserved in this investigation expressly says its dataset is not an official Department record, not certified-copy equivalent and not proof of current legal status (physical pp2â€“3). All findings retain that limitation. Entity-status/name-history rows can use approval dates where the all-filings dataset has separate filed/approved dates; exact fields are retained rather than collapsed. Duplicate name-history rows for Partners do not establish two entities.

The name-fragment query returned unrelated OPEH-containing names. Those rows remain only in the raw acquisition response for reproducibility and are excluded from subject entities and claims.

## Rejected identifier and remaining gaps

1. **Reject CIK1977777 for EP Fund GP LLC.** A third-party directory suggested this identifier. The independently retrieved [official SEC submissions JSON](https://data.sec.gov/submissions/CIK0001977777.json) instead identifies **Cata Labs Inc.** No Bleich/EntryPoint join is made. This is a concrete correction to a newly surfaced lead, not evidence that all similar secondary claims are false.
2. **EP Fund GP LLC corporate ID remains unresolved.** Exact quoted Delaware searches under its displayed name produced no matching rows in this bounded session. Its regulatory related-person/fund-GP role remains documented. No conclusion about nonexistence or jurisdiction follows.
3. **OPEH LLC remains unlinked.** The exact Delaware name search and focused official-source discovery did not establish a responsive company or an Ophir rename/ownership chain. No legacy ZIP or litigation material was consulted. Absence of a match is bounded search coverage, not proof the entity does not exist.
4. **Cayman legal form remains unresolved by corporate proof.** March2026 EntryPoint brochure physicalp4 calls EP Third Moment InternationalLP a Cayman exempted limited partnership. Its FormsD select Corporation. Both are preserved as conflicting as-filed statements; no original Cayman registry/formation record was obtained. The brochure is not independent registry adjudication of the discrepancy.
5. **Current legal status and ownership changes require further records.** Delaware free details explicitly withhold current status/history behind paid options. None was purchased. NY formal record access is still unavailable in this session. No current ownership conclusion is inferred from agents, names, dates or the absence of a filing.

## Evidence package and verification

- `sources.json`:49 source/reuse/attempt records, including original Delaware browser response bytes, government JSON responses, retrieval limits, reused official PDF metadata, hashes and claim links.
- `claims.json`:19 claims with source identifiers, locators, status and candidate qualification.
- `candidates.json`:five Delaware corporate detail candidates, kept separate from ownership assertions.
- `search-log.json`:Parallel Search queries and available search identifiers/URLs; third-party results are discovery leads only.
- `evidence/`:original acquisitions. Files ending `.dom.html` are separately generated browser DOM captures; original network response HTML is indexed under CORP2-BROWSER identifiers.

All files referenced by source records were checked against SHA256 on completion. New acquisitions have individual UTC retrieval timestamps. Reused originals retain their original timestamps in earlier investigation source indexes; this continuation deliberately does not invent new retrieval dates for them. Source count includes unsuccessful attempts and multiple page states, so it is not an entity or unique-document count.
