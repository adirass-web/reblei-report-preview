"""Behavioral tests for a tiny, source-scoped reader fixture."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent

class ReaderTests(unittest.TestCase):
    def test_scoped_records_preserve_qualifications_and_link_original_ids(self):
        module = HERE / 'build_front.py'
        self.assertTrue(module.exists(), 'reader builder is missing')
        spec = importlib.util.spec_from_file_location('build_front', module)
        front = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(front)
        records = [dict(id='finding-one', dossier_id='scout', collection='findings', statement='Qualified finding', confidence='uncertain', assumptions=['only if'], source_citations=[], dependencies=[], evaluation={'value':'12.3400'}), dict(id='mixed-one', dossier_id='deferred', collection='assertions', statement='DO NOT PUBLISH COMBINED', source_citations=[], dependencies=[])]
        html = front.records_page(records, 'scout')
        self.assertIn('id="finding-one"', html)
        self.assertIn('uncertain', html)
        self.assertIn('only if', html)
        self.assertIn('12.3400', html)
        self.assertNotIn('DO NOT PUBLISH COMBINED', html)

    def test_authored_active_html_rejected(self):
        module = HERE / 'build_front.py'
        self.assertTrue(module.exists(), 'reader builder is missing')
        spec = importlib.util.spec_from_file_location('build_front', module)
        front = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(front)
        with self.assertRaises(ValueError):
            front.render_markdown('<script>alert(1)</script>', 'scout', [], [])

    def test_unsafe_link_is_rejected(self):
        spec = importlib.util.spec_from_file_location('build_front', HERE / 'build_front.py')
        front = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(front)
        with self.assertRaises(ValueError):
            front.render_markdown('[click](javascript:alert(1))', 'scout', [], [])

    def test_reader_index_omits_deferred_statement_and_cross_source_original(self):
        spec = importlib.util.spec_from_file_location('build_front', HERE / 'build_front.py')
        front = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(front)
        index = {'records': [{'id':'mixed', 'dossier_id':'deferred', 'collection':'links', 'statement':'DO NOT PUBLISH'}, {'id':'local', 'dossier_id':'scout', 'canonical_record':{'statement':'CROSS SOURCE'}, 'statement':'local'}], 'dispositions':[{'id':'mixed', 'collection':'links', 'dossier_id':'deferred', 'disposition':'deferred', 'reason':'scope'}]}
        data = str(front.reader_index(index))
        self.assertNotIn('DO NOT PUBLISH', data)
        self.assertNotIn('CROSS SOURCE', data)
        self.assertIn('local', data)
