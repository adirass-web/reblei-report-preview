"""Build a portable, source-scoped static reader from the approved index."""
from pathlib import Path
from html import escape
from urllib.parse import quote, urlsplit
import argparse
import json
import re
import shutil

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[1]
E = lambda v: escape(str(v), quote=True)


def render_markdown(text, lane, records, documents):
    from markdown_it import MarkdownIt
    # Authored HTML and images are not part of the manuscript format.
    if re.search(r'<\s*/?\s*[A-Za-z!][^>]*>', text) or re.search(r'!\[', text):
        raise ValueError('Authored HTML and images are prohibited')
    if re.search(r'\]\(\s*(?:javascript|data|vbscript|file):', text, re.I):
        raise ValueError('Unsafe authored link')
    md = MarkdownIt('commonmark', {'html': False}).enable('table')
    rec = {r['id'] for r in records if r['dossier_id'] == lane}
    rec.update(r['canonical_id'] for r in records if r['dossier_id'] == lane and r.get('canonical_id'))
    deferred = {r['id'] for r in records if r['dossier_id'] == 'deferred'}
    docs = {d['id'] for d in documents if d['dossier_id'] == lane}
    md.renderer.rules['table_open'] = lambda tokens, idx, options, env: '<div class="table-scroll" role="region" aria-label="Report table" tabindex="0"><table>\n'
    md.renderer.rules['table_close'] = lambda tokens, idx, options, env: '</table></div>\n'
    tokens = md.parse(text)
    headings = {}
    def walk(items):
        for i, token in enumerate(items):
            if token.type in ('th_open', 'td_open') and token.attrGet('style'):
                align = token.attrGet('style').split(':')[-1].strip()
                if align not in ('left', 'center', 'right'): raise ValueError('Unexpected table alignment')
                token.attrs.pop('style')
                token.attrSet('class', 'align-' + align)
            if token.type == 'heading_open':
                title = items[i + 1].content
                slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-') or 'section'
                headings[slug] = headings.get(slug, 0) + 1
                token.attrSet('id', slug + ('-' + str(headings[slug]) if headings[slug] > 1 else ''))
            if token.type == 'link_open':
                href = token.attrGet('href') or ''
                if href.startswith('record:'):
                    ident = href[7:]
                    if ident not in rec and ident not in deferred: raise ValueError('Unknown or cross-lane record: ' + ident)
                    token.attrSet('href', ('records.html#' if ident in rec else '../coverage.html#') + quote(ident, safe=''))
                elif href.startswith('doc:'):
                    ident, sep, locator = href[4:].partition('#')
                    if ident not in docs: raise ValueError('Unknown or cross-lane document: ' + ident)
                    if not sep or not re.fullmatch(r'(?:page|row|line)=[1-9][0-9]*|section=body', locator):
                        raise ValueError('Invalid source locator: ' + href)
                    token.attrSet('href', source_link(ident, locator))
                    token.attrSet('title', 'Retained source; ' + locator)
                elif urlsplit(href).scheme in ('http', 'https') and urlsplit(href).netloc:
                    token.attrSet('class', 'external')
                    token.attrSet('rel', 'noopener noreferrer')
                    token.attrSet('title', 'External reference; not retrieved by this reader')
                elif href.startswith('#'):
                    pass
                else:
                    raise ValueError('Unsafe or unsupported link: ' + href)
            if token.children: walk(token.children)
    walk(tokens)
    return financial_tables(md.renderer.render(tokens, md.options, {}))



def financial_tables(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    for table in soup.select('table'):
        headers = table.select('thead th')
        classes = []
        for h in headers:
            label = h.get_text(' ', strip=True).lower()
            classes.append('assets' if label == 'total assets' else 'liabilities' if label == 'total liabilities' else 'equity' if label in ("members' capital", 'members’ capital') else None)
        if not any(classes): continue
        for row in table.select('tr'):
            for i, cell in enumerate(row.find_all(['th', 'td'], recursive=False)):
                if i < len(classes) and classes[i]: cell['class'] = cell.get('class', []) + ['financial-' + classes[i]]
        legend = soup.new_tag('p', attrs={'class':'financial-legend'})
        legend.string = 'Financial category legend: Assets (blue) · Liabilities (amber) · Members’ capital / equity (teal). Labels identify each category.'
        table.parent.insert_before(legend)
    return str(soup)


def validate_figure(f, lane, records, root):
    fields = {'id','lane','title','summary','limitation','section_anchor','appendix','svg','png','csv','json','table','source_record_ids','kind','legend','alt'}
    if not isinstance(f, dict) or not fields <= set(f) or set(f) - fields - {'highlight'}: raise ValueError('Invalid figure schema')
    if 'highlight' in f and (not isinstance(f['highlight'], str) or not f['highlight'].strip()): raise ValueError('Invalid figure highlight')
    for key in ('id','lane','title','summary','limitation','section_anchor','kind','alt'):
        if not isinstance(f[key], str) or not f[key].strip(): raise ValueError('Missing figure ' + key)
    if f['lane'] != lane or not re.fullmatch(lane + r'-[a-z0-9-]+', f['id']): raise ValueError('Invalid figure lane or id')
    if not re.fullmatch(r'[a-z0-9-]+', f['section_anchor']): raise ValueError('Invalid figure anchor')
    if type(f['appendix']) is not bool or not isinstance(f['table'], list) or not f['table'] or not all(isinstance(r, dict) and r for r in f['table']): raise ValueError('Invalid figure table')
    if not isinstance(f['legend'], dict) or not f['legend'] or not all(isinstance(k,str) and k and isinstance(v,str) and re.fullmatch(r'#[0-9a-fA-F]{6}',v) for k,v in f['legend'].items()): raise ValueError('Invalid legend')
    ids = {r['id'] for r in records if r['dossier_id'] == lane}
    if not isinstance(f['source_record_ids'], list) or not f['source_record_ids'] or not all(isinstance(i,str) and i in ids for i in f['source_record_ids']): raise ValueError('Invalid figure source ownership')
    for ext in ('svg','png','json','csv'):
        expected = f'figures/{lane}/{f["id"]}.{ext}'
        if f[ext] != expected: raise ValueError('Invalid figure path')
        path = root / expected
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(root.resolve()): raise ValueError('Missing or unsafe figure file: ' + expected)
    import xml.etree.ElementTree as ET
    raw = (root / f['svg']).read_bytes()
    # ElementTree discards processing instructions; inspect UTF-8 bytes before parsing.
    try: raw.decode('utf-8')
    except UnicodeDecodeError as exc: raise ValueError('SVG must be UTF-8') from exc
    if b'\x00' in raw: raise ValueError('SVG must be UTF-8')
    if re.search(br'<\?(?!xml\s)[\s\S]*?\?>|<!ENTITY\b|<!DOCTYPE[^>]*\[', raw, re.I): raise ValueError('Unsafe SVG declaration')
    try: tree = ET.fromstring(raw)
    except ET.ParseError as exc: raise ValueError('Invalid SVG') from exc
    svg_ns = 'http://www.w3.org/2000/svg'
    allowed_svg = {'svg','g','text','path','use','defs','rect','clipPath','metadata','style','pattern'}
    allowed_metadata = {
        '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF',
        '{http://creativecommons.org/ns#}Work', '{http://creativecommons.org/ns#}Agent',
        '{http://purl.org/dc/elements/1.1/}type', '{http://purl.org/dc/elements/1.1/}format',
        '{http://purl.org/dc/elements/1.1/}creator', '{http://purl.org/dc/elements/1.1/}title',
    }
    allowed_attrs = {'id','style','x','y','transform','d','clip-path','width','height','viewBox','version','type','patternUnits','fill'}
    local_ref = re.compile(r'^#[A-Za-z_][A-Za-z0-9_.:-]*$')
    for node in tree.iter():
        if node.tag not in allowed_metadata and node.tag not in {'{'+svg_ns+'}'+tag for tag in allowed_svg}: raise ValueError('Unsupported SVG element')
        if node.tag == '{'+svg_ns+'}style' and (len(node) != 0 or (node.text or '').strip() != '*{stroke-linejoin: round; stroke-linecap: butt}'): raise ValueError('Unsupported SVG stylesheet')
        for key, value in node.attrib.items():
            if key == '{http://www.w3.org/1999/xlink}href':
                if not local_ref.fullmatch(value): raise ValueError('Unsafe SVG reference')
            elif key == '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource':
                if value != 'http://purl.org/dc/dcmitype/StillImage': raise ValueError('Unsafe SVG metadata')
            elif key not in allowed_attrs: raise ValueError('Unsupported SVG attribute')
            if key == 'style':
                properties = {'fill','font-family','font-size','font-weight','stroke','stroke-dasharray','stroke-dashoffset','stroke-linecap','stroke-linejoin','stroke-width','text-anchor'}
                for declaration in value.split(';'):
                    if not declaration.strip(): continue
                    prop, sep, val = declaration.partition(':')
                    prop, val = prop.strip(), val.strip()
                    if not sep or prop not in properties or not val: raise ValueError('Unsupported SVG CSS property')
                    if prop == 'fill' and re.fullmatch(r'url\(#[A-Za-z_][A-Za-z0-9_.:-]*\)', val): continue
                    if not re.fullmatch(r"[A-Za-z0-9#.,' _-]+", val): raise ValueError('Unsafe SVG CSS value')
            elif key == 'fill':
                if not re.fullmatch(r'#[0-9a-fA-F]{3,8}|[A-Za-z]+|url\(#[A-Za-z_][A-Za-z0-9_.:-]*\)', value): raise ValueError('Unsafe SVG fill')
            elif key == 'clip-path' and not re.fullmatch(r'url\(#[A-Za-z_][A-Za-z0-9_.:-]*\)', value): raise ValueError('Unsafe SVG clip path')
    return f


def load_figures(root, index):
    result = {}
    all_ids = set()
    for lane, count in (('scout',8),('opeh',7)):
        path = root / 'figures' / lane / 'manifest.json'
        try: figures = json.loads(path.read_text(encoding='utf-8'))
        except (OSError, ValueError) as exc: raise ValueError('Missing or invalid manifest: ' + str(path)) from exc
        if not isinstance(figures,list) or len(figures) != count: raise ValueError('Incorrect figure count: ' + lane)
        for i, f in enumerate(figures):
            validate_figure(f, lane, index['records'], root)
            if f['id'] in all_ids or f['appendix'] != (i >= 5): raise ValueError('Duplicate figure or incorrect appendix order')
            all_ids.add(f['id'])
        result[lane] = figures
    return result


def figure_html(f):
    columns = list(dict.fromkeys(k for row in f['table'] for k in row))
    table = '<div class="table-scroll" role="region" aria-label="Figure data" tabindex="0"><table><thead><tr>' + ''.join('<th scope="col">'+E(k)+'</th>' for k in columns) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>'+E(row.get(k) if row.get(k) is not None else 'Unknown')+'</td>' for k in columns) + '</tr>' for row in f['table']) + '</tbody></table></div>'
    sources = ', '.join('<a href="records.html#'+E(quote(i, safe=''))+'">'+E(i)+'</a>' for i in f['source_record_ids'])
    downloads = ' · '.join('<a href="../figures/'+E(f['lane'])+'/'+E(f['id'])+'.'+ext+'" download>'+ext.upper()+'</a>' for ext in ('svg','png','csv','json'))
    highlight = '<p class="visual-highlight"><strong>Key finding:</strong> ' + E(f['highlight']) + '</p>' if f.get('highlight') else ''
    return '<figure class="visual" id="'+E(f['id'])+'"><h2>'+E(f['title'])+'</h2><img src="../'+E(f['svg'])+'" alt="'+E(f['alt'])+'"><figcaption><p><a href="../'+E(f['svg'])+'">Open full-size figure</a></p><p class="visual-summary">'+E(f['summary'])+'</p>'+highlight+'<p class="visual-limitation"><strong>Limitation:</strong> '+E(f['limitation'])+'</p><p>Sources: '+sources+'</p><p>Download: '+downloads+'</p></figcaption><h3>Figure data</h3>'+table+'</figure>'

def source_link(ident, locator):
    typ, _, number = locator.partition('=')
    if typ == 'page': return '../evidence/' + ident + '/pages/' + number.zfill(4) + '.png'
    return '../evidence/' + ident + '/excerpt.html#' + quote(locator, safe='=')


def display(value, lane=None, rec_ids=(), doc_ids=()):
    if isinstance(value, dict):
        return '<dl>' + ''.join('<dt>' + E(k) + '</dt><dd>' + display(v, lane, rec_ids, doc_ids) + '</dd>' for k, v in value.items()) + '</dl>'
    if isinstance(value, list):
        return '<ul>' + ''.join('<li>' + display(v, lane, rec_ids, doc_ids) + '</li>' for v in value) + '</ul>' if value else '[]'
    if value is None: return 'null'
    if isinstance(value, bool): return str(value).lower()
    s = str(value)
    if s in rec_ids: return '<a href="records.html#' + E(quote(s, safe='')) + '">' + E(s) + '</a>'
    if s.startswith('doc:'):
        ident, sep, locator = s[4:].partition('#')
        if ident in doc_ids and sep and re.fullmatch(r'(?:page|row|line)=[1-9][0-9]*|section=body', locator):
            return '<a href="' + E(source_link(ident, locator)) + '">' + E(s) + '</a>'
    return E(s)


def filters(count, types):
    options = ''.join('<option value="' + E(t) + '">' + E(t) + '</option>' for t in sorted(types))
    return ('<section class="filter-panel js-only" aria-label="Filter records"><label for="search">Search<input id="search" type="search" autocomplete="off"></label>'
            '<div class="filter-fields"><label for="filter-collection">Collection<select id="filter-collection" data-filter="collection"><option value="">All</option>' + options + '</select></label></div>'
            '<div class="filter-actions"><button type="button" id="reset">Clear filters</button><p id="result-count" role="status" aria-live="polite">' + str(count) + ' of ' + str(count) + ' records shown</p></div></section>'
            '<noscript><p class="notice">All records are shown. Use your browser’s Find command to search.</p></noscript><p id="empty-state" hidden>No records match. Clear the filters.</p>')


def records_page(records, lane, documents=()):
    selected = [r for r in records if r['dossier_id'] == lane]
    ids = {r['id'] for r in selected}
    docids = {d['id'] for d in documents if d['dossier_id'] == lane}
    rows = []
    for r in selected:
        ident = r['id']
        collection = r.get('collection', '')
        fields = {k:v for k,v in r.items() if k not in ('id','dossier_id','canonical_record')}
        badge = '<p class="notice"><strong>Appendix material — not a main finding.</strong></p>' if r.get('appendix_only') else ''
        highlights = {k: r[k] for k in ('evidentiary_status', 'confidence', 'attributed_to', 'attribution') if r.get(k)}
        summary = display(highlights, lane, ids, docids) if highlights else ''
        alias = r.get('canonical_id', ident)
        alias_html = '<span id="' + E(alias) + '"></span>' if alias != ident and alias not in ids else ''
        rows.append('<article class="record" id="' + E(ident) + '" data-collection="' + E(json.dumps([collection])) + '">' + alias_html + '<h2>' + E(ident) + '</h2>' + badge + summary + display(fields, lane, ids, docids) + '</article>')
    return '<p class="eyebrow">Source-scoped register</p><h1>Records</h1><p class="lede">Original record IDs, source citations, dependencies, calculations and qualifications.</p>' + filters(len(rows), {r.get('collection','') for r in selected}) + ''.join(rows)


def shell(title, body, prefix):
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'"><title>''' + E(title) + ''' · Supplied dossiers</title><link rel="stylesheet" href="''' + prefix + '''assets/report.css"><script defer src="''' + prefix + '''assets/report.js"></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="''' + prefix + '''index.html">ReBlei <span>Supplied dossiers</span></a><nav aria-label="Main navigation"><a href="''' + prefix + '''scout/index.html">Scout</a><a href="''' + prefix + '''opeh/index.html">OPEH</a></nav><button type="button" class="print-button js-only">Print this view</button></header><div class="edition">Source-scoped review · retained supplied files</div><div class="layout"><main id="main" tabindex="-1">''' + body + '''</main></div><footer>Read source citations and qualifications alongside each record. External references are marked online and are not retrieved by this reader.</footer></body></html>'''


def evidence(doc, output, repo):
    ident = doc['id']
    target = output / 'evidence' / ident
    target.mkdir(parents=True, exist_ok=True)
    src = (repo / doc['source_path']).resolve()
    src.relative_to((repo / 'corpus').resolve())
    shutil.copyfile(src, target / ('original' + src.suffix))
    pages = repo / 'corpus' / 'documents' / ident / 'pages'
    if pages.exists(): shutil.copytree(pages, target / 'pages', dirs_exist_ok=True)
    mdfile = repo / 'corpus' / 'documents' / ident / 'document.md'
    text = mdfile.read_text(encoding='utf-8') if mdfile.exists() else ''
    if src.suffix.lower() in ('.txt', '.md', '.paper', '.csv'):
        text = src.read_text(encoding='utf-8-sig', errors='replace')
    lines = text.splitlines()
    rendered = '\n'.join('<span id="line=' + str(i) + '">' + E(line) + '</span>' for i, line in enumerate(lines, 1))
    # Row numbers refer to source CSV rows, not extracted Markdown lines.
    if src.suffix.lower() == '.csv':
        import csv, io
        rows = list(csv.reader(io.StringIO(src.read_text(encoding='utf-8-sig'))))
        rendered += '\n\n' + '\n'.join('<span id="row=' + str(i) + '">' + E(' | '.join(row)) + '</span>' for i, row in enumerate(rows, 1))
    (target / 'excerpt.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Source excerpt</title></head><body><h1>Extracted text · ' + E(ident) + '</h1><p>Generated text; consult the retained original for context.</p><pre id="section=body">' + rendered + '</pre></body></html>', encoding='utf-8')


def reader_index(index):
    result = dict(index)
    dispositions = {(d['collection'], d['id']): d for d in index['dispositions']}
    result['records'] = []
    for record in index['records']:
        if record['dossier_id'] == 'deferred':
            disposition = dispositions[(record['collection'], record['id'])]
            result['records'].append({k: disposition[k] for k in ('id', 'collection', 'dossier_id', 'disposition', 'reason')})
        else:
            result['records'].append({k: v for k, v in record.items() if k != 'canonical_record'})
    return result


def build(index, output, repo=REPO):
    index = reader_index(index)
    figures = load_figures(BASE / 'presentation', index)
    output.mkdir(parents=True, exist_ok=True)
    assets = BASE / 'presentation' / 'assets'
    if assets.resolve() != (output / 'assets').resolve(): shutil.copytree(assets, output / 'assets', dirs_exist_ok=True)
    figure_assets = BASE / 'presentation' / 'figures'
    if figure_assets.resolve() != (output / 'figures').resolve(): shutil.copytree(figure_assets, output / 'figures', dirs_exist_ok=True)
    (output / 'data').mkdir(exist_ok=True)
    (output / 'data' / 'index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / 'index.html').write_text(shell('Supplied dossiers', '<p class="eyebrow">Independent source collections</p><h1>Supplied dossiers</h1><p class="lede">Two separate reports and their source-scoped records.</p><ul><li><a href="scout/index.html">Scout dossier</a> · <a href="scout/visuals.html">Scout visuals</a></li><li><a href="opeh/index.html">OPEH dossier</a> · <a href="opeh/visuals.html">OPEH visuals</a></li></ul><p class="notice">Mixed-source records are deferred and are counted only as a coverage limitation.</p>', ''), encoding='utf-8')
    deferred = [r for r in index['records'] if r['dossier_id'] == 'deferred']
    coverage = '<h1>Deferred coverage</h1><p>These mixed-source records are deferred from both dossiers.</p>' + ''.join('<article class="record" id="' + E(r['id']) + '"><h2>' + E(r['id']) + '</h2>' + display(r) + '</article>' for r in deferred)
    (output / 'coverage.html').write_text(shell('Deferred coverage', coverage, ''), encoding='utf-8')
    done = set()
    for d in index['documents']:
        if d['id'] not in done:
            evidence(d, output, repo); done.add(d['id'])
    for lane in ('scout','opeh'):
        path = output / lane; path.mkdir(exist_ok=True)
        doclist = [d for d in index['documents'] if d['dossier_id'] == lane]
        body = render_markdown((BASE / lane / 'dossier.md').read_text(encoding='utf-8'), lane, index['records'], index['documents'])
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(body, 'html.parser')
        for fig in figures[lane][:5]:
            anchor = soup.find(id=fig['section_anchor'])
            if not anchor or anchor.name not in ('h2','h3'): raise ValueError('Missing figure section anchor: ' + fig['section_anchor'])
            next_node = anchor.find_next_sibling()
            target = next_node if next_node and next_node.name == 'p' else anchor
            target.insert_after(BeautifulSoup(figure_html(fig), 'html.parser'))
        body = str(soup)
        headings = BeautifulSoup(body, 'html.parser').select('h2[id]')
        if headings:
            toc = '<details class="report-contents"><summary>Contents</summary><nav aria-label="Report contents"><ul>' + ''.join('<li><a href="#' + E(h['id']) + '">' + E(h.get_text()) + '</a></li>' for h in headings) + '</ul></nav></details>'
            body = body.replace('</h1>', '</h1>' + toc, 1) if '</h1>' in body else toc + body
        nav = '<nav class="subnav" aria-label="Dossier sections"><a href="index.html">Report</a><a href="records.html">Records</a><a href="sources.html">Sources</a><a href="visuals.html">Visuals</a></nav>'
        (path / 'index.html').write_text(shell(lane.upper() + ' report', nav + body, '../'), encoding='utf-8')
        gallery = '<h1>Visuals</h1><p>Figures with source records, qualifications and downloadable data.</p>' + ''.join(figure_html(f) for f in figures[lane])
        (path / 'visuals.html').write_text(shell(lane.upper() + ' visuals', nav + gallery, '../'), encoding='utf-8')
        (path / 'records.html').write_text(shell(lane.upper() + ' records', nav + records_page(index['records'], lane, index['documents']), '../'), encoding='utf-8')
        rows = []
        for d in doclist:
            ident = d['id']; original = next((output / 'evidence' / ident).glob('original.*'))
            pages = sorted((output / 'evidence' / ident / 'pages').glob('*.png'))
            links = '<p><a href="../evidence/' + E(ident) + '/' + E(original.name) + '" download>Retained original</a> · <a href="../evidence/' + E(ident) + '/excerpt.html#section=body">Extracted text</a></p>'
            if pages: links += '<p>Physical pages: ' + ' '.join('<a href="../evidence/' + E(ident) + '/pages/' + p.name + '">' + str(int(p.stem)) + '</a>' for p in pages) + '</p>'
            rows.append('<article class="record" id="' + E(ident) + '" data-collection="' + E(json.dumps([str(d.get('document_type',''))])) + '"><h2>' + E(ident) + '</h2>' + links + display(d) + '</article>')
        intro = '<p class="eyebrow">Source-scoped catalog</p><h1>Sources</h1><p class="lede">Retained originals, physical pages and document metadata.</p>'
        (path / 'sources.html').write_text(shell(lane.upper() + ' sources', nav + intro + filters(len(rows), {str(d.get('document_type','')) for d in doclist}) + ''.join(rows), '../'), encoding='utf-8')


def main():
    import adapter
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, default=BASE/'presentation'); parser.add_argument('--validate', action='store_true'); args = parser.parse_args()
    manifest = BASE / 'audit' / 'input-manifest.json'
    if args.validate:
        adapter.verify_inputs(REPO, json.loads(manifest.read_text(encoding='utf-8')))
    index = adapter.build_index(REPO); adapter.validate_index(index, REPO)
    build(index, args.output.resolve())
    if args.validate:
        from validate_front import validate
        validate(args.output.resolve(), index)
    print('Built reader at', args.output)

if __name__ == '__main__': main()
