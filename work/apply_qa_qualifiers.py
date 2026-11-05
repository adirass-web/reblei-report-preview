from pathlib import Path
p=Path('work/build_index.py');s=p.read_text(encoding='utf8');s=s.replace("edge('E009','E008','GP_manager_or_director_as_listed','ID-C016')","edge('E009','E008','GP_manager_or_director_as_listed','ID-C016',note='Specifically Section7B1 privatefund805-5280422629; not attributed to other same-name ID805-9412438643.')")
s=s.replace("fin('E008','private_fund_gross_asset_value','24250059','dollars','ID-C019',None,'measurement date not established'","fin('E008','private_fund_gross_asset_value','24250059','dollars','ID-C019',None,'Specifically Section7B1 ID805-5280422629; no attribution to805-9412438643; measurement date not established'")
s=s.replace(",'financial_specialist_stage_raw':financial","")
s=s.replace("'independent_qa_scope':'specialist identity+SEC originals and brochures; final normalized index has structural/hash checks, not an independent content audit'","'independent_qa_scope':'specialist originals, brochures, 13F anomaly and bounded final normalized index second pass; see independent-qa.md, not every filing audited'")
p.write_text(s,encoding='utf8')
