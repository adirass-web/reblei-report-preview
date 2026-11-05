from pathlib import Path
p=Path('continuation-2/litigation/work/finra_native.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace("queries=['Michael Bleich','Michael Edward Bleich','Scout Trading','Ophir Partners','EntryPoint Capital','EP Third Moment','Inferent Capital']", "queries=['Bleich','\"Michael Bleich\"','\"Michael Edward Bleich\"','\"Scout Trading\"','\"Ophir Partners\"','\"EntryPoint Capital\"','\"EP Third Moment\"','\"Inferent Capital\"']")
s=s.replace("'LIT3-AAO-'+str(n)","'LIT3-AAO-PHRASE-'+str(n)")
s=s.replace("'displayed_rows','award_links']}))", "'empty_messages']}))")
s=s.replace(";logs=[]", ";logs=json.loads((root/'search-log.json').read_text(encoding='utf-8'))")
p2=p.with_name('finra_phrases.py');p2.write_text(s,encoding='utf-8')
