from processing.json_dict_processing import create_processor


def parse_award_year(raw_year):
    """Преобразует год вручения премии в int или возвращает None."""
    if raw_year is None:
        return None
    try:
        return int(raw_year)
    except (ValueError, TypeError):
        return None


CONFIG_PRIZE = {
    'prize_amount': ['prizeAmount'],
    'prize_amount_adjusted': ['prizeAmountAdjusted'],
    'award_year': (['awardYear'], parse_award_year),
    'category_en': ['category', 'en'],
    'prize_status': ['prizeStatus'],
}

CONFIG_PRIZE_WITH_MOTIVATION = {
    **CONFIG_PRIZE,
    'motivation_en': ['motivation', 'en'],
}


def prize_processor(include_motivation=False):
    """Создает процессор для обработки списка словарей с призами."""
    config = (
        CONFIG_PRIZE_WITH_MOTIVATION
        if include_motivation
        else CONFIG_PRIZE
    )
    return create_processor(config, list_processor=True)
