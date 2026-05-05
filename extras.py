import re


def normalize_string(s: str) -> str:
    # Убираем кавычки (одинарные и двойные)
    s = re.sub(r"[\"']", "", s)
    # Заменяем любые пробелы и запятые на один разделитель (запятую)
    s = re.sub(r"[,\s]+", ",", s.strip())
    # Разбиваем на элементы
    parts = [p for p in s.split(",") if p]
    # Оборачиваем в кавычки
    result = ', '.join(f'{p}' for p in parts)
    return result