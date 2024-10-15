import requests
from bs4 import BeautifulSoup


def get_submenu_links(url, menu_selector, submenu_selector):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Найдите элемент меню
    menu_element = soup.select_one(menu_selector)

    if not menu_element:
        print("Меню не найдено.")
        return []

    # Найдите подменю внутри элемента меню
    submenu_element = menu_element.select_one(submenu_selector)

    if not submenu_element:
        print("Подменю не найдено.")
        return []

    # Извлекаем все ссылки из подменю
    links = submenu_element.find_all("a", href=True)
    links_dict = {link.get_text(strip=True): link["href"] for link in links}

    return links_dict


if __name__ == "__main__":
    url = "https://example.com"  # Замените на нужный URL
    menu_selector = ".menu-class"  # Замените на селектор вашего меню
    submenu_selector = ".submenu-class"  # Замените на селектор вашего подменю

    submenu_links = get_submenu_links(url, menu_selector, submenu_selector)

    # Выводим ссылки из подменю
    for text, link in submenu_links.items():
        print(f'"{text}": "{link}"')
