"""Build the offline reader from reviewed sources; never edit source records."""
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
from urllib.parse import urlsplit, unquote, quote
from html import escape
import hashlib
import json
import os
import re
import subprocess
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'presentation'
REPO = ROOT.parents[1]
SOURCE_COMMIT = '556b60ea6d21650d3105bbdb84e3821c629ba1d5'
PREFIX = 'investigations/2026-11-04-official-records/'
PAGES = {
    'dossier/full-dossier.md': 'index.html',
    'dossier/claims.md': 'claims.html',
    'dossier/documents.md': 'documents.html',
    'dossier/conflicts-and-gaps.md': 'issues.html',
    'dossier/entities-and-roles.md': 'entities.html',
    'dossier/events.md': 'events.html',
    'dossier/financial-observations.md': 'financial.html',
    'remaining-work-instructions.md': 'follow-up.html',
}
SOURCE_FILES = list(PAGES) + ['evidence-index.json', 'dossier/release.json']
TABLES = json.loads((ROOT / 'evidence-index.json').read_text(encoding='utf-8'))['tables']
SUBJECTS = {r['subject_id']: r['display_name'] for r in TABLES['subjects']}
CLAIMS = {r['claim_id']: r for r in TABLES['claims']}
DOCS = {r['document_id']: r for r in TABLES['documents']}
# Reviewed labels are presentation-only; exact status keys remain filter values.
LABEL_REVIEW = json.loads((OUT / 'review/status-label-reviewed.json').read_text(encoding='utf-8'))
LABEL_ROWS = {r['exact_status']: r for r in LABEL_REVIEW['mapping']}
assert set(LABEL_ROWS) == {r['evidence_status'] for r in TABLES['claims']}
for status, row in LABEL_ROWS.items():
    assert set(row['claim_ids']) == {c['claim_id'] for c in TABLES['claims'] if c['evidence_status'] == status}
    assert row['decision'] in ('apply', 'exception')
STATUS_LABELS = {status: row['label'] for status, row in LABEL_ROWS.items() if row['decision'] == 'apply'}
assert all(STATUS_LABELS.values())

EVIDENCE = defaultdict(list)
DOC_CLAIMS = defaultdict(list)
for row in TABLES['claim_evidence']:
    EVIDENCE[row['claim_id']].append(row)
    DOC_CLAIMS[row['document_id']].append(row['claim_id'])
CONFLICTS = defaultdict(list)
for row in TABLES['conflict_claims']:
    CONFLICTS[row['claim_id']].append(row['conflict_id'])


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def esc(value):
    return escape(str(value if value is not None else 'Not established'), quote=True)


def anchor(kind, value):
    return kind + '-' + hashlib.sha256(value.encode()).hexdigest()[:16]


def link(url, source):
    """Only explicit HTTP(S) or paths contained in this evidence package."""
    u = urlsplit(url)
    if u.scheme:
        if u.scheme not in ('https', 'http') or not u.netloc:
            raise ValueError('Unsupported source URL: ' + url)
        return url
    if u.netloc or '\\' in unquote(u.path):
        raise ValueError('Unsafe local URL: ' + url)
    target = (source.parent / unquote(u.path)).resolve() if u.path else source
    rel = target.relative_to(ROOT).as_posix()
    if not target.exists():
        raise ValueError('Missing packaged source: ' + rel)
    mapped = OUT / PAGES[rel] if rel in PAGES else target
    result = quote(Path(os.path.relpath(mapped, OUT)).as_posix(), safe='/')
    return result + ('?' + u.query if u.query else '') + ('#' + u.fragment if u.fragment else '')


def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def render(text, source):
    md = MarkdownIt('commonmark', {'html': True}).enable('table')
    tokens = md.parse(text)
    headings = []
    table_title = [source.stem]
    def table_open(tokens, idx, options, env):
        label = esc(tokens[idx].meta['label'])
        return f'<div class="table-scroll" role="region" aria-label="{label}" tabindex="0"><table>\n'
    md.renderer.rules['table_open'] = table_open
    seen = defaultdict(int)

    def walk(items):
        for i, token in enumerate(items):
            if token.type in ('th_open', 'td_open') and token.attrGet('style'):
                align = token.attrGet('style').split(':')[-1].strip()
                assert align in ('left', 'center', 'right')
                token.attrs.pop('style')
                token.attrSet('class', 'align-' + align)
            if token.type == 'table_open':
                token.meta['label'] = table_title[0] + ' source table'
            if token.type == 'th_open':
                token.attrSet('scope', 'col')
            if token.type == 'heading_open':
                title = items[i + 1].content
                table_title[0] = title
                name = slug(title)
                seen[name] += 1
                if seen[name] > 1:
                    name += '-' + str(seen[name])
                token.attrSet('id', name)
                if token.tag == 'h2':
                    headings.append((name, title))
            if token.type == 'link_open':
                href = token.attrGet('href')
                token.attrSet('href', link(href, source))
                if urlsplit(href).scheme:
                    token.attrSet('rel', 'noreferrer noopener')
                    token.attrSet('class', 'external')
                else:
                    target = (source.parent / unquote(urlsplit(href).path)).resolve()
                    if target.suffix.lower() in ('.html', '.htm', '.js') and target.parent != OUT:
                        token.attrSet('download', '')
                        token.attrSet('title', 'Download preserved source response; not report content')
            if token.type == 'image':
                token.attrSet('src', link(token.attrGet('src'), source))
                token.attrSet('loading', 'lazy')
            if token.type in ('html_inline', 'html_block'):
                # Reviewed Markdown uses only explicit dossier anchors and line breaks.
                raw = token.content.strip()
                if not re.fullmatch(r'(?:<a id="[a-zA-Z0-9_-]+">(?:</a>)?|</a>|<br\s*/?>)', raw):
                    token.content = escape(token.content)
            if token.children:
                walk(token.children)
    walk(tokens)
    body = md.renderer.render(tokens, md.options, {})
    body = body.replace('</table>', '</table></div>')
    return body, headings


NAV = [('index.html', 'Report'), ('claims.html', 'Dossier'), ('follow-up.html', 'Follow-up'), ('about.html', 'About this copy')]
SUBNAV = [('claims.html', 'Claims'), ('documents.html', 'Documents'), ('entities.html', 'Entities & roles'), ('events.html', 'Events'), ('financial.html', 'Financial observations'), ('issues.html', 'Conflicts & gaps')]


def shell(filename, title, body, toc=(), dossier=False):
    active = 'claims.html' if dossier else filename
    nav = ''.join(f'<a href="{u}"' + (' aria-current="page"' if u == active else '') + f'>{t}</a>' for u, t in NAV)
    sub = '<nav class="subnav" aria-label="Dossier">' + ''.join(f'<a href="{u}"' + (' aria-current="page"' if u == filename else '') + f'>{t}</a>' for u, t in SUBNAV) + '</nav>' if dossier else ''
    side = '<aside class="contents"><p class="eyebrow">On this page</p><nav aria-label="Contents">' + ''.join(f'<a href="#{esc(a)}">{esc(t)}</a>' for a, t in toc if t != 'Contents') + '</nav></aside>' if toc else ''
    result = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'none'; base-uri 'none'; form-action 'none'; object-src 'none'">
<title>{esc(title)} · Bleich diligence</title><link rel="stylesheet" href="assets/report.css"><script defer src="assets/report.js"></script></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><a class="brand" href="index.html">ReBlei <span>Due diligence</span></a><nav aria-label="Main navigation">{nav}</nav><button type="button" class="print-button js-only">Print this view</button></header>
<div class="edition">Internal review · Read-only snapshot <span>Research cut-off: 4 November 2026</span></div>{sub}
<div class="layout{' with-contents' if toc else ''}">{side}<main id="main" tabindex="-1">{body}</main></div>
<footer><p>Official-record research · Michael Edward Bleich · CRD 4262671</p><p>Coverage is incomplete. Read the <a href="follow-up.html">open questions and access gaps</a>. Source-specific qualifications remain part of every finding.</p><a href="about.html">Version, provenance and opening instructions</a></footer></body></html>'''
    (OUT / filename).write_text(result, encoding='utf-8')


def source_blocks(path):
    text = path.read_text(encoding='utf-8')
    pieces = re.split(r'^<a id="([a-z]-[a-f0-9]+)"></a>\s*$', text, flags=re.M)
    assert len(pieces) % 2 == 1
    return {pieces[i]: pieces[i + 1].strip() for i in range(1, len(pieces), 2)}


def facet(name, values):
    options = ''.join(f'<option value="{esc(v)}">{esc(STATUS_LABELS.get(v, v) if name == 'Evidence status' else v)}</option>' for v in sorted(set(values)) if v)
    return f'<label for="filter-{slug(name)}">{esc(name)}<select id="filter-{slug(name)}" data-filter="{slug(name)}"><option value="">All</option>{options}</select></label>'


def filters(rows, definitions):
    fields = ''.join(facet(name, [v for row in rows for v in row['facets'][slug(name)]]) for name in definitions)
    return f'''<section class="filter-panel js-only" aria-label="Filter records"><label class="search-label" for="search">Search records<input type="search" id="search" placeholder="Name, ID, wording or source locator" autocomplete="off"></label><div class="filter-fields">{fields}</div><div class="filter-actions"><button type="button" id="reset">Clear filters</button><p id="result-count" role="status" aria-live="polite">{len(rows)} of {len(rows)} records shown</p></div></section><noscript><p class="notice">All records are shown. Use your browser's Find command to search. Evidence links and printing work without JavaScript.</p></noscript><p id="empty-state" hidden>No records match. Clear the filters or try another search.</p>'''


def record(row):
    attrs = ' '.join(f'data-{k}="{esc(json.dumps(v, ensure_ascii=False))}"' for k, v in row['facets'].items())
    return f'<article class="record" id="{row["anchor"]}" data-record-id="{esc(row["id"])}" {attrs}>{row["body"]}</article>'


def topic(cid):
    # UI grouping only; it is not a new research classification or evidence status.
    if cid.startswith(('EMP', 'ID-')): return 'Identity & employment'
    if cid.startswith('INF'): return 'Inferent — conditional affiliation'
    if cid.startswith('CORP'): return 'Corporate identity & ownership'
    if cid.startswith(('EVT', 'LIT')): return 'Investment-management events'
    if cid.startswith(('FIN', 'SEC')): return 'Filings & financial observations'
    if cid.startswith('EP'): return 'Adviser history & related filings'
    return 'Other registered observations'


def retained_url(doc, locator=''):
    url = link('../' + quote(doc['file_path'], safe='/'), OUT / 'documents.html')
    # Only physical pages are safe to translate; printed-page and CSV conventions vary.
    match = re.search(r'physical(?:\s+PDF)?\s+pages?\s*[:=]?\s*(\d+)', locator, re.I)
    if match and Path(doc['file_path']).suffix.lower() == '.pdf':
        page = int(match[1])
        if page >= 1 and (not doc['pdf_pages'] or page <= doc['pdf_pages']):
            url += '#page=' + str(page)
    return url


def build():
    fingerprints = {}
    for name in SOURCE_FILES:
        old = subprocess.check_output(['git', '-C', str(REPO), 'show', SOURCE_COMMIT + ':' + PREFIX + name])
        assert hashlib.sha256(old).hexdigest() == sha(ROOT / name), 'Reviewed input changed: ' + name
        fingerprints[name] = sha(ROOT / name)
    for doc in DOCS.values():
        path = (ROOT / doc['file_path']).resolve()
        path.relative_to(ROOT)
        assert sha(path) == doc['sha256'], doc['document_id']

    for source, dest in PAGES.items():
        if dest in ('claims.html', 'documents.html'):
            continue
        body, headings = render((ROOT / source).read_text(encoding='utf-8'), ROOT / source)
        if dest == 'index.html':
            lead = '''<div class="report-intro"><p class="eyebrow">Professional public-record investigation</p><div class="report-tools"><a class="button" href="claims.html">Explore the evidence dossier <span aria-hidden="true">→</span></a><a href="follow-up.html">Read remaining-work instructions</a></div><div class="facts"><div><strong>247</strong><span>Registered assertions</span></div><div><strong>396</strong><span>Source representations</span></div><div><strong>26</strong><span>Conflicts & qualifications</span></div></div><p class="caption">Counts describe the retained register, including unresolved propositions and access observations; they are not counts of verified findings.</p></div>'''
            # Keep the reviewed title and scope first; the sidebar replaces a long repeated outline.
            at = body.index('<h2 id="contents">')
            # Approved S1: retain the whole principal-findings block before register counts.
            end = body.index('<h3 id="scope-and-reading-rules">')
            body = body[:end] + lead + body[end:]
            body = re.sub(r'<h2 id="contents">Contents</h2>\s*(.*?)<h2 ', r'<details class="report-contents"><summary>Contents and supporting appendices</summary>\1</details><h2 ', body, count=1, flags=re.S)
        shell(dest, {'index.html': 'Research report', 'follow-up.html': 'Follow-up instructions'}.get(dest, source.split('/')[-1].replace('.md', '').replace('-', ' ').title()), body, headings, dest not in ('index.html', 'follow-up.html'))

    blocks = source_blocks(ROOT / 'dossier/claims.md')
    rows = []
    for cid, c in CLAIMS.items():
        aid = anchor('c', cid)
        body, _ = render(blocks[aid], ROOT / 'dossier/claims.md')
        status_label = STATUS_LABELS.get(c['evidence_status'])
        if status_label:
            body = body.replace('</h2>', '</h2><p class="status-label"><strong>In plain English:</strong> ' + esc(status_label) + '</p>', 1)

        docs = [DOCS[x['document_id']] for x in EVIDENCE[cid]]
        files = []
        for e in EVIDENCE[cid]:
            d = DOCS[e['document_id']]
            download = ' download' if Path(d['file_path']).suffix.lower() in ('.html', '.htm', '.js') else ''
            files.append(f'<li><a href="{esc(retained_url(d, e["locator"]))}"{download} target="_blank" rel="noopener noreferrer">{esc(d["document_id"])} — retained file</a><br><span>{esc(e["locator"])}</span><br>Filing date: {esc(d["filing_date"])} · Accession: {esc(d["accession_id"])}</li>')
        body += '<details><summary>Filing identifiers and direct source links</summary><p>Page locators retain their original wording. Physical PDF pages are 1-based; use the visible locator if your PDF viewer ignores a page link.</p><ul class="source-list">' + ''.join(files) + '</ul><p class="caption">Source HTML and scripts download as preserved files; inspect the document classification before relying on a retained response.</p></details>'
        rows.append({'id': cid, 'anchor': aid, 'body': body, 'facets': {
            'entity-person': [SUBJECTS.get(c['subject_id'], 'No assigned subject')],
            'topic-ui-group': [topic(cid)],
            'evidence-status': [c['evidence_status']],
            'linked-source-class': sorted({d['source_class'] for d in docs}),
            'linked-date-basis': sorted({'Filing date recorded' if d['filing_date'] else 'Filing date not established' for d in docs}),
        }})
    intro = '<p class="eyebrow">Evidence dossier</p><h1>Claims</h1><p class="lede">Every registered assertion, with its recorded status, source locators and qualifications.</p><p>The narrative uses the latest reviewed interpretation. Earlier formulations, conditional propositions and bounded search observations remain here for traceability. Topic is a navigation grouping only; linked date basis is not an employment or asset-measurement date.</p>'
    shell('claims.html', 'Claims', intro + filters(rows, ['Entity / person', 'Topic (UI group)', 'Evidence status', 'Linked source class', 'Linked date basis']) + '<div id="records">' + ''.join(map(record, rows)) + '</div>', dossier=True)

    blocks = source_blocks(ROOT / 'dossier/documents.md')
    rows = []
    for did, d in DOCS.items():
        body, _ = render(blocks[anchor('d', did)], ROOT / 'dossier/documents.md')
        related = DOC_CLAIMS[did]
        body += '<p>Linked claims: ' + (', '.join(f'<a href="claims.html#{anchor("c", c)}">{esc(c)}</a>' for c in related) or 'No linked claim; retained for provenance and coverage review.') + '</p>'
        body += '<details><summary>Additional filing and preservation metadata</summary><pre class="metadata">' + esc(json.dumps(json.loads(d['metadata_json']), ensure_ascii=False, indent=2)) + '</pre></details>'
        subjects = {SUBJECTS.get(CLAIMS[c]['subject_id'], 'No assigned subject') for c in related}
        rows.append({'id': did, 'anchor': anchor('d', did), 'body': body, 'facets': {
            'linked-entity-person': sorted(subjects) or ['No linked claim'],
            'source-class': [d['source_class']],
            'authority': [d['authority'] or 'Not established'],
            'date-basis': ['Filing date recorded' if d['filing_date'] else 'Filing date not established', 'Period end recorded' if d['period_end'] else 'Period end not established'],
        }})
    intro = '<p class="eyebrow">Evidence dossier</p><h1>Documents</h1><p class="lede">396 retained source representations, with provenance and local evidence links.</p><p>Includes originals, compressed members, derivatives, unjoined leads and failed responses. This is not a unique-filing count. SHA256 identifies bytes, not truth. An unavailable filing date remains unknown; retrieval time is shown separately.</p>'
    shell('documents.html', 'Documents', intro + filters(rows, ['Linked entity / person', 'Source class', 'Authority', 'Date basis']) + '<div id="records">' + ''.join(map(record, rows)) + '</div>', dossier=True)

    stamp = datetime.now(timezone.utc).isoformat()
    meta = {'reviewed_status_labels_sha256': sha(OUT / 'review/status-label-reviewed.json'), 'source_commit': SOURCE_COMMIT, 'research_cutoff': '2026-11-04', 'built_at_utc': stamp, 'inputs_sha256': fingerprints, 'counts': {k: len(v) for k, v in TABLES.items()}, 'evidence_files_verified': len(DOCS), 'read_only': True, 'network_required_to_read': False, 'generator_dependency': 'markdown-it-py==4.2.0'}
    (OUT / 'build.json').write_text(json.dumps(meta, indent=2) + '\n', encoding='utf-8')
    drafts = ''.join(f'<li>{kind.title()} {letter.upper()}: <a href="../visualization/{folder}/{kind}-{letter}.pdf">PDF</a> · <a href="../visualization/{folder}/{kind}-{letter}.svg">SVG</a></li>' for kind, folder in [('ownership', 'ownership'), ('timeline', 'timelines')] for letter in 'abc')
    body = f'''<p class="eyebrow">Reader guide</p><h1>About this copy</h1><p class="lede">A portable, read-only view of the reviewed research and its preserved evidence.</p><h2 id="opening">Open and share</h2><p>Open <strong>presentation/index.html</strong> in a browser. Keep the entire investigation folder together when copying it; the evidence files live alongside this presentation folder. No installation, local server or internet connection is needed.</p><p>Search and filters affect only the current view. They save no notes or decisions. Use claim and document IDs in your existing review process. Print this view prints the current page and, on dossier lists, the displayed records. Clear filters to print all records. Source URLs marked “online” require a connection.</p><h2 id="version">Version and provenance</h2><dl><dt>Research cut-off</dt><dd>4 November 2026</dd><dt>Input research commit</dt><dd><code>{SOURCE_COMMIT}</code></dd><dt>HTML built at UTC</dt><dd>{esc(stamp)}</dd></dl><p><a href="build.json">Build metadata and input hashes</a> · <a href="../SHA256SUMS.txt">Complete package checksum manifest</a> · <a href="../dossier/full-dossier.md">Reviewed Markdown manuscript</a> · <a href="../evidence-index.json">Normalized source index</a> · <a href="../dossier/release.json">Dossier review record</a></p><h2 id="limits">Reading the evidence</h2><p>The report preserves filed assertions, official-record inferences, conditional affiliations and access observations. A firm sanction is not a personal sanction; an administrative withdrawal is not enforcement; an award is not proof of collection. Unknown dates remain unknown. This package does not establish comprehensive career or court clearance.</p><p>Some retained files are failed responses, provider transformations or compressed archive members. Read their source class and preservation metadata. PDF page links use physical pages only when the original locator explicitly identifies them; the complete locator remains visible. Browser PDF behavior varies.</p><p class="notice">NYSCEF remains an accepted access gap. PACER has no authorized account. See the <a href="follow-up.html">separate instructions for unresolved records and access conditions</a>.</p><h2 id="drafts">Separate visualization review</h2><p>These six layouts are drafts awaiting selection. They are not selected report figures. Each family uses the same selected facts; the report remains complete without choosing a diagram.</p><ul>{drafts}</ul><p><a href="../visualization/README.md">Draft comparison guide and qualifications (Markdown)</a></p>'''
    shell('about.html', 'About this copy', body, [('opening', 'Opening instructions'), ('version', 'Version & provenance'), ('limits', 'Reading the evidence'), ('drafts', 'Visualization drafts')])
    print(json.dumps({'pages': len(PAGES) + 1, 'claims': len(CLAIMS), 'documents': len(DOCS), 'source_files_hash_verified': len(DOCS), 'source_commit': SOURCE_COMMIT}))


if __name__ == '__main__':
    build()
