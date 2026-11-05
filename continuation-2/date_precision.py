from pathlib import Path
p=Path('work/build_continuation.py');s=p.read_text(encoding='utf-8-sig').replace("note='Resolution field uses FINRAindex/service date;", "note='Claim filed on or about2015-10-22; resolution field uses FINRAindex/service date;");p.write_text(s,encoding='utf-8')
