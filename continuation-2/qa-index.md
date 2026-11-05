# Final normalized-index QA, continuation 2

Reviewed November4,2026. Target: schema2 index generated2026-11-04T18:02:41.244857+00:00. This is a bounded normalization/integrity review; original-source factual QA is documented separately. Only this note was written. No index, database, source, manifest or shared data file was edited.

**Result: passed; no blocking normalization issue found.**

## Integrity and agreement

- Parsed evidence-index.json and all nested metadata_json values successfully.
- Compared every JSON table row with the corresponding SQLite row across all17 tables. Counts and values agree semantically. SQLite REAL ownership columns render integer-valued numbers as floats; this is equivalent numeric storage, not a factual difference.
- SQLite PRAGMA integrity_check returned ok; PRAGMA foreign_key_check returned no rows. Document aliases, claims, evidence links, entity/role/event links and conflict links therefore resolve through the normalized schema.
- Independently recomputed SHA256 for all200 indexed document files against their normalized recorded hashes. All matched.
- Confirmed counts:200 documents,182 claims,213 document aliases,55 financial observations,6 events,243 claim-evidence links,26 event-claim links,38 subjects,33 entities,6 roles and27 relationships. These agree with validation.json.

Exact reviewed output digests:

- evidence-index.json: 0c5ed9b585636223ca6732255ee614bade55cf3be06a678c3c1f0bd612480e5d
- evidence-index.sqlite: 74a8255c204b2ec5a0c9db0ea4498b597af71d04837a9a095d0019ef6a793671

## Events and monetary normalization

Five existing regulatory firm events remain EVT-E001 through EVT-E005. One additional event, LIT3-E001, is explicitly a firm arbitration award with inferred Scout identity mapping. Its claimant is E001 Scout and respondent is E020 Wedbush; fine_amount is NULL. The event text and LIT3-C10 retain probable identity inference from multiple official records, lack of a Scout CRD in the award, no Bleich party/personal sanction, and the remaining name-collision possibility.

The award is not normalized as another regulatory fine or personal penalty. Financial observations separate:

- LIT3-F001: USD237594 compensatory damages awarded to Scout, collection unverified.
- LIT3-F002: USD1250 filing-fee reimbursement ordered to Scout, payment unverified.
- LIT3-F003: USD9550 hearing-session fees assessed to Wedbush payable to FINRA, not Scout income or a regulatory fine.

LIT3-E001 resolution_date2016-11-18 is explicitly identified as the FINRA index/service date. Its note and linked LIT3-C07 separately retain November16 arbitrator signatures and leave the legal interest-transition date unresolved. No calculated interest total or presumed payment date is added. The normalized initiated_date is anchored to LIT3-C03's source-qualified on-or-aboutOctober22,2015 statement. The event note now also explicitly preserves Claim filed on or about2015-10-22; the underlying approximation is retained.

The new Wedbush AWC claims LIT3-C11/C12 enrich existing EVT-E005 (case20100243866-02; Nasdaq acceptance2016-02-25). They do not create another event or duplicate the USD675000 joint FINRA/Nasdaq fine. The note preserves that USD337500 to Nasdaq is included in the joint amount, not additive, and that sanctions effectiveness/completion/payment remain unverified. Regulatory firm outcomes do not become Bleich personal sanctions.

## Inferent and rejected identity boundaries

INF3-F001 and INF3-F002 are attached to E021 Inferent Capital, which remains a candidate subject affiliation. Their financial status explicitly says verified as-filed firm fact in a conditional branch; neither amount is attributed to Bleich. Both exact measurement_date fields are NULL. The record explains that filing dates2018-07-05 and2018-08-31 come from the official mapping and are not asset-measurement dates. Client AUM and regulatory AUM are retained as different metrics.

No Inferent role was added to the6-role table and no P001-to-Inferent branch relationship was added. The33-entity table does not create an Inferent QE Client LP entity from the August2018 wording. INF3-C008 preserves Client/Master source-wording ambiguity with no established typo, rename, succession, separate entity or identity equivalence. Existing Inferent branch entities remain conditional; no Ophir merger or Bleich affiliation is upgraded.

CIK1977777 does not appear as an assigned identifier. CORP2-CIK-REJECTION and conflict CONT-X-CIK1977777 continue to reject its attribution to EP Fund GP because the official SEC record identifies Cata Labs Inc. The rejected lead remains auditable without becoming an entity identifier.

This QA validates the specified normalized snapshot and explicit evidentiary boundaries. It does not establish complete career history, comprehensive court clearance, payment/satisfaction of an award or sanction, or a new corporate-owner identity join.

