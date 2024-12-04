import time
import unittest
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPageLoad(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Настройка драйвера браузера Firefox с установкой стратегии загрузки страницы
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = "eager"  # Установка стратегии загрузки на 'eager'
        cls.driver = webdriver.Firefox(options=options)
        cls.driver.set_page_load_timeout(config.TIMEOUT)

    def test_page_load_time_within_timeout(self):
        """Проверяет, что страница загружается в пределах установленного времени.

        Тест выполняет следующие шаги:
        1. Загружает главную страницу.
        2. Ожидает, пока элемент <body> станет доступен.
        3. Измеряет время загрузки страницы.
        4. Проверяет, что время загрузки не превышает заданный таймаут.

        Ожидается, что страница должна загружаться быстро и не превышать установленное время ожидания.
        """

        start_time = time.time()

        try:
            self.driver.get(config.MAIN_URL)  # Замените на нужный URL
            WebDriverWait(self.driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except Exception as e:
            self.fail(f"Ошибка при загрузке страницы: {str(e)}")

        load_time = time.time() - start_time
        print(f"Время загрузки страницы: {load_time:.2f} секунд")

        # Проверка на время загрузки страницы
        if load_time > config.TIMEOUT:
            self.fail("Тест не выполнен: страница загружается слишком долго!")

        self.assertLess(
            load_time, config.TIMEOUT, "Страница загружается слишком долго!"
        )

    def test_images_load_within_timeout(self):
        """Проверяет, что все изображения на странице загружаются в пределах установленного времени.

        Тест выполняет следующие шаги:
        1. Загружает главную страницу.
        2. Ожидает, пока все изображения на странице станут доступными.
        3. Проверяет, что каждое изображение загружено полностью.
        4. Измеряет время загрузки контента и проверяет, что оно не превышает заданный таймаут.

        Ожидается, что все изображения должны успешно загружаться и отображаться на странице в рамках установленного времени ожидания.
        """

        start_time = time.time()

        try:
            self.driver.get(config.MAIN_URL)  # Замените на нужный URL

            WebDriverWait(self.driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )

            images = self.driver.find_elements(By.TAG_NAME, "img")
            all_images_loaded = True

            for image in images:
                if image.get_attribute("complete") == "false":
                    all_images_loaded = False
                    break

            load_time = time.time() - start_time
            print(f"Время загрузки контента: {load_time:.2f} секунд")

            # Проверка на время загрузки контента
            if load_time > config.TIMEOUT:
                self.fail("Тест не выполнен: контент загружается слишком долго!")

            # Проверка на загрузку всех изображений
            self.assertTrue(all_images_loaded, "Некоторые изображения не загрузились!")

        except Exception as e:
            self.fail(f"Ошибка при ожидании загрузки изображений: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()
