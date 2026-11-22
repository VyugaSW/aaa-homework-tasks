import unittest

from analytics.atribute_manager import add_attributes


class TestAtributeManager(unittest.TestCase):
    """Тесты для добавления вычисляемых полей датасета."""

    def setUp(self):
        self.records = [
            {'name': 'Alice', 'birth_year': 1950, 'award_year': 2000},
            {'name': 'Bob', 'birth_year': 1960, 'award_year': 2005},
        ]

    def test_add_attributes_non_mutating_and_chained(self):
        updated = add_attributes(
            self.records,
            {
                'age': lambda row: row['award_year'] - row['birth_year'],
                'is_over_48': lambda row: row['age'] > 48,
            },
        )
        self.assertEqual(updated[0]['age'], 50)
        self.assertTrue(updated[0]['is_over_48'])
        self.assertFalse(updated[1]['is_over_48'])
        self.assertNotIn('age', self.records[0])


if __name__ == '__main__':
    unittest.main()
