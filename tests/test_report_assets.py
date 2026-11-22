import importlib.util
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

SPEC = importlib.util.spec_from_file_location('report_assets', Path(__file__).resolve().parents[1] / 'report_assets.py')
a = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(a)


def snapshot(rules='first', bodies=3):
    return {'revision': 'a' * 40, 'rules_id': rules,
            'reference': {'url': 'https://example.org/sdk', 'sha256': 'b' * 64},
            'groups': [{'total': 10, 'counts': {'body': bodies, 'partial': 1, 'noop': 1, 'stub': 8 - bodies}}]}


class HistoryTests(unittest.TestCase):
    def test_same_day_replaced_and_regression_preserved(self):
        history = a.update_history(None, snapshot(), '2026-01-01')
        history = a.update_history(history, snapshot(bodies=5), '2026-01-01')
        history = a.update_history(history, snapshot(bodies=2), '2026-01-02')
        points = a.current_series(history)['points']
        self.assertEqual([p['body'] for p in points], [5, 2])
        self.assertEqual([p['total'] for p in points], [10, 10])

    def test_changed_rules_start_separate_series(self):
        old = a.update_history(None, snapshot(), '2026-01-01')
        new = a.update_history(old, snapshot('second'), '2026-01-02')
        self.assertEqual(len(new['series']), 2)
        self.assertEqual(len(a.current_series(new)['points']), 1)
        self.assertEqual(old['current_rules_id'], 'first')

    def test_backfill_does_not_overwrite_observed_day(self):
        point = a.history_point(snapshot(bodies=1), '2026-01-01', 'rescanned')
        history = a.update_history(None, snapshot(), '2026-01-01', [point])
        self.assertEqual(a.current_series(history)['points'][0]['body'], 3)
        self.assertEqual(a.current_series(history)['points'][0]['origin'], 'observed')

    def test_single_and_multiple_point_graphs_are_valid(self):
        history = a.update_history(None, snapshot(), '2026-01-01')
        ET.fromstring(a.render_history(history, 'example/repo'))
        history = a.update_history(history, snapshot(bodies=2), '2026-01-04')
        svg = a.render_history(history, 'example/repo')
        ET.fromstring(svg)
        self.assertIn('2026-01-04', svg)
        self.assertIn('commit/' + 'a' * 40, svg)

    def test_badges_escape_values(self):
        svg = a.badge('A & B', '<none>', '#238636')
        ET.fromstring(svg)
        self.assertNotIn('<none>', svg)

    def test_missing_historical_source_not_zero(self):
        history = a.update_history(None, snapshot(), '2026-01-02', skipped=[
            {'date': '2026-01-01', 'revision': 'c' * 40, 'reason': 'No source interface'}])
        report = a.history_report(history, 'example/repo')
        self.assertIn('not treated as zero', report)
        self.assertIn('No source interface', report)


if __name__ == '__main__':
    unittest.main()
