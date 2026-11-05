"""Behavior tests for the source-bound supplied-dossier adapter."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SPEC = importlib.util.spec_from_file_location('supplied_adapter', HERE / 'adapter.py')


class AdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (HERE / 'adapter.py').exists():
            cls.adapter = None
            return
        cls.adapter = importlib.util.module_from_spec(SPEC)
        SPEC.loader.exec_module(cls.adapter)
        cls.index = cls.adapter.build_index(ROOT)

    def setUp(self):
        self.assertIsNotNone(self.adapter, 'source adapter implementation is missing')

    def test_source_allocation_matches_occurrences_and_unique_documents(self):
        for lane, occurrences, documents in [('scout', 20, 18), ('opeh', 21, 20)]:
            self.assertEqual(sum(x['dossier_id'] == lane for x in self.index['occurrences']), occurrences)
            self.assertEqual(sum(x['dossier_id'] == lane for x in self.index['documents']), documents)

    def test_all_acceptance_records_have_one_explicit_disposition(self):
        for collection, total in [('profile_assertions',47),('findings',26),('calculations',129),('profile_financial_links',42),('discrepancies',40)]:
            canonical = {json.loads(line)['id'] for line in (ROOT / 'analysis/bleich-profile-financial/data' / (collection + '.jsonl')).read_text().splitlines()}
            dispositions = [x for x in self.index['dispositions'] if x['collection'] == collection]
            self.assertEqual(len(dispositions), total)
            self.assertEqual({x['id'] for x in dispositions}, canonical)

    def test_expected_mixed_statements_stay_deferred(self):
        deferred = [r for r in self.index['records'] if r['dossier_id'] == 'deferred']
        self.assertEqual(len(deferred), 6)
        self.assertIn('prof-secondary-current-role', {r['id'] for r in deferred})
        self.assertTrue(all(r['appendix_only'] for r in deferred))

    def test_financial_results_are_joined_without_changing_canonical_fields(self):
        rows = {r['id']:r for r in self.index['records']}
        for lane, count in [('scout',104),('opeh',25)]:
            calculations = [r for r in rows.values() if r['collection']=='calculations' and r['dossier_id']==lane]
            self.assertEqual(len(calculations),count)
            for calc in calculations:
                self.assertEqual(calc['evaluation']['id'], calc['id'])
                self.assertIn('exact_result',calc['evaluation'])
        self.assertEqual(rows['calc-scout-2011-common-sector-total']['evaluation']['residual'],'-1')

    def test_dependencies_close_within_source_lane(self):
        rows={r['id']:r for r in self.index['records']}
        for record in rows.values():
            for dependency in record['dependencies']:
                self.assertIn(dependency,rows)
                if record['dossier_id']!='deferred':
                    self.assertEqual(rows[dependency]['dossier_id'],record['dossier_id'],(record['id'],dependency))
        calc=rows['calc-opeh-per-diem']
        self.assertIn('norm-b1-34-35',calc['dependencies'])
        self.assertNotIn('ent-opeh',calc['dependencies'])

    def test_literal_zero_targets_are_values_and_source_targets_are_edges(self):
        calculations=[r for r in self.index['records'] if r['collection']=='calculations']
        zeros=[r for r in calculations if r['comparison_basis']=='literal_zero']
        self.assertEqual(len(zeros),5)
        for row in zeros:
            self.assertEqual(row['comparison_target'],'0')
            self.assertNotIn('0',row['dependencies'])
        for row in calculations:
            if row['comparison_basis']=='normalized_source':
                self.assertIn(row['comparison_target'],row['dependencies'])

    def test_canonical_fields_are_preserved_and_aliases_are_explicit(self):
        records={r['id']:r for r in self.index['records']}
        for collection in ['calculations','findings','profile_assertions','profile_financial_links','discrepancies']:
            for canonical in map(json.loads,(ROOT/'analysis/bleich-profile-financial/data'/(collection+'.jsonl')).read_text().splitlines()):
                for key,value in canonical.items():self.assertEqual(records[canonical['id']][key],value)
        self.assertEqual(records['oblfam-opeh-jan2018']['canonical_provenance']['aliases'],['analysis/bleich-profile-financial/data/obligations-opeh.jsonl'])

    def test_shared_entities_are_scoped_without_cross_source_citations(self):
        docs={x['id']:x['dossier_id'] for x in self.index['documents']}
        entities=[r for r in self.index['records'] if r.get('canonical_id')=='ent-scout']
        self.assertEqual({r['dossier_id'] for r in entities},{'scout','opeh'})
        for r in entities:
            self.assertTrue(r['appendix_only'])
            self.assertTrue(all(docs[c[4:].split('#')[0]]==r['dossier_id'] for c in r['source_citations']))
            self.assertIn('canonical_record',r)

    def test_mixed_entity_identifiers_never_become_operational_lane_facts(self):
        records={r['id']:r for r in self.index['records']}
        for canonical_id, expected in [('ent-scout',{'CRD':'151990'}),('ent-ophir-partners-llc',{'CRD':'164729','SEC':'801-77121'})]:
            for lane in ['scout','opeh']:
                row=records[canonical_id+'--'+lane]
                self.assertEqual(row.get('identifiers',{}),{},row['id'])
                self.assertEqual(row['canonical_record']['identifiers'],expected)
                visible={key:value for key,value in row.items() if key!='canonical_record'}
                for identifier in expected.values():
                    self.assertNotIn(identifier,json.dumps(visible,sort_keys=True),row['id'])

    def test_mixed_entity_projection_contains_no_original_analytical_prose(self):
        safe_fields={'id','record_type','canonical_name','entity_type','identifiers',
                     'source_citations','supporting_record_ids','source_mention_ids',
                     'dossier_id','collection','canonical_id','canonical_provenance',
                     'dependencies','dependency_edges','evaluation','appendix_only',
                     'canonical_record','scope_note','metadata_references','evidentiary_status'}
        scoped=[r for r in self.index['records'] if 'canonical_record' in r]
        self.assertEqual(len(scoped),12)
        originals={r['id']:r for r in map(json.loads,(ROOT/'analysis/bleich-profile-financial/data/entities.jsonl').read_text().splitlines())}
        for row in scoped:
            self.assertLessEqual(set(row),safe_fields,row['id'])
            self.assertEqual(row['canonical_record'],originals[row['canonical_id']])
            self.assertEqual(row['metadata_references'],{})
            self.assertEqual(row['evidentiary_status'],'indexing_metadata_only')
            self.assertIn('indexing labels',row['scope_note'])
            self.assertIn('identity joins',row['scope_note'])

    def test_raw_entity_mentions_are_not_silently_omitted(self):
        raw={json.loads(s)['id'] for s in (ROOT/'corpus/analysis/entities.jsonl').read_text().splitlines()}
        supplied={r.get('canonical_id',r['id']) for r in self.index['records'] if r['collection']=='corpus-entities'}
        self.assertEqual(raw,supplied)

    def test_secondary_and_peripheral_source_classification(self):
        docs={x['id']:x for x in self.index['documents']}
        self.assertTrue(docs['bee45b687c95d8daa1b49efe316cac13e0690cbe72ccfcce0b5814eb66c5c728']['secondary'])
        self.assertTrue(docs['254c7a178054b538fb51405d1cc65673261c8966331bc0fdf06ecf1bbd71ab08']['appendix_only'])

    def test_missing_citation_is_rejected(self):
        changed=copy.deepcopy(self.index)
        next(r for r in changed['records'] if r['collection']=='findings')['source_citations']=[]
        with self.assertRaisesRegex(ValueError,'citation'):
            self.adapter.validate_index(changed,ROOT)

    def test_wrong_lane_is_rejected(self):
        changed=copy.deepcopy(self.index)
        next(r for r in changed['records'] if r['collection']=='findings')['dossier_id']='opeh'
        with self.assertRaisesRegex(ValueError,'lane|source|canonical'):
            self.adapter.validate_index(changed,ROOT)

    def test_invalid_physical_page_and_nonpdf_locator_are_rejected(self):
        for locator in ['page=99999','line=1']:
            changed=copy.deepcopy(self.index)
            row=next(r for r in changed['records'] if r['collection']=='findings')
            row['source_citations']=[row['source_citations'][0].split('#')[0]+'#'+locator]
            with self.assertRaisesRegex(ValueError,'page|locator|citation'):
                self.adapter.validate_index(changed,ROOT)

    def test_removed_acceptance_record_is_rejected(self):
        changed=copy.deepcopy(self.index)
        changed['records']=[r for r in changed['records'] if r['id']!='calc-opeh-per-diem']
        with self.assertRaises(ValueError):self.adapter.validate_index(changed,ROOT)

    def test_freeze_checks_added_missing_and_changed_inputs(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'corpus').mkdir();(root/'analysis').mkdir()
            original=root/'corpus/source.txt';original.write_text('immutable')
            output=root/'manifest.json'
            manifest=self.adapter.freeze_inputs(root,output)
            self.assertEqual(manifest,json.loads(output.read_text()))
            self.adapter.verify_inputs(root,manifest)
            original.write_text('changed')
            with self.assertRaisesRegex(ValueError,'hash|changed'):self.adapter.verify_inputs(root,manifest)
            original.write_text('immutable');(root/'analysis/extra.txt').write_text('new')
            with self.assertRaisesRegex(ValueError,'added|set'):self.adapter.verify_inputs(root,manifest)
            (root/'analysis/extra.txt').unlink();original.unlink()
            with self.assertRaisesRegex(ValueError,'missing|set'):self.adapter.verify_inputs(root,manifest)

    def test_build_is_deterministic_and_valid(self):
        self.assertEqual(self.index,self.adapter.build_index(ROOT))
        self.adapter.validate_index(self.index,ROOT)


if __name__=='__main__':unittest.main()
