from configs.prizes_configs import prize_processor
from processing.json_dict_processing import create_processor


def process_year(year_string):
    """Извлекает год как целое число из строки формата 'YYYY-MM-DD'."""
    if not isinstance(year_string, str) or not year_string.strip():
        return None
    year_part = year_string.strip().split('-')[0]
    try:
        year_int = int(year_part)
        return year_int if year_int > 0 else None
    except ValueError:
        return None


def _build_person_config(include_motivation=False):
    """Собирает словарь-конфиг для лауреатов-людей."""
    return {
        'id': ['id'],
        'name': ['knownName', 'en'],
        'gender': ['gender'],
        'birth_year': (['birth', 'date'], process_year),
        'country_birth': ['birth', 'place', 'country', 'en'],
        'country_now': ['birth', 'place', 'countryNow', 'en'],
        'prizes_relevant': (
            ['nobelPrizes'],
            prize_processor(include_motivation=include_motivation),
        ),
    }


def _build_org_config(include_motivation=False):
    """Собирает словарь-конфиг для лауреатов-организаций."""
    return {
        'id': ['id'],
        'name': ['orgName', 'en'],
        'founded_year': (['founded', 'date'], process_year),
        'country_founded': ['founded', 'place', 'country', 'en'],
        'country_now': ['founded', 'place', 'countryNow', 'en'],
        'prizes_relevant': (
            ['nobelPrizes'],
            prize_processor(include_motivation=include_motivation),
        ),
    }


CONFIG_PERSON = _build_person_config(include_motivation=False)
CONFIG_ORG = _build_org_config(include_motivation=False)


def person_processor(include_motivation=False):
    """Создает процессор для обработки словарей о людях-лауреатах."""
    config = (
        _build_person_config(include_motivation=True)
        if include_motivation
        else CONFIG_PERSON
    )
    return create_processor(config, list_processor=False)


def org_processor(include_motivation=False):
    """Создает процессор для обработки словарей об организациях."""
    config = (
        _build_org_config(include_motivation=True)
        if include_motivation
        else CONFIG_ORG
    )
    return create_processor(config, list_processor=False)


process_persons = person_processor()
process_orgs = org_processor()
