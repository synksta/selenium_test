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


class TestLogin(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера (например, Firefox)
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def test_successful_login(self):
        driver = self.driver
        logging.info("Переход на страницу авторизации.")

        # Переход на страницу авторизации
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

        # Ожидание перехода на страницу личного кабинета
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/personal/']")
                )  # Селектор для ссылки на личный кабинет
            )
            logging.info("Успешный вход в систему.")
            self.assertTrue(
                driver.find_element(
                    By.CSS_SELECTOR, "a[href='/personal/']"
                ).is_displayed(),
                "Личный кабинет не отображается.",
            )
            logging.info("Личный кабинет успешно отображается.")
        except Exception as e:
            logging.error("Ошибка при ожидании успешного входа: %s", e)
            self.fail("Не удалось выполнить вход в систему.")

    def test_unsuccessful_login(self):
        driver = self.driver
        logging.info("Переход на страницу авторизации.")

        # Переход на страницу авторизации
        login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
        login_link.click()
        logging.info("Клик по ссылке 'Войти'.")

        # Заполнение формы авторизации с неверными данными
        email_input = driver.find_element(By.NAME, "USER_LOGIN")
        password_input = driver.find_element(By.NAME, "USER_PASSWORD")

        logging.info("Заполнение формы авторизации неверными данными.")
        email_input.send_keys(config.AUTH_EMAIL_INVALID)  # Неверный email
        password_input.send_keys(config.AUTH_PASSWORD_INVALID)  # Неверный пароль

        # Отправка формы
        password_input.send_keys(Keys.RETURN)
        logging.info("Отправка формы авторизации с неверными данными.")

        # Переход на главную страницу после неудачной попытки входа
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/']")
                )  # Селектор для главной страницы
            )
            logging.info("Переход на главную страницу.")
            driver.find_element(By.CSS_SELECTOR, "a[href='/']").click()

            # Проверка отсутствия ссылки на личный кабинет
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "a[href='/personal/']")
                    )
                )
                logging.error(
                    "Личный кабинет отображается, хотя вход должен был быть неуспешным."
                )
                self.fail("Личный кабинет отображается при неуспешном входе.")
            except Exception:
                logging.info("Личный кабинет не отображается - тест пройден.")

        except Exception as e:
            logging.error("Ошибка при ожидании перехода на главную страницу: %s", e)
            self.fail(
                "Не удалось перейти на главную страницу после неудачной попытки входа."
            )

    def tearDown(self):
        # Закрытие браузера
        logging.info("Закрытие браузера.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
