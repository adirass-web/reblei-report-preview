"""Check preservation, safe links and offline completeness without rewriting research."""
from urllib.parse import urlsplit, unquote
from datetime import datetime, timezone
import hashlib
import html
import json
import re
import sys
sys.dont_write_bytecode = True
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from build_front import ROOT, OUT, PAGES, TABLES, anchor, link, render


def norm(text):
    return re.sub(r'\s+', ' ', html.unescape(str(text if text is not None else 'Not established'))).strip()


def validate():
    pages = {p.name: BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser') for p in OUT.glob('*.html')}
    assert set(pages) == set(PAGES.values()) | {'about.html'}
    checked = 0
    for name, soup in pages.items():
        assert soup.html['lang'] == 'en'
        assert len(soup.select('h1')) == 1, name
        assert soup.select_one('main#main') and soup.select_one('.skip')
        assert not soup.select('iframe, form, object, embed, style')
        assert 'connect-src \'none\'' in soup.find('meta', attrs={'http-equiv': 'Content-Security-Policy'})['content']
        ids = [x['id'] for x in soup.select('[id]')]
        assert len(ids) == len(set(ids)), ('Duplicate anchor', name)
        for tag in soup.find_all(True):
            assert not any(k.startswith('on') or k == 'style' for k in tag.attrs), (name, tag.name)
        for tag in soup.select('[href], [src]'):
            url = tag.get('href', tag.get('src'))
            u = urlsplit(url)
            if u.scheme:
                assert tag.name == 'a' and u.scheme in ('https', 'http'), (name, url)
                continue
            assert not u.netloc
            target = (OUT / unquote(u.path)).resolve() if u.path else OUT / name
            target.relative_to(ROOT)
            assert target.exists(), (name, url)
            if u.fragment and target.parent == OUT and target.suffix == '.html':
                assert pages[target.name].find(id=unquote(u.fragment)), (name, url)
            if u.fragment and target.suffix == '.pdf':
                assert re.fullmatch('page=[1-9][0-9]*', u.fragment)
            if tag.name == 'script':
                assert target == OUT / 'assets/report.js' and not tag.string
            checked += 1
    claim_page = pages['claims.html']
    assert len(claim_page.select('.record')) == len(TABLES['claims'])
    for c in TABLES['claims']:
        row = claim_page.find(id=anchor('c', c['claim_id']))
        assert row and row['data-record-id'] == c['claim_id']
        text = norm(row.get_text(' ', strip=True))
        assert norm(c['statement']) in text, ('Statement changed', c['claim_id'])
        assert c['evidence_status'] in text, c['claim_id']
        for e in (x for x in TABLES['claim_evidence'] if x['claim_id'] == c['claim_id']):
            assert norm(e['locator']) in text, (c['claim_id'], e['locator'])
            assert row.find('a', href='documents.html#' + anchor('d', e['document_id']))
    assert 'Later qualification:' in claim_page.find(id=anchor('c', 'ID-C012')).get_text()
    assert pages['issues.html'].get_text().count('Current-reading note: original Cboe orders were subsequently recovered.') == 2
    doc_page = pages['documents.html']
    assert len(doc_page.select('.record')) == len(TABLES['documents'])
    for d in TABLES['documents']:
        row = doc_page.find(id=anchor('d', d['document_id']))
        assert row
        text = norm(row.get_text(' ', strip=True))
        for field in ('title', 'source_class', 'sha256', 'retrieved_at_utc', 'preservation_status'):
            assert norm(d[field]) in text, (d['document_id'], field)
        assert json.loads(row.select_one('.metadata').get_text()) == json.loads(d['metadata_json'])
        assert hashlib.sha256((ROOT / d['file_path']).read_bytes()).hexdigest() == d['sha256']
    for c in TABLES['conflicts']:
        assert pages['issues.html'].find(id=anchor('x', c['conflict_id']))

    text_checks = 0
    for source, dest in PAGES.items():
        if dest in ('claims.html', 'documents.html'):
            continue
        page_text = norm(pages[dest].select_one('main').get_text(' ', strip=True))
        tokens = MarkdownIt('commonmark', {'html': True}).enable('table').parse((ROOT / source).read_text(encoding='utf-8'))
        for t in tokens:
            if t.type != 'inline':
                continue
            parts = []
            for child in t.children or []:
                if child.type in ('text', 'code_inline'):
                    parts.append(child.content)
                elif child.type in ('softbreak', 'hardbreak') or child.content == '<br>':
                    parts.append(' ')
                elif child.type in ('link_open', 'link_close', 'strong_open', 'strong_close', 'em_open', 'em_close'):
                    parts.append(' ')
            expected = norm(''.join(parts))
            if expected:
                assert expected in page_text, (dest, expected[:180])
                text_checks += 1
    for unsafe in ('javascript:alert(1)', 'data:text/html,hi', '//example.com/a', '../../../../../outside.txt', '..%5C..%5Coutside'):
        try:
            link(unsafe, ROOT / 'dossier/claims.md')
        except ValueError:
            pass
        else:
            raise AssertionError('Unsafe link accepted: ' + unsafe)
    try:
        link('../absent-original.pdf', ROOT / 'dossier/claims.md')
    except ValueError:
        pass
    else:
        raise AssertionError('Missing original silently accepted')
    injected, _ = render('<script>alert(1)</script>\n\n<img src=x onerror=alert(1)>', ROOT / 'dossier/claims.md')
    assert not BeautifulSoup(injected, 'html.parser').select('script, img')
    metadata = json.loads((OUT / 'build.json').read_text(encoding='utf-8'))
    for path, digest in metadata['inputs_sha256'].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'pages': len(pages), 'local_links_and_resources_checked': checked, 'reviewed_text_fragments_preserved': text_checks, 'claims_preserved': len(TABLES['claims']), 'evidence_links_preserved': len(TABLES['claim_evidence']), 'document_metadata_and_original_hashes_verified': len(TABLES['documents']), 'conflicts_preserved': len(TABLES['conflicts']), 'safe_link_and_html_checks': 'passed', 'missing_local_original_behavior': 'Build fails explicitly; no dead link is silently emitted', 'source_commit': metadata['source_commit']}
    (OUT / 'review/static-validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    validate()
