import requests
from bs4 import BeautifulSoup
import re

# Регулярные выражения для фильтрации
phone_pattern = re.compile(r"\+?\d[\d\s()-]{5,}\d")  # Шаблон для телефонных номеров
email_pattern = re.compile(
    r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
)  # Шаблон для email


def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links_dict = {}

    for a in soup.find_all("a", href=True):
        link_text = a.get_text(strip=True)  # Получаем текст ссылки
        link_url = a["href"]  # Получаем URL

        # Пропускаем пустые ссылки и ссылки на телефонные номера и email
        if (
            not link_text
            or not link_url
            or "/" not in link_url
            or phone_pattern.search(link_text)
            or email_pattern.search(link_text)
        ):
            continue

        links_dict[link_text] = link_url  # Добавляем в словарь

    return links_dict


def get_visible_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    visible_links_dict = {}

    for a in soup.find_all("a", href=True):
        link_text = a.get_text(strip=True)  # Получаем текст ссылки
        link_url = a["href"]  # Получаем URL

        # Проверяем, является ли ссылка видимой (например, не скрыта через CSS)
        if (
            not link_text
            or not link_url
            or "/" not in link_url
            or phone_pattern.search(link_text)
            or email_pattern.search(link_text)
        ):
            continue

        # Проверяем, что ссылка не скрыта (например, с помощью CSS класса)
        style = a.get("style", "")
        if "display: none" in style or "visibility: hidden" in style:
            continue

        visible_links_dict[link_text] = link_url  # Добавляем в словарь

    return visible_links_dict


if __name__ == "__main__":
    # Пример использования
    url = "https://example.com"  # Замените на нужный URL

    links = get_links(url)
    visible_links = get_visible_links(url)

    # Выводим все ссылки
    print("Все ссылки:")
    for text, link in links.items():
        print(f'"{text}": "{link}"')

    print("\nВидимые ссылки:")
    for text, link in visible_links.items():
        print(f'"{text}": "{link}"')
