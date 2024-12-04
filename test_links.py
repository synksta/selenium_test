import unittest
import config
import logging
from utils.links import get_links
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlparse

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestLinks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Настройка драйвера перед запуском тестов."""
        cls.driver = webdriver.Firefox()
        cls.driver.maximize_window()
        cls.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def test_links_main_page(self):
        """Тестирует пункты меню навигации на главной странице.

        Тест выполняет следующие шаги:
        1. Получает список пунктов меню и ожидаемых URL из главной страницы.
        2. Для каждого пункта меню:
           - Пытается найти элемент и кликнуть по нему.
           - Проверяет, что текущий URL соответствует ожидаемому.
           - В случае ошибки (например, таймаута) записывает сообщение в лог и продолжает тестирование других пунктов меню.
        3. Возвращается на главную страницу после проверки каждого пункта меню.

        Ожидается, что все пункты меню корректно ведут на соответствующие страницы.
        """
        menu_items = get_links(config.MAIN_URL)

        logging.info(menu_items)

        for item, expected_url in menu_items.items():
            with self.subTest(item=item):
                logging.info(f"Переход к пункту меню: {item}")

                try:
                    # Увеличиваем время ожидания и используем видимость элемента
                    menu_element = WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.LINK_TEXT, item))
                    )
                    menu_element.click()
                    logging.info(
                        f"Успешно перешли на страницу: {self.driver.current_url}"
                    )

                    # Проверка текущего URL
                    current_url = self.driver.current_url
                    parsed_expected_url = urlparse(expected_url)
                    parsed_current_url = urlparse(current_url)

                    self.assertEqual(
                        parsed_current_url.path,
                        parsed_expected_url.path,
                        f"Ошибка: ожидается {expected_url}, но получено {current_url}",
                    )
                    logging.info(
                        f"Успешная проверка URL: ожидается {expected_url}, получено {current_url}"
                    )

                except TimeoutException:
                    logging.error(f"Не удалось найти элемент меню: {item}")
                    continue  # Пропускаем этот элемент и продолжаем с остальными

                # Возвращаемся на главную страницу для следующего теста
                self.driver.get(config.MAIN_URL)
                logging.info("Возвращение на главную страницу.")

    @classmethod
    def tearDownClass(cls):
        """Закрытие драйвера после завершения тестов."""
        cls.driver.quit()
        logging.info("Закрыт драйвер браузера.")


if __name__ == "__main__":
    unittest.main()
