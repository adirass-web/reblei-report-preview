# Early employment, second continuation

Research date: November 4, 2026. Scope: professional facts about Michael Edward Bleich, CRD 4262671. Keith Michael Bleich, CRD 2372764, and unrelated namesakes were excluded. Legacy repository root PDFs/ZIPs were not read.

## Result

**No additional official record establishing exact Chase, Lehman or Barclays employment dates was retrieved in this pass.** The new evidence resolves part of the access question: the public FINRA and IAPD individual search services both completed requests successfully and returned zero hits for CRD 4262671. They did not return the individual's historical record.

This completed public search is distinct from the previously recorded individual-PDF HTTP 403 failures. It does not validate the proposed employment dates, disprove a historical registration, or establish an individual's disclosure history.

## Newly preserved official material

- **EMP3-FINRA-APP:** current public BrokerCheck application JavaScript exposes the public FINRA and IAPD search base URLs and its individual lookup query. The original script is preserved for endpoint provenance, not employment evidence.
- **EMP3-FINRA-API / EMP3-FINRA-CLIENT-API:** both the bare individual route and the exact query used by the public client returned HTTP 200, `{"hits":{"total":0,"hits":[]}}`.
- **EMP3-IAPD-CLIENT-API:** the corresponding IAPD public individual lookup returned the same HTTP 200 zero-hit response. No authentication or nonpublic API was used.
- **EMP3-FINRA-ABOUT:** FINRA's original methodology page distinguishes registration history from employment history reported on the last Form U4. It states that reports include the latter for the last 10 years. The page also describes continued public inclusion for ten years after termination and specified conditions for inclusion afterward. The downloaded original HTML and labeled derived text are preserved.

Exact request URLs, response bytes, UTC timestamps, SHA-256 hashes and locators appear in `sources.json`. These are search and methodology records; none is a newly obtained subject employment history.

## Inference and alternatives

FINRA's public retention policy makes public-display scope a **possible explanation** of a missing individual result. This is an unresolved explanation, not a finding that the policy actually removed this subject. The September 2014 date in the earlier AdvisorCheck lead remains third-party information and is not an official premise for asserting when the subject's registration ended. A firm's termination date likewise cannot establish the individual's departure date.

Other possibilities include public indexing/coverage issues and historical report availability under another URL. The zero-hit response cannot establish the absence of adverse events or any other information in the underlying historical CRD record. No employment start or end date is inferred from it.

## Other new routes and limits

A public Wayback CDX request for the exact current FINRA individual PDF URL completed with HTTP 200 and `[]`. It was restricted to successful PDF captures and collapsed duplicate digests. It says nothing about other URL forms, unindexed captures or holdings elsewhere.

A direct request for the SEC Form ADV historical-data catalog returned HTTP 403. The search service returned an indexed description of Part 1/ADV-W firm data. That description is a route lead, not a retrieved historic individual Form U4. No archive was treated as absent because of the 403. The separate Inferent workstream owns adviser brochure archive mapping to avoid duplicated retrievals.

Targeted Parallel Search batches covered official-name/CRD results, adviser brochure supplements, Chase/Lehman date variants, professional court employment exhibits, and regulator API/data catalogs. Results mostly repeated known corporate/third-party leads or returned documents about other people. No new candidate with explicit subject employment dates survived review. No assertion is made that a comprehensive court or regulator search was completed. Personal litigation, contact aggregators and unrelated-industry hits were not adopted or preserved as subject evidence.

## Next precise record needed

The useful missing record is an original historical **Form U4 employment-history section or CRD registration-history extract for CRD 4262671**, particularly the 2000 initial Lehman filing or the 2008 transfer to Barclays. A 2008 employment-history disclosure could cover the proposed 1998-2000 Chase period; its contents must be obtained and read before making that claim. The registration-history section and any Form U5 could separately establish regulatory registration/termination dates. Neither automatically establishes employment dates.

An authenticated employer employment agreement or dated employment certificate naming the full subject is another appropriate source. The existing LBHI RSU-counterparty schedule supplies neither those dates nor a CRD and remains bounded as in the earlier report.

No accounts, purchases, outreach or nonpublic API access were attempted. `claims.json` separates verified search observations, verified methodology and unresolved inference. `search-log.json` preserves search IDs, selected professional URLs, successful requests and failures. No employment claim was upgraded in this pass.
