"""Release checks exercise real files and canonical scoped export data."""
import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).with_name('seal_package.py')


class SealTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(MODULE_PATH.exists(), 'release tooling is not implemented')
        spec = importlib.util.spec_from_file_location('seal_package', MODULE_PATH)
        self.release = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.release)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'data').mkdir()
        base = dict(confidence='conditional', attributed_to='@source', flags=['conditional'],
                    assumptions=['identity unproved'], source_citations=['doc:abc#page=2'],
                    identity_capacity='firm only; personal capacity unproved')
        self.index = {'baseline_commit': '40e77bd', 'documents': [
            {'id': 'abc', 'dossier_id': 'scout', 'title': '=source', 'source_path': 'evidence/abc.pdf'},
            {'id': 'def', 'dossier_id': 'opeh', 'title': 'OPEH'}], 'records': [
            dict(base, id='finding', dossier_id='scout', collection='findings', statement='=untrusted'),
            dict(base, id='calc', dossier_id='scout', collection='calculations', status='conditional',
                 evaluation={'display_result': '3.00', 'exact_result': '3', 'status': 'conditional'}),
            dict(base, id='issue', dossier_id='opeh', collection='discrepancies'),
            dict(base, id='mixed', dossier_id='deferred', collection='findings', statement='do not export')]}
        (self.root / 'data/evidence-index.json').write_text(json.dumps(self.index))

    def test_manifest_is_sorted_deterministic_and_covers_package(self):
        (self.root / 'z.txt').write_text('last')
        (self.root / '__pycache__').mkdir()
        (self.root / '__pycache__/ignored.pyc').write_text('volatile')
        first = self.release.seal(self.root)
        self.assertEqual(list(first['files']), sorted(first['files']))
        self.assertIn('z.txt', first['files'])
        self.assertIn('exports/scout/records.jsonl', first['files'])
        self.assertNotIn('audit/release-manifest.json', first['files'])
        self.assertNotIn('audit/release-verification.json', first['files'])
        self.assertNotIn('__pycache__/ignored.pyc', first['files'])
        self.assertEqual(first, self.release.seal(self.root))
        self.release.verify(self.root)

    def test_verification_rejects_tamper_missing_and_unexpected(self):
        for operation in ('tamper', 'missing', 'unexpected'):
            with self.subTest(operation=operation):
                self.release.seal(self.root)
                target = self.root / 'exports/scout/records.jsonl'
                if operation == 'tamper': target.write_text('changed')
                elif operation == 'missing': target.unlink()
                else: (self.root / 'unexpected').write_text('extra')
                with self.assertRaises(ValueError): self.release.verify(self.root)
                if operation == 'unexpected': (self.root / 'unexpected').unlink()

    def test_exports_keep_raw_values_qualifiers_and_scoped_records(self):
        self.release.export_index(self.root, self.index)
        records = [json.loads(line) for line in (self.root / 'exports/scout/records.jsonl').read_text().splitlines()]
        self.assertEqual(records, [r for r in self.index['records'] if r['dossier_id'] == 'scout'])
        with (self.root / 'exports/scout/financial_findings.csv').open(newline='') as handle:
            finding = next(csv.DictReader(handle))
        self.assertEqual(finding['statement'], "'=untrusted")
        self.assertEqual(finding['attributed_to'], "'@source")
        self.assertEqual(finding['identity_capacity'], 'firm only; personal capacity unproved')
        self.assertEqual(json.loads(finding['assumptions']), ['identity unproved'])
        with (self.root / 'exports/scout/calculations.csv').open(newline='') as handle:
            calc = next(csv.DictReader(handle))
        self.assertEqual((calc['display_result'], calc['exact_result'], calc['status']), ('3.00', '3', 'conditional'))
        self.assertNotIn('mixed', ''.join(p.read_text() for p in (self.root / 'exports').rglob('*') if p.is_file()))
        self.assertFalse((self.root / 'exports/deferred').exists())

    def test_scoped_exports_strip_audit_only_cross_source_original(self):
        audit_original = {'identifiers': {'CRD': 'otherlane-secret'},
                          'statement': 'cross-source prose audit only'}
        for record in self.index['records']:
            record['canonical_record'] = audit_original
        before = json.dumps(self.index, sort_keys=True)
        self.release.export_index(self.root, self.index)
        for path in (self.root / 'exports').rglob('*'):
            if path.is_file():
                with self.subTest(path=path.name):
                    text = path.read_text()
                    self.assertNotIn('canonical_record', text)
                    self.assertNotIn('otherlane-secret', text)
                    self.assertNotIn('cross-source prose audit only', text)
        self.assertEqual(json.dumps(self.index, sort_keys=True), before)

    def test_seal_preserves_authored_review_and_never_invents_test_evidence(self):
        report = self.root / 'audit/packaging-report.md'
        report.parent.mkdir()
        authored = '# Review\n\nReviewed by a human; evidence pending.\n'
        report.write_text(authored)
        self.release.seal(self.root)
        self.assertEqual(report.read_text(), authored)
        generated = self.root / 'audit/release-export-metadata.json'
        self.assertTrue(generated.is_file())
        metadata = json.loads(generated.read_text())
        self.assertEqual(metadata['record_counts'], {'scout': 2, 'opeh': 1})
        for path in (self.root / 'audit').glob('*'):
            self.assertNotIn('tests passed', path.read_text())
            self.assertNotIn('Tooling verification', path.read_text())

    def test_rejects_symlink_and_manifest_path_escape(self):
        (self.root / 'escape').symlink_to('/etc/hosts')
        with self.assertRaises(ValueError): self.release.seal(self.root)
        (self.root / 'escape').unlink()
        self.release.seal(self.root)
        path = self.root / 'audit/release-manifest.json'
        manifest = json.loads(path.read_text())
        manifest['files']['../outside'] = {'sha256': '0' * 64, 'size': 0}
        path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError): self.release.verify(self.root)


if __name__ == '__main__': unittest.main()
