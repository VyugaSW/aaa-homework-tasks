import unittest

from configs.prizes_configs import parse_award_year, prize_processor


class TestPrizesConfigs(unittest.TestCase):
    """Тесты для парсинга года награждения и процессора призов."""

    def test_parse_award_year(self):
        self.assertEqual(parse_award_year('2001'), 2001)
        self.assertEqual(parse_award_year(1975), 1975)
        self.assertIsNone(parse_award_year(None))
        self.assertIsNone(parse_award_year('invalid'))

    def test_prize_processor_default(self):
        raw_prizes = [
            {
                'prizeAmount': 10000000,
                'prizeAmountAdjusted': 15547541,
                'awardYear': '2001',
                'category': {'en': 'Economic Sciences'},
                'prizeStatus': 'received',
                'motivation': {'en': 'for their analyses of markets'},
            }
        ]
        result = prize_processor()(raw_prizes)
        expected = [
            {
                'prize_amount': 10000000,
                'prize_amount_adjusted': 15547541,
                'award_year': 2001,
                'category_en': 'Economic Sciences',
                'prize_status': 'received',
            }
        ]
        self.assertEqual(result, expected)

    def test_prize_processor_with_motivation(self):
        raw_prizes = [
            {
                'prizeAmount': 630000,
                'prizeAmountAdjusted': 4304697,
                'awardYear': '1975',
                'category': {'en': 'Physics'},
                'prizeStatus': 'received',
                'motivation': {'en': 'for the discovery of the connection'},
            }
        ]
        result = prize_processor(include_motivation=True)(raw_prizes)
        self.assertEqual(
            result[0]['motivation_en'],
            'for the discovery of the connection',
        )


if __name__ == '__main__':
    unittest.main()
