import re


def parse_phone_number(phone):
    # Удаляем все символы, кроме цифр
    cleaned = re.sub(r"\D", "", phone)

    # Проверяем, начинается ли номер с '7' или '8' и убираем их
    if cleaned.startswith("7"):
        cleaned = cleaned[1:]
    elif cleaned.startswith("8"):
        cleaned = cleaned[1:]

    return cleaned
