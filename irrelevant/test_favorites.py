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

    def test_add_to_favorites(self):
        driver = self.driver

        logging.info("Ожидание появления ссылки на страницу авторизации.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.login"))
        )
        # Вход в личный кабинет
        logging.info("Переход на страницу авторизации.")
        login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
        login_link.click()
        logging.info("Клик по ссылке 'Войти'.")

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
        login_link = driver.find_element(By.CSS_SELECTOR, "[href='/']")
        login_link.click()

        # Переход в личный кабинет и удаление всех любимых товаров
        try:
            logging.info("Переход в личный кабинет.")
            driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").click()

            # Переход в любимые товары
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/personal/favorites/']")
                )
            )
            logging.info("Переход в любимые товары.")
            driver.find_element(
                By.CSS_SELECTOR, "a[href='/personal/favorites/']"
            ).click()

            # Удаление всех любимых товаров с ожиданием загрузки элементов
            while True:
                try:
                    # Ожидание появления всех элементов с классом .product_like.liked в течение 3 секунд
                    WebDriverWait(driver, 3).until(
                        EC.presence_of_all_elements_located(
                            (By.CSS_SELECTOR, ".product_like.liked")
                        )
                    )

                    liked_items = driver.find_elements(
                        By.CSS_SELECTOR, ".product_like.liked"
                    )
                    if not liked_items:
                        logging.info("Все любимые товары удалены.")
                        break

                    # Удаление одного элемента из избранного
                    product_id = liked_items[0].get_attribute("data-product-id")
                    logging.info(f"Удаление блюда с ID {product_id} из избранного.")
                    liked_items[0].click()

                    # Ожидание исчезновения элемента после удаления
                    WebDriverWait(driver, 10).until(EC.staleness_of(liked_items[0]))

                except Exception as e:
                    logging.warning(f"Ошибка при удалении любимых товаров: {e}")
                    break

            # Переход на главную страницу после удаления всех товаров из избранного
            driver.find_element(By.CSS_SELECTOR, "a[href='/']").click()

        except Exception as e:
            logging.error(
                f"Ошибка при переходе в личный кабинет или удалении любимых товаров: {e}"
            )
            self.fail("Не удалось перейти в личный кабинет или удалить любимые товары.")

        # Добавление блюд в избранное
        favorite_ids = []

        for _ in range(5):  # Добавляем пять блюд в избранное
            try:
                product_like = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, ".product_like:not(.liked)")
                    )  # Ищем только не лайкнутые блюда
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
            except Exception as e:
                logging.error(f"Ошибка при добавлении блюда в избранное: {e}")
                self.fail("Не удалось добавить блюдо в избранное.")

        # Переход в личный кабинет для проверки избранного
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/personal/']")
                )
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
            driver.find_element(
                By.CSS_SELECTOR, "a[href='/personal/favorites/']"
            ).click()

            # Проверка наличия добавленных блюд в списке любимых товаров
            for product_id in favorite_ids:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                f"a.product_like[data-product-id='{product_id}']",
                            )
                        )
                    )
                    logging.info(
                        f"Блюдо с ID {product_id} присутствует в списке любимых товаров."
                    )
                except Exception as e:
                    logging.error(
                        f"Блюдо с ID {product_id} не найдено в списке любимых товаров: {e}"
                    )
                    self.fail(
                        f"Блюдо с ID {product_id} отсутствует в списке любимых товаров."
                    )

            logging.info(
                "Все добавленные блюда присутствуют в списке любимых товаров. Тест пройден."
            )

        except Exception as e:
            logging.error(
                f"Ошибка при переходе в личный кабинет или проверке любимых товаров: {e}"
            )
            self.fail(
                "Не удалось перейти в личный кабинет или проверить любимые товары."
            )

    def tearDown(self):
        # Закрытие браузера
        logging.info("Закрытие браузера.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
