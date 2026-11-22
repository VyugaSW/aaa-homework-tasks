def add_attributes(data, attributes_map):
    """Последовательно добавляет вычисляемые поля в копии записей."""
    current_data = [dict(record) for record in data]
    for field_name, value_func in attributes_map.items():
        for record in current_data:
            record[field_name] = value_func(record)
    return current_data
