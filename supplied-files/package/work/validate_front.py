"""Check generated links, safety, scope, and complete record catalogs."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
from bs4 import BeautifulSoup


def validate(output, index):
    output = Path(output).resolve()
    errors = []
    fragment_cache = {}
    for page in sorted(output.rglob('*.html')):
        soup = BeautifulSoup(page.read_text(encoding='utf-8'), 'html.parser')
        ids = [x['id'] for x in soup.select('[id]')]
        if len(ids) != len(set(ids)): errors.append(f'{page}: duplicate id')
        for el in soup.find_all(True):
            if any(a.lower().startswith('on') or a.lower() == 'style' for a in el.attrs): errors.append(f'{page}: unsafe attribute')
            if el.name == 'script' and (el.get('src') not in ('assets/report.js', '../assets/report.js') or el.string): errors.append(f'{page}: unsafe script')
            if el.name in ('iframe','object','embed','form','base'): errors.append(f'{page}: unsafe element {el.name}')
            for attr in ('href','src'):
                if not el.has_attr(attr): continue
                url = el[attr]; u = urlsplit(url)
                if u.scheme or u.netloc:
                    if el.name != 'a' or u.scheme not in ('https','http') or not u.netloc: errors.append(f'{page}: unsafe URL {url}')
                    continue
                dest = (page.parent / unquote(u.path)).resolve() if u.path else page
                try: dest.relative_to(output)
                except ValueError: errors.append(f'{page}: outside package {url}'); continue
                if not dest.is_file(): errors.append(f'{page}: missing {url}'); continue
                if u.fragment and dest.suffix == '.html':
                    if dest not in fragment_cache:
                        target = BeautifulSoup(dest.read_text(encoding='utf-8'), 'html.parser')
                        fragment_cache[dest] = {x['id'] for x in target.select('[id]')}
                    if unquote(u.fragment) not in fragment_cache[dest]: errors.append(f'{page}: missing fragment {url}')
    for lane in ('scout','opeh'):
        for filename, key in [('records.html','records'),('sources.html','documents')]:
            soup = BeautifulSoup((output/lane/filename).read_text(encoding='utf-8'), 'html.parser')
            expected = {r['id'] for r in index[key] if r['dossier_id'] == lane}
            actual = {r['id'] for r in soup.select('article.record')}
            if actual != expected: errors.append(f'{lane}/{filename}: record IDs differ: missing {expected-actual}, extra {actual-expected}')
        # The record catalog renders each original field, including empty and nested qualifiers.
        soup = BeautifulSoup((output/lane/'records.html').read_text(encoding='utf-8'), 'html.parser')
        nodes = {node['id']:node for node in soup.select('article.record')}
        for record in (r for r in index['records'] if r['dossier_id'] == lane):
            node = nodes.get(record['id'])
            if node:
                labels = {x.get_text() for x in node.find_all('dt')}
                missing = set(record) - {'id','dossier_id','canonical_record'} - labels
                if missing: errors.append(f'{lane}/{record["id"]}: missing fields {missing}')
    if errors: raise ValueError('\n'.join(errors))
    return True

if __name__ == '__main__':
    import sys
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'presentation'
    validate(out, json.loads((out/'data/index.json').read_text(encoding='utf-8')))
    print('Static validation passed')
