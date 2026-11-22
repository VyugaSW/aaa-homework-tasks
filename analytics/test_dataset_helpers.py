import unittest

from analytics.aggregations import compute_mean
from analytics.dataset_helpers import (
    apply_aggregation_to_groups,
    compute_missing_ratios,
    count_missing_values,
    filter_dataset,
    group_by_attributes,
)


class TestDatasetHelpers(unittest.TestCase):
    """Тесты для фильтрации, группировки, агрегаций и подсчета пропусков."""

    def setUp(self):
        self.sample_data = [
            {'name': 'Alice', 'country': 'USA', 'age': 25},
            {'name': 'Bob', 'country': 'UK', 'age': 30},
            {'name': 'Charlie', 'country': 'USA', 'age': 25},
            {'name': 'Diana', 'country': 'USA', 'age': 35},
        ]

    def test_filter_dataset(self):
        filtered = filter_dataset(
            self.sample_data,
            {
                'country': 'USA',
                'age': lambda val: val is not None and val > 25,
            },
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['name'], 'Diana')

    def test_group_by_attributes(self):
        grouped = group_by_attributes(self.sample_data, ['country', 'age'])
        self.assertEqual(len(grouped[('USA', 25)]), 2)
        self.assertEqual(len(grouped[('UK', 30)]), 1)
        self.assertEqual(len(grouped[('USA', 35)]), 1)

    def test_group_by_attributes_empty_raises(self):
        with self.assertRaises(ValueError):
            group_by_attributes(self.sample_data, [])

    def test_apply_aggregation_to_groups(self):
        grouped = group_by_attributes(self.sample_data, ['country'])
        by_country = apply_aggregation_to_groups(
            grouped,
            compute_mean,
            field='age',
        )
        self.assertAlmostEqual(by_country[('USA',)], (25 + 25 + 35) / 3)
        self.assertAlmostEqual(by_country[('UK',)], 30.0)

    def test_missing_values_and_ratios(self):
        dirty_data = [
            {'id': '1', 'name': 'Alice', 'country': 'USA'},
            {'id': '2', 'name': None, 'country': ''},
        ]
        self.assertEqual(
            count_missing_values(dirty_data),
            {'id': 0, 'name': 1, 'country': 1},
        )
        self.assertEqual(
            compute_missing_ratios(dirty_data),
            {'id': 0.0, 'name': 0.5, 'country': 0.5},
        )
        self.assertEqual(compute_missing_ratios([]), {})


if __name__ == '__main__':
    unittest.main()
