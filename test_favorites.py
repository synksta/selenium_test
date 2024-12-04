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


class TestFavorites(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера (например, Firefox)
        print("\n", unittest.TestCase.id(self))
        print("\n", unittest.TestCase.shortDescription(self))
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def test_add_to_favorites_authorized(self):
        """Проверяет функциональность добавления и удаления товаров из избранного.

        Тест выполняет следующие шаги:
        1. Переходит на страницу авторизации и выполняет вход с корректными учетными данными.
        2. Переходит в личный кабинет и удаляет все ранее добавленные товары из избранного.
        3. Добавляет пять новых товаров в избранное.
        4. Переходит в личный кабинет и проверяет, что добавленные товары присутствуют в списке любимых товаров.

        Ожидается, что все добавленные товары будут успешно отображаться в списке избранного после их добавления.
        """

        driver = self.driver

        logging.info("Ожидание появления ссылки на страницу авторизации.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.login"))
        )
        # Вход в личный кабинет
        logging.info("Переход на страницу авторизации.")
        login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
        login_link.click()

        # Заполнение формы авторизации
        email_input = driver.find_element(By.NAME, "USER_LOGIN")
        password_input = driver.find_element(By.NAME, "USER_PASSWORD")

        logging.info("Заполнение формы авторизации.")
        email_input.send_keys(config.AUTH_EMAIL_CORRECT)
        password_input.send_keys(config.AUTH_PASSWORD_CORRECT)

        # Отправка формы
        password_input.send_keys(Keys.RETURN)
        logging.info("Отправка формы авторизации.")

        # Ожидание перехода на главную страницу
        logging.info("Ожидание появления ссылки на главную страницу.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
        )

        logging.info("Переход на главную страницу.")
        driver.find_element(By.CSS_SELECTOR, "[href='/']").click()

        # Переход в личный кабинет и удаление всех любимых товаров
        logging.info("Переход в личный кабинет.")
        driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").click()

        # Переход в любимые товары
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href='/personal/favorites/']")
            )
        )

        logging.info("Переход в любимые товары.")
        driver.find_element(By.CSS_SELECTOR, "a[href='/personal/favorites/']").click()

        # Удаление всех любимых товаров
        while True:
            liked_items = driver.find_elements(By.CSS_SELECTOR, ".product_like.liked")

            if not liked_items:
                break  # Выход из цикла, если список пуст

            product_id = liked_items[0].get_attribute("data-product-id")
            logging.info(f"Удаление блюда с ID {product_id} из избранного.")
            liked_items[0].click()

            # Ожидание исчезновения элемента после удаления
            WebDriverWait(driver, 10).until(EC.staleness_of(liked_items[0]))

        logging.info("Все блюда из избранного были удалены.")

        # Переход на главную страницу после удаления всех товаров из избранного
        logging.info("Переход на главную страницу.")
        driver.find_element(By.CSS_SELECTOR, "[href='/']").click()

        # Добавление блюд в избранное
        favorite_ids = []

        logging.info("Добавление блюд в избранное.")
        for _ in range(5):  # Добавляем пять блюд в избранное
            product_like = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, ".product_like:not(.liked)")
                )
            )
            product_id = product_like.get_attribute("data-product-id")
            logging.info(f"Добавление блюда с ID {product_id} в избранное.")

            product_like.click()
            favorite_ids.append(product_id)

            # Проверка изменения иконки
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        f"a.product_like.liked[data-product-id='{product_id}']",
                    )
                )
            )
            logging.info(f"Блюдо с ID {product_id} успешно добавлено в избранное.")

        # Переход в личный кабинет для проверки избранного
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/personal/']"))
        )

        logging.info("Переход в личный кабинет.")
        driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").click()

        # Переход в любимые товары
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href='/personal/favorites/']")
            )
        )

        logging.info("Переход в любимые товары.")
        driver.find_element(By.CSS_SELECTOR, "a[href='/personal/favorites/']").click()

        # Проверка наличия добавленных блюд в списке любимых товаров
        for product_id in favorite_ids:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, f"a.product_like[data-product-id='{product_id}']")
                )
            )
            logging.info(
                f"Блюдо с ID {product_id} присутствует в списке любимых товаров."
            )

            # Утверждение о наличии блюда в списке любимых товаров
            self.assertTrue(
                driver.find_elements(
                    By.CSS_SELECTOR, f"a.product_like[data-product-id='{product_id}']"
                ),
                f"Блюдо с ID {product_id} отсутствует в списке любимых товаров.",
            )

    def test_add_to_favorites_non_authorized(self):
        """Проверяет возможность добавления товара в избранное без авторизации.

        Тест выполняет следующие шаги:
        1. Ожидает появления карточек товаров на странице.
        2. Находит первый неактивированный переключатель "Мне нравится".
        3. Кликает на переключатель и ожидает изменения его состояния.
        4. Проверяет, что товар успешно добавлен в избранное.

        Ожидается, что товар будет добавлен в избранное даже без авторизации.
        """

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

    @unittest.skip("Skipped")
    def test_remove_from_favorites_non_authorized(self):
        """Проверяет возможность удаления товара из избранного без авторизации.

        Тест выполняет следующие шаги:
        1. Ожидает появления карточек товаров на странице.
        2. Находит первый неактивированный переключатель "Мне нравится" и добавляет товар в избранное.
        3. Удаляет добавленный товар из избранного, кликнув по переключателю.
        4. Проверяет, что товар успешно удален из избранного.

        Ожидается, что товар будет успешно удален из избранного даже без авторизации.
        """

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
