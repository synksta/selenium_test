import config
import unittest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestFavoritesFunctionality(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера (например, Firefox)
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def test_add_to_favorites_without_auth(self):
        driver = self.driver

        # Ожидание появления карточек товаров
        logging.info("Ожидание появления карточек товаров.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".product_like:not(.liked)")
            )
        )

        # Нахождение первого неактивированного переключателя "Мне нравится"
        product_like = driver.find_element(By.CSS_SELECTOR, ".product_like:not(.liked)")

        # Получение ID продукта и названия товара
        product_id = product_like.get_attribute("data-product-id")

        logging.info(f"Добавление блюда с ID {product_id} в избранное.")

        # Клик на переключатель "Мне нравится"
        product_like.click()

        # Ожидание изменения состояния переключателя
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    f"a.product_like.liked[data-product-id='{product_id}']",
                )
            )
        )

        # Проверка изменения состояния переключателя
        self.assertTrue(
            driver.find_element(
                By.CSS_SELECTOR, f"a.product_like.liked[data-product-id='{product_id}']"
            ),
            f"Блюдо с ID {product_id} не добавлено в избранное.",
        )
        logging.info(f"Блюдо с ID {product_id} успешно добавлено в избранное.")

    def test_remove_from_favorites_without_auth(self):
        driver = self.driver

        # Ожидание появления карточек товаров
        logging.info("Ожидание появления карточек товаров.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, ".product_like:not(.liked)")
            )
        )

        # Нахождение первого неактивированного переключателя "Мне нравится"
        product_like = driver.find_element(By.CSS_SELECTOR, ".product_like:not(.liked)")

        # Получение ID продукта и названия товара
        product_id = product_like.get_attribute("data-product-id")

        logging.info(f"Добавление блюда с ID {product_id} в избранное перед удалением.")

        # Клик на переключатель "Мне нравится"
        product_like.click()

        # Ожидание изменения состояния переключателя после добавления
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    f"a.product_like.liked[data-product-id='{product_id}']",
                )
            )
        )

        logging.info(f"Блюдо с ID {product_id} успешно добавлено в избранное.")

        # Удаление блюда из избранного
        logging.info(f"Удаление блюда с ID {product_id} из избранного.")

        # Клик на переключатель "Мне нравится" для удаления
        product_like.click()

        # Ожидание изменения состояния переключателя после удаления
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    f"a.product_like[data-product-id='{product_id}']:not(.liked)",
                )
            )
        )

        # Проверка изменения состояния переключателя
        self.assertFalse(
            driver.find_element(
                By.CSS_SELECTOR, f"a.product_like[data-product-id='{product_id}']"
            )
            .get_attribute("class")
            .find("liked")
            != -1,
            f"Блюдо с ID {product_id} не удалено из избранного.",
        )

        logging.info(f"Блюдо с ID {product_id} успешно удалено из избранного.")

    def tearDown(self):
        # Закрытие браузера
        logging.info("Закрытие браузера.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
