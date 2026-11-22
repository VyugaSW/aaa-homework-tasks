def extract_nested_value(obj, keys):
    """Извлекает значение из вложенных словарей по цепочке ключей."""
    current = obj
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def process_dictionary_with_config(dictionary, config):
    """Преобразует вложенный словарь в плоский по заданному конфигу."""
    result = {}
    for attribute, spec in config.items():
        if isinstance(spec, tuple):
            path, transform_func = spec
            raw_value = extract_nested_value(dictionary, path)
            result[attribute] = (
                transform_func(raw_value) if raw_value is not None else None
            )
        else:
            result[attribute] = extract_nested_value(dictionary, spec)
    return result


def process_list_of_dicts_with_config(list_of_dicts, config):
    """Обрабатывает список вложенных словарей по заданному конфигу."""
    if not list_of_dicts:
        return []
    return [
        process_dictionary_with_config(item, config)
        for item in list_of_dicts
    ]


def create_processor(config, list_processor=False):
    """Возвращает функцию-процессор с предзагруженным конфигом."""
    def processor(data):
        if list_processor:
            return process_list_of_dicts_with_config(data, config)
        return process_dictionary_with_config(data, config)

    return processor
