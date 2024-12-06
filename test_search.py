import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import config
import logging
from selenium.webdriver.common.keys import Keys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestSearch(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def tearDown(self):
        # Закрытие драйвера после завершения теста
        self.driver.quit()
        logging.info("Закрыт веб-драйвер.")

    # @unittest.skip("Skipped")
    def test_presense_of_searchbox(self):
        """
        Тест для проверки наличия и функциональности поля ввода запроса поиска.

        Этот тест выполняет следующие шаги:
        1. Поиск поля ввода запроса поиска на странице.
        2. Проверка, что поле ввода было найдено.
        3. Ввод запроса в поле ввода.
        4. Поиск кнопки отправки запроса.
        5. Проверка, что кнопка отправки была найдена.
        6. Нажатие на кнопку отправки запроса.
        7. Проверка изменения URL после отправки запроса для подтверждения успешного выполнения поиска.

        Проверяемые элементы:
        - Поле ввода запроса поиска (по имени "SEARCH_QUERY").
        - Кнопка отправки запроса (по имени "search").

        Исключения:
        - AssertionError будет вызвано, если поле ввода или кнопка отправки не найдены,
          или если URL не изменился после отправки запроса.

        Логирование:
        В процессе выполнения теста ведется логирование ключевых действий для упрощения отладки.

        Returns:
            None
        """

        driver = self.driver

        current_url = driver.current_url

        # 1. Находим поле ввода запроса поиска
        logging.info("Поиск поля ввода запроса поиска.")
        search_query_box = driver.find_element(By.NAME, "SEARCH_QUERY")
        self.assertTrue(
            search_query_box is not None,
            "Поле ввода запроса поиска не было найдено.",
        )
        logging.info("Поле ввода запроса поиска успешно найдено.")

        # 2. Вводим запрос в поле ввода
        logging.info("Ввод запроса в поле ввода.")
        search_query_box.send_keys(config.SEARCH_QUERY)
        logging.info("Запрос успешно введен в поле ввода.")

        # 3. Поиск кнопки отправки запроса
        logging.info("Поиск кнопки отправки запроса поиска.")
        search_submit_button = driver.find_element(By.NAME, "search")
        self.assertTrue(
            search_submit_button is not None,
            "Кнопка отправки запроса поиска не была найдена.",
        )
        logging.info("Кнопка отправки запроса поиска успешно найдена.")

        # 4. Нажимаем на кнопку отправки запроса
        logging.info("Нажатие кнопки отправки запроса.")
        search_submit_button.click()
        logging.info("Кнопка отправки запроса успешно нажата.")

        # 5. Проверяем наличие результатов поиска
        logging.info("Проверка изменения URL после отправки запроса.")
        # Получаем новый URL
        new_url = driver.current_url

        # Используем assert для проверки, что URL изменился
        self.assertTrue(current_url != new_url, f"URL не изменился: остался {new_url}")

        logging.info("URL успешно изменен.")
        logging.info(f"Старый URL: {current_url}")
        logging.info(f"Новый URL: {new_url}")


if __name__ == "__main__":
    unittest.main()
