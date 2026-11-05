import pathlib
p=pathlib.Path('work/build_index.py');s=p.read_text(encoding='utf-8-sig');needle='# Explicit relational schema, with references enforcing ownership of evidence and identity.'
assert needle in s
hook="""# Integrate reviewed continuation records through the existing schema.
if (ROOT/'continuation'/'early-employment'/'claims.json').exists():
 import runpy
 runpy.run_path(str(ROOT/'work'/'build_continuation.py'),init_globals={'ROOT':ROOT,'data':data})
"""
assert 'runpy.run_path' not in s;s=s.replace(needle,hook+needle);p.write_text(s,encoding='utf-8')
