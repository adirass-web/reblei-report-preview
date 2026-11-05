"""Validate selected static exports and seal only the visualization directory."""
from pathlib import Path
import sys, hashlib, json, re, xml.etree.ElementTree as ET
from urllib.parse import unquote
R = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(R/'.runtime/python'))
import fitz
from PIL import Image

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def included(p): return p.is_file() and not any(x in {'.runtime', '.cache', '__pycache__'} for x in p.relative_to(R).parts) and p.suffix != '.pyc'

snap = json.loads((R/'source-snapshot.json').read_text(encoding='utf-8-sig'))
repo = R.parents[2]
report = {'source_commit': snap['source_commit'], 'inputs': [], 'exports': [], 'markdown_link_failures': []}
for f in snap['files']:
    original, copy = repo/f['repository_path'], R/f['snapshot_path']
    assert digest(original) == digest(copy) == f['sha256'], f'Input changed: {original}'
    report['inputs'].append({'path': f['snapshot_path'], 'copy_and_canonical_match': True, 'sha256': f['sha256']})
manifest = json.loads((R/'assets.json').read_text(encoding='utf-8'))
assert len(manifest['assets']) == 6
for asset in manifest['assets']:
    files = asset['files']
    ET.parse(R/files['svg'])
    with Image.open(R/files['png']) as im:
        size = list(im.size)
        im.verify()
    with fitz.open(R/files['pdf']) as pdf:
        assert len(pdf) == 1 and len(pdf[0].get_text()) > 100, asset['id']
        page = list(pdf[0].rect)
    report['exports'].append({'id': asset['id'], 'svg_xml_valid': True, 'png_pixels': size, 'pdf_pages': 1, 'pdf_rect': page})
checks = json.loads((R/'review/semantic-checks.json').read_text(encoding='utf-8'))
assert all(checks['snapshot_hashes'].values())
assert not checks['timeline']['claim_record_mismatches']
assert not checks['ownership']['dot_edge_mismatch']
for v in 'abc':
    t = checks['timeline'][v]
    assert len(t['observation_ids_present']) == 16
    assert not any(t[k] for k in ['missing_titles', 'missing_details', 'missing_claim_ids'])
    assert len(checks['ownership'][v]) == 14
    assert all(e['label_present'] and e['claim_exists'] for e in checks['ownership'][v])
for category in ('local_link_failures', 'fragment_failures'):
    assert not any(checks[category].values())
report['semantic_checks_pass'] = True
# Immutable input copies retain original relative URLs. Working maps are checked instead.
for p in sorted(R.rglob('*.md')):
    if not included(p) or 'inputs' in p.relative_to(R).parts: continue
    for raw in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8-sig')):
        if '://' in raw or raw.startswith('mailto:'): continue
        target, sep, fragment = raw.partition('#')
        dest = p.parent/unquote(target) if target else p
        # These generated reports are produced by this validator after checks pass.
        if dest.resolve() in {(R/'SHA256SUMS.txt').resolve(), (R/'review/package-checks.json').resolve()}: continue
        if not dest.exists():
            report['markdown_link_failures'].append({'file': str(p.relative_to(R)), 'target': raw})
        elif sep and fragment and dest.suffix == '.md':
            text = dest.read_text(encoding='utf-8-sig')
            anchors = re.findall(r'id="([^"]+)"', text)
            anchors += [re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in re.findall(r'^#{1,6} +(.+)$', text, re.M)]
            if unquote(fragment) not in anchors:
                report['markdown_link_failures'].append({'file': str(p.relative_to(R)), 'target': raw})
assert not report['markdown_link_failures'], report['markdown_link_failures']
report['status'] = 'PASS'
(R/'review/package-checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
files = sorted(p for p in R.rglob('*') if included(p) and p.name != 'SHA256SUMS.txt')
(R/'SHA256SUMS.txt').write_text(''.join(f'{digest(p)}  {p.relative_to(R).as_posix()}\n' for p in files), encoding='utf-8')
print(json.dumps({'status': 'PASS', 'assets': 6, 'exports': 18, 'sealed_files': len(files), 'canonical_inputs_unchanged': True}))
