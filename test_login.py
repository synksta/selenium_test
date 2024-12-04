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

    def test_login_successful(self):
        """Проверяет успешный вход в систему с корректными учетными данными.

        Тест выполняет следующие шаги:
        1. Переходит на страницу авторизации.
        2. Заполняет форму авторизации корректными учетными данными (логин и пароль).
        3. Отправляет форму и ожидает перехода на страницу личного кабинета.
        4. Проверяет, что личный кабинет отображается на странице.

        Ожидается, что при вводе корректных учетных данных пользователь успешно войдет в систему и увидит личный кабинет.
        """

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

        # Ожидание перехода на страницу личного кабинета и проверка успешного входа
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/personal/']"))
        )

        logging.info("Успешный вход в систему.")

        # Проверка отображения личного кабинета
        self.assertTrue(
            driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").is_displayed(),
            "Личный кабинет не отображается.",
        )
        logging.info("Личный кабинет успешно отображается.")

    def test_login_unsuccessful(self):
        """Проверяет неудачный вход в систему с неверными учетными данными.

        Тест выполняет следующие шаги:
        1. Переходит на страницу авторизации.
        2. Заполняет форму авторизации неверными учетными данными (логин и пароль).
        3. Отправляет форму и ожидает возвращения на главную страницу после неудачной попытки входа.
        4. Проверяет, что ссылка на личный кабинет не отображается.

        Ожидается, что при вводе неверных учетных данных пользователь не сможет войти в систему, и ссылка на личный кабинет не будет доступна.
        """

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

        # Ожидание перехода на главную страницу после неудачной попытки входа
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
        )

        main_link = driver.find_element(By.CSS_SELECTOR, "a[href='/']")
        main_link.click()

        logging.info("Переход на главную страницу.")

        # Проверка отсутствия ссылки на личный кабинет

        self.assertFalse(
            len(driver.find_elements(By.CSS_SELECTOR, "a[href='/personal/']")) > 0,
            "Ссылка на личный кабинет отображается.",
        )
        logging.info("Ссылка на личный кабинет не отображается.")

    def tearDown(self):
        # Закрытие браузера
        logging.info("Закрытие браузера.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
