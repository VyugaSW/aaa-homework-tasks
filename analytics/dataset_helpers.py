from collections import defaultdict


def filter_dataset(data, conditions):
    """Фильтрует список словарей по точным значениям или предикатам."""
    filtered_records = []
    for record in data:
        matches_all = True
        for field_name, expected in conditions.items():
            actual_value = record.get(field_name)
            if callable(expected):
                if not expected(actual_value):
                    matches_all = False
                    break
            elif actual_value != expected:
                matches_all = False
                break
        if matches_all:
            filtered_records.append(record)
    return filtered_records


def group_by_attributes(data, attributes):
    """Группирует список словарей по набору указанных атрибутов."""
    if not attributes:
        raise ValueError('attributes must be a non empty sequence of keys')
    grouped = defaultdict(list)
    for record in data:
        group_key = tuple(record.get(attr) for attr in attributes)
        grouped[group_key].append(record)
    return dict(grouped)


def apply_aggregation_to_groups(grouped_data, agg_func, *args, **kwargs):
    """Применяет функцию агрегации к каждой группе словарей."""
    return {
        group_key: agg_func(records, *args, **kwargs)
        for group_key, records in grouped_data.items()
    }


def count_missing_values(data):
    """Считает количество пропусков (None или пустых значений) по полям."""
    all_fields = []
    seen_fields = set()
    for record in data:
        for key in record:
            if key not in seen_fields:
                seen_fields.add(key)
                all_fields.append(key)

    missing_counts = {field: 0 for field in all_fields}
    for record in data:
        for field in all_fields:
            value = record.get(field)
            if value is None or value == '' or value == []:
                missing_counts[field] += 1
    return missing_counts


def compute_missing_ratios(data):
    """Вычисляет долю пропусков для каждого поля в датасете."""
    total_records = len(data)
    if total_records == 0:
        return {}
    missing_counts = count_missing_values(data)
    return {
        field: round(count / total_records, 4)
        for field, count in missing_counts.items()
    }
