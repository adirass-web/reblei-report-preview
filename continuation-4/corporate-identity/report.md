# Corporate identity continuation 4: the 2009 change is coded as process-address information

Research date: November 4, 2026. **A new official-data field narrows the MEB question: New York's electronic filing index codes the September 25, 2009 Certificate of Change for DOS 3772241 as a service-of-process address change.** It does not supply a corporate-name change or Bleich's shareholder linkage to that DOS number. MEB INC and MEB NY INC therefore remain distinct as-filed labels pending a proper identity bridge.

## What can now be closed

Earlier queries retained selected filing columns but omitted amendment flags. This stage retrieved the full original All Filings response for DOS 3772241. The September 25, 2009 row, film **090925000007**, is a Certificate of Change with `mod_certcode=27DB A` and **`amd_procs_info_flag=X`**. The original dataset metadata defines that exact API field as a service-of-process address change. The original data dictionary confirms the definition on physical page 2, under Amd SOP Address Flag. The API entity-name-change flag, `amd_corp_name_flag`, is not present in that returned row; its separate definition is on dictionary physical page 1. [CORP5-C001]

This closes the narrower question of **how this electronic index classifies the 2009 change**. It does not reveal the old or new address, the signer or the complete filed instrument. The row's `law` field reads `402 BCL`; that source value is preserved without correcting it to a different statute or deriving legal conclusions from it.

The name-history response for the same DOS number contains one record: MEB NY INC., actual-name code A, active-name code A, linked to incorporation film **090206000693**, filed February 6, 2009. The name-history dictionary defines these name codes on its physical page 1. Active *name* is not treated as an independently certified current entity status. [CORP5-C002]

**Limited inference from multiple government records:** the retrieved filing flags and name-history row do not support using the September 2009 Certificate of Change as evidence that MEB INC was renamed MEB NY INC. The current DOS guidance also treats a domestic corporation's Certificate of Change as covering process-address/county/agent information, while providing a separate name-amendment route. The decisive target certificate itself remains unretrieved; the current guidance is not passed off as the law's exact historical wording in 2009. A shorthand or inconsistent SEC label, a different MEB entity, or another unlocated corporate event remains possible. None is selected. [CORP5-C003]

## What remains unresolved

The government-published open-data overview expressly says these datasets are not an official Department record, certified copy, or proof of current legal status; physical pages 2-3 preserve those limits. The new result is therefore an attributed electronic-index finding, rather than a formal certificate finding. [CORP5-C004]

The previously recovered SEC Schedule A/B records explicitly tie Bleich's full name and individual CRD 4262671 to the ownership rows, but spell the intermediate entity MEB INC in some fields and MEB NY INC in others. They do not supply New York DOS 3772241 in those entity rows. This stage supplies no missing shared corporate identifier. It does not merge the two spellings, convert a title/signature into share ownership, or treat the common initials as proof. [CORP5-C005]

A bounded query to the official Active Corporations dataset selected only entity identifiers, names and officer-name fields. The DOS 3772241 row supplied the entity name, formation date, jurisdiction and type, but no CEO or location-name field. That is missing returned information, not proof of no CEO, no beneficial owner or no biennial filing. No address search was needed. Exact-name queries to the name-history and active datasets supplied no additional target row for the tested Finch, NAYS and EP Fund GP spellings; those are query limits, not nonexistence findings. [CORP5-C006]

No new owner-linked registry identifier was obtained for Finch LLC, NAYS LLC or EP Fund GP LLC. The previously tracked Delaware candidates remain candidates; matching name, formation chronology, a registered provider or a mailing address does not turn them into owner-resolved entities. EP Fund GP and EntryPoint GP are not merged. Discovery returned public NASAA Form D views naming EP Fund GP as a general partner, but no corporate filing identifier; those views were not promoted into a new identity join. [CORP5-C007]

## Bounded bank-name branch

At the coordinating workstream's request, a limited search checked UNITED INTERNATIONAL BANK CORP, a new as-filed ownership-chain label. The official GLEIF legal-name filter returned one record, **United International Bank N.V.**, Curaçao registration **107214**, LEI **549300KNXGPJJTQC2Y92**. Its legal name/form differs from CORP, and the returned record supplies no link to United Master LLC or the EntryPoint ownership disclosures. It remains an unjoined candidate. Neither unrelated FDIC banks surfaced by search nor the historical Flushing bank is attached to this chain. A limited search's failure to find the exact corporate form does not prove that the disclosed entity does not exist or lacks a banking license. [CORP5-C008]

## Access and preservation

The original NY metadata, targeted JSON responses, four original data-dictionary/overview PDFs, current DOS guidance HTML and GLEIF JSON are preserved with URLs, UTC capture timestamps and SHA256 hashes. PDF text files are derived and separately labeled. The retained discovery log contains search identifiers, result URLs and titles; unrelated excerpts and addresses were omitted. Third-party pages remained leads or namesake exclusions.

The official DOS copy-service page says filed documents can be ordered online for entities formed or authorized on or after July 30, 1990, and identifies the exact-name/DOS-ID/document information needed. That is an identified access route, not a retrieved certificate or permission to place an order. No accounts, fees, outreach, NYSCEF activity, home/family research, private civil material, Git or shared-index modifications occurred. Specific next records and completion gates are in `remaining-instructions.md`.
