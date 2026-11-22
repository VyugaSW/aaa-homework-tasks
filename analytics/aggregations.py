from collections import Counter


def _extract_numeric_values(data, field):
    """Извлекает числовые (не None и не bool) значения указанного поля."""
    values = []
    for record in data:
        value = record.get(field)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            values.append(float(value))
    return values


def compute_count(data, field=None):
    """Считает число записей или непустых значений в указанном поле."""
    if field is None:
        return len(data)
    return sum(1 for record in data if record.get(field) is not None)


def compute_mean(data, field):
    """Вычисляет среднее арифметическое по числовому полю."""
    values = _extract_numeric_values(data, field)
    if not values:
        return None
    return sum(values) / len(values)


def compute_median(data, field):
    """Вычисляет медиану по числовому полю."""
    values = sorted(_extract_numeric_values(data, field))
    count = len(values)
    if count == 0:
        return None
    mid = count // 2
    if count % 2 == 1:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def compute_min(data, field):
    """Находит минимальное значение по числовому полю."""
    values = _extract_numeric_values(data, field)
    return min(values) if values else None


def compute_max(data, field):
    """Находит максимальное значение по числовому полю."""
    values = _extract_numeric_values(data, field)
    return max(values) if values else None


def get_top_n(data, field, top_n=5, reverse=True):
    """Возвращает топ-N записей, отсортированных по указанному полю."""
    valid_records = [
        record for record in data if record.get(field) is not None
    ]
    sorted_records = sorted(
        valid_records,
        key=lambda item: item[field],
        reverse=reverse,
    )
    return sorted_records[:top_n]


def count_by_value(data, field, top_n=None):
    """Подсчитывает частоты непустых значений в указанном поле."""
    counter = Counter(
        record[field]
        for record in data
        if record.get(field) is not None
    )
    return counter.most_common(top_n)
