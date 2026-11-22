import unittest

from processing.json_dict_processing import (
    create_processor,
    extract_nested_value,
    process_dictionary_with_config,
    process_list_of_dicts_with_config,
)


class TestJsonDictProcessing(unittest.TestCase):
    """Тесты для извлечения значений и обработки словарей по конфигу."""

    def test_extract_nested_value_existing_path(self):
        data = {'a': {'b': {'c': 42}}}
        self.assertEqual(extract_nested_value(data, ['a', 'b', 'c']), 42)

    def test_extract_nested_value_missing_key(self):
        data = {'a': {'b': 1}}
        self.assertIsNone(extract_nested_value(data, ['a', 'x', 'y']))

    def test_extract_nested_value_non_dict_intermediate(self):
        data = {'a': 'not_a_dict'}
        self.assertIsNone(extract_nested_value(data, ['a', 'b']))

    def test_process_dictionary_with_config(self):
        record = {
            'id': '745',
            'knownName': {'en': 'A. Michael Spence'},
            'year': '2001',
        }
        config = {
            'id': ['id'],
            'name': ['knownName', 'en'],
            'year_int': (['year'], int),
            'missing_field': (['absent', 'key'], int),
        }
        expected = {
            'id': '745',
            'name': 'A. Michael Spence',
            'year_int': 2001,
            'missing_field': None,
        }
        self.assertEqual(
            process_dictionary_with_config(record, config),
            expected,
        )

    def test_process_list_of_dicts_with_config(self):
        records = [
            {'awardYear': '1975', 'category': {'en': 'Physics'}},
            {'awardYear': '2001', 'category': {'en': 'Economic Sciences'}},
        ]
        config = {
            'award_year': (['awardYear'], int),
            'category_en': ['category', 'en'],
        }
        expected = [
            {'award_year': 1975, 'category_en': 'Physics'},
            {'award_year': 2001, 'category_en': 'Economic Sciences'},
        ]
        self.assertEqual(
            process_list_of_dicts_with_config(records, config),
            expected,
        )

    def test_process_list_of_dicts_empty(self):
        self.assertEqual(process_list_of_dicts_with_config([], {}), [])

    def test_create_processor_single_and_list(self):
        config = {'value': (['nested', 'val'], int)}
        single_proc = create_processor(config, list_processor=False)
        list_proc = create_processor(config, list_processor=True)

        self.assertEqual(single_proc({'nested': {'val': '7'}}), {'value': 7})
        self.assertEqual(
            list_proc([{'nested': {'val': '7'}}, {'nested': {'val': '8'}}]),
            [{'value': 7}, {'value': 8}],
        )


if __name__ == '__main__':
    unittest.main()
