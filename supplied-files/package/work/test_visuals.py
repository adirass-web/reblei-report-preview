"""Figure contract and semantic rendering checks."""
import json
import tempfile
import unittest
from pathlib import Path
import build_front as front

HERE = Path(__file__).parent

class FigureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.records = [{'id':'s', 'dossier_id':'scout'}, {'id':'o', 'dossier_id':'opeh'}, {'id':'d', 'dossier_id':'deferred'}]
        self.fig = dict(id='scout-one', lane='scout', title='Title', summary='Summary', limitation='Conditional only', section_anchor='section', appendix=False, svg='figures/scout/scout-one.svg', png='figures/scout/scout-one.png', csv='figures/scout/scout-one.csv', json='figures/scout/scout-one.json', table=[{'value':'unknown'}], source_record_ids=['s'], kind='test', legend={'unknown':'#6B7280'}, alt='Alternative')
        for ext in ('svg','png','json','csv'):
            p = self.root / ('figures/scout/scout-one.' + ext); p.parent.mkdir(parents=True, exist_ok=True); p.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>' if ext == 'svg' else 'data')
    def tearDown(self): self.tmp.cleanup()
    def validate(self): return front.validate_figure(self.fig, 'scout', self.records, self.root)
    def test_rejects_wrong_lane_and_deferred_source(self):
        for source in ('o', 'd'):
            self.fig['source_record_ids'] = [source]
            with self.subTest(source=source), self.assertRaises(ValueError): self.validate()
    def test_rejects_missing_figure_file(self):
        (self.root / self.fig['svg']).unlink()
        with self.assertRaises(ValueError): self.validate()
    def test_rejects_omitted_qualification(self):
        self.fig['limitation'] = ''
        with self.assertRaises(ValueError): self.validate()
    def test_visible_qualification_and_accessible_data(self):
        self.validate()
        html = front.figure_html(self.fig)
        self.assertIn('Conditional only', html)
        self.assertIn('<table>', html)
        self.assertNotIn('<details', html)
        self.assertIn('Open full-size figure</a>', html)
        self.assertIn('records.html#s', html)

    def test_rejects_external_svg_resources_and_animation(self):
        # Start with a real generated chart, retaining its normal definitions and clipping.
        from shutil import copyfile
        package = HERE.parent / 'presentation'
        fig = json.loads((package / 'figures/scout/manifest.json').read_text())[0]
        index = json.loads((package / 'data/index.json').read_text())
        for ext in ('svg', 'png', 'csv', 'json'):
            target = self.root / fig[ext]
            target.parent.mkdir(parents=True, exist_ok=True)
            copyfile(package / fig[ext], target)
        svg = self.root / fig['svg']
        original = svg.read_text()
        cases = {
            'import': '<style>@import url(https://example.com/a.css);</style>',
            'font-face': '<style>@font-face {font-family:x; src:url(https://example.com/a.woff)}</style>',
            'style-child-tail': '<style>*{stroke-linejoin: round; stroke-linecap: butt}<g/>@font-face{font-family:foo;src:url(http://127.0.0.1:8923/font.woff)}text{font-family:foo}</style><text>test</text>',
            'animation': '<set attributeName="href" to="https://example.com"/>',
            'stylesheet-pi': '<?xml-stylesheet href="https://example.com/a.css" type="text/css"?>',
        }
        svg.write_text(original.replace('<svg ', '<svg style="background-image:image-set(&quot;http://127.0.0.1:8923/bg.png&quot; 1x)" ', 1))
        with self.assertRaises(ValueError): front.validate_figure(fig, 'scout', index['records'], self.root)
        svg.write_bytes(original.replace('encoding="utf-8"', 'encoding="utf-16"').replace('</svg>', cases['stylesheet-pi'] + '</svg>').encode('utf-16'))
        with self.assertRaises(ValueError): front.validate_figure(fig, 'scout', index['records'], self.root)
        for label, payload in cases.items():
            svg.write_text(original.replace('</svg>', payload + '</svg>'))
            with self.subTest(label=label), self.assertRaises(ValueError):
                front.validate_figure(fig, 'scout', index['records'], self.root)

    def test_all_generated_figures_validate(self):
        package = HERE.parent / 'presentation'
        index = json.loads((package / 'data/index.json').read_text())
        self.assertEqual(sum(map(len, front.load_figures(package, index).values())), 15)

    def test_financial_table_has_labeled_classes(self):
        html = front.render_markdown('| Year | Total assets | Total liabilities | Members\' capital |\n| --- | --- | --- | --- |\n| 2009 | 1 | 2 | 3 |', 'scout', [], [])
        for cls in ('financial-assets', 'financial-liabilities', 'financial-equity'):
            self.assertIn(cls, html)
        self.assertIn('Financial category legend', html)
