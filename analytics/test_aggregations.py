import unittest

from analytics.aggregations import (
    compute_count,
    compute_max,
    compute_mean,
    compute_median,
    compute_min,
    count_by_value,
    get_top_n,
)


class TestAggregations(unittest.TestCase):
    """Тесты для статистических агрегаций и выбора топ-N записей."""

    def setUp(self):
        self.records = [
            {'name': 'Alice', 'country': 'USA', 'age': 20},
            {'name': 'Bob', 'country': 'UK', 'age': 30},
            {'name': 'Charlie', 'country': 'USA', 'age': 70},
            {'name': 'Unknown', 'country': None, 'age': None},
        ]

    def test_compute_count(self):
        self.assertEqual(compute_count(self.records), 4)
        self.assertEqual(compute_count(self.records, field='age'), 3)

    def test_compute_mean_and_median(self):
        self.assertAlmostEqual(compute_mean(self.records, 'age'), 40.0)
        self.assertAlmostEqual(compute_median(self.records, 'age'), 30.0)
        self.assertIsNone(compute_mean([], 'age'))
        self.assertIsNone(compute_median([], 'age'))

    def test_compute_median_even_count(self):
        even_records = [{'age': 10}, {'age': 40}, {'age': 20}, {'age': 30}]
        self.assertAlmostEqual(compute_median(even_records, 'age'), 25.0)

    def test_compute_min_and_max(self):
        self.assertEqual(compute_min(self.records, 'age'), 20.0)
        self.assertEqual(compute_max(self.records, 'age'), 70.0)
        self.assertIsNone(compute_min([], 'age'))
        self.assertIsNone(compute_max([], 'age'))

    def test_get_top_n(self):
        top_two = get_top_n(self.records, 'age', top_n=2, reverse=True)
        self.assertEqual([r['name'] for r in top_two], ['Charlie', 'Bob'])

        bottom_one = get_top_n(self.records, 'age', top_n=1, reverse=False)
        self.assertEqual(bottom_one[0]['name'], 'Alice')

    def test_count_by_value(self):
        counts = count_by_value(self.records, 'country', top_n=2)
        self.assertEqual(counts, [('USA', 2), ('UK', 1)])


if __name__ == '__main__':
    unittest.main()
