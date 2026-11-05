import json,pathlib
b=pathlib.Path('outputs/ReBlei/investigations/2026-11-04-official-records/continuation-3/inferent')
a=json.loads((b/'part1bulk-directory.json').read_text());print(type(a));print(str(a)[:600])
