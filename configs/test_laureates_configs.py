import unittest

from configs.laureates_configs import (
    org_processor,
    person_processor,
    process_orgs,
    process_persons,
    process_year,
)


class TestLaureatesConfigs(unittest.TestCase):
    """Тесты для process_year, person_processor и org_processor."""

    def test_process_year(self):
        self.assertEqual(process_year('1943-11-07'), 1943)
        self.assertEqual(process_year('1922-00-00'), 1922)
        self.assertEqual(process_year('1901'), 1901)
        self.assertIsNone(process_year('0000-00-00'))
        self.assertIsNone(process_year(''))
        self.assertIsNone(process_year(None))
        self.assertIsNone(process_year('unknown'))

    def test_person_processor(self):
        raw_person = {
            'id': '745',
            'knownName': {'en': 'A. Michael Spence'},
            'gender': 'male',
            'birth': {
                'date': '1943-11-07',
                'place': {
                    'country': {'en': 'USA'},
                    'countryNow': {'en': 'USA'},
                },
            },
            'nobelPrizes': [
                {
                    'prizeAmount': 10000000,
                    'prizeAmountAdjusted': 15547541,
                    'awardYear': '2001',
                    'category': {'en': 'Economic Sciences'},
                    'prizeStatus': 'received',
                }
            ],
        }
        expected = {
            'id': '745',
            'name': 'A. Michael Spence',
            'gender': 'male',
            'birth_year': 1943,
            'country_birth': 'USA',
            'country_now': 'USA',
            'prizes_relevant': [
                {
                    'prize_amount': 10000000,
                    'prize_amount_adjusted': 15547541,
                    'award_year': 2001,
                    'category_en': 'Economic Sciences',
                    'prize_status': 'received',
                }
            ],
        }
        self.assertEqual(person_processor()(raw_person), expected)
        self.assertEqual(process_persons(raw_person), expected)

    def test_org_processor(self):
        raw_org = {
            'id': '482',
            'orgName': {'en': 'International Committee of the Red Cross'},
            'founded': {
                'date': '1863-00-00',
                'place': {
                    'country': {'en': 'Switzerland'},
                    'countryNow': {'en': 'Switzerland'},
                },
            },
            'nobelPrizes': [
                {
                    'prizeAmount': 133823,
                    'prizeAmountAdjusted': 4000000,
                    'awardYear': '1917',
                    'category': {'en': 'Peace'},
                    'prizeStatus': 'received',
                }
            ],
        }
        result = org_processor()(raw_org)
        self.assertEqual(result['id'], '482')
        self.assertEqual(
            result['name'],
            'International Committee of the Red Cross',
        )
        self.assertEqual(result['founded_year'], 1863)
        self.assertEqual(result['country_founded'], 'Switzerland')
        self.assertEqual(result['country_now'], 'Switzerland')
        self.assertEqual(len(result['prizes_relevant']), 1)
        self.assertEqual(process_orgs(raw_org), result)


if __name__ == '__main__':
    unittest.main()
