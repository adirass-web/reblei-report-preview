#!/usr/bin/env python3
"""Export accepted values, seal the portable package, or verify an existing seal.

Run from anywhere: python work/seal_package.py [--verify]. No source values are
recomputed. The package-root data/evidence-index.json is the canonical input.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import tempfile

LANES = ('scout', 'opeh')
EXCLUDED_DIRS = {'.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache',
                 'node_modules', '.venv', 'venv'}
EXCLUDED_FILES = {'audit/release-manifest.json', 'audit/release-verification.json'}
COMMON_COLUMNS = ['id', 'dossier_id', 'collection', 'statement', 'display_result',
                  'exact_result', 'status', 'evidentiary_status', 'confidence',
                  'attributed_to', 'flags', 'assumptions', 'source_citations']


def _json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def _atomic_write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    if path.is_symlink() or any(p.is_symlink() for p in path.parents if p != root.parent):
        raise ValueError(f'symlink is not a package file: {relative}')
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', newline='',
                                         dir=path.parent, prefix='.seal-', delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary and temporary.exists(): temporary.unlink()


def _files(root: Path) -> dict[str, Path]:
    result = {}
    for directory, dirs, names in os.walk(root, followlinks=False):
        parent = Path(directory)
        for name in sorted(dirs):
            if name not in EXCLUDED_DIRS and (parent / name).is_symlink():
                raise ValueError(f'symlink directory is forbidden: {(parent / name).relative_to(root)}')
        dirs[:] = sorted(name for name in dirs if name not in EXCLUDED_DIRS)
        for name in sorted(names):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink(): raise ValueError(f'symlink file is forbidden: {relative}')
            if not path.is_file(): raise ValueError(f'nonregular package file: {relative}')
            if relative not in EXCLUDED_FILES and not name.endswith(('.pyc', '.pyo')):
                result[relative] = path
    return dict(sorted(result.items()))


def _cell(value: object) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else '' if value is None else str(value)
    # JSONL is raw; only spreadsheet-facing CSV cells receive this prefix.
    return "'" + text if text.startswith(('=', '+', '-', '@')) else text


def _csv(rows: list[dict], common: list[str]) -> str:
    fields = common + sorted({key for row in rows for key in row} - set(common))
    output = io.StringIO(newline='')
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for row in rows: writer.writerow({key: _cell(row.get(key)) for key in fields})
    return output.getvalue()


def export_index(root: Path, index: dict) -> None:
    """Export each source lane without recomputation or mixed-source statements."""
    root = Path(root).resolve()
    _files(root)  # Refuse unsafe existing paths before writing any exports.
    for lane in LANES:
        # canonical_record is the audit-only cross-source original, never lane evidence.
        records = [{key: value for key, value in record.items() if key != 'canonical_record'}
                   for record in index['records'] if record['dossier_id'] == lane]
        raw = ''.join(json.dumps(record, ensure_ascii=False, sort_keys=True) + '\n' for record in records)
        _atomic_write(root, f'exports/{lane}/records.jsonl', raw)
        for filename, collection in [('financial_findings', 'findings'), ('calculations', 'calculations'), ('discrepancies', 'discrepancies')]:
            rows = []
            for record in records:
                if record.get('collection') != collection: continue
                row = dict(record)
                evaluation = record.get('evaluation')
                if isinstance(evaluation, dict):
                    for key in ('display_result', 'exact_result', 'status'):
                        if key in evaluation: row[key] = evaluation[key]
                    # Preserve both record flags/qualifiers and the complete joined evaluation.
                rows.append(row)
            _atomic_write(root, f'exports/{lane}/{filename}.csv', _csv(rows, COMMON_COLUMNS))
        docs = [doc for doc in index['documents'] if doc['dossier_id'] == lane]
        _atomic_write(root, f'exports/{lane}/sourceinventory.csv', _csv(docs, ['id', 'dossier_id', 'title', 'source_path']))


def _digest(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''): digest.update(chunk)
    return {'sha256': digest.hexdigest(), 'size': path.stat().st_size}


def seal(root: Path) -> dict:
    """Generate scoped exports and deterministic hashes of all included files."""
    root = Path(root).resolve()
    _files(root)
    index = json.loads((root / 'data/evidence-index.json').read_text(encoding='utf-8'))
    export_index(root, index)
    counts = {lane: len([r for r in index['records'] if r['dossier_id'] == lane]) for lane in LANES}
    metadata = {
        'schema_version': 1,
        'canonical_input': 'data/evidence-index.json',
        'canonical_input_sha256': _digest(root / 'data/evidence-index.json')['sha256'],
        'record_counts': counts,
        'omitted_audit_only_fields': ['canonical_record'],
        'exports': {relative: _digest(path) for relative, path in _files(root).items()
                    if relative.startswith('exports/')},
    }
    _atomic_write(root, 'audit/release-export-metadata.json', _json(metadata))
    manifest = {'schema_version': 1, 'algorithm': 'sha256',
                'source_input_baseline': index.get('baseline_commit'),
                'reused_presentation_commit': '06031b1',
                'excluded_directories': sorted(EXCLUDED_DIRS),
                'excluded_files': sorted(EXCLUDED_FILES),
                'excluded_suffixes': ['.pyc', '.pyo'],
                'files': {relative: _digest(path) for relative, path in _files(root).items()}}
    _atomic_write(root, 'audit/release-manifest.json', _json(manifest))
    verify(root)
    return manifest


def verify(root: Path) -> dict:
    """Reject modified, missing, or unexpected included package files."""
    root = Path(root).resolve()
    manifest = json.loads((root / 'audit/release-manifest.json').read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 1 or manifest.get('algorithm') != 'sha256':
        raise ValueError('unsupported release manifest')
    expected = manifest['files']
    for name in expected:
        path = PurePosixPath(name)
        if not name or '\\' in name or path.is_absolute() or '..' in path.parts or path.as_posix() != name:
            raise ValueError(f'invalid package-relative manifest path: {name}')
    actual = _files(root)
    if set(actual) != set(expected):
        raise ValueError(f"package file set changed: missing={sorted(set(expected)-set(actual))}; unexpected={sorted(set(actual)-set(expected))}")
    for relative, path in actual.items():
        if _digest(path) != expected[relative]: raise ValueError(f'package hash changed: {relative}')
    result = {'verified': True, 'algorithm': 'sha256', 'file_count': len(actual),
              'manifest_sha256': _digest(root / 'audit/release-manifest.json')['sha256']}
    _atomic_write(root, 'audit/release-verification.json', _json(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify', action='store_true', help='verify existing exports and seal without regeneration')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        result = verify(root) if args.verify else seal(root)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f'Package verification failed: {error}\n')
    print(json.dumps({'verified': True, 'file_count': result.get('file_count', len(result.get('files', {})))}, sort_keys=True))
    return 0


if __name__ == '__main__': raise SystemExit(main())
