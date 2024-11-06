import config
import unittest
import logging
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestChangePassword(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера (например, Firefox)
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def generate_random_password(self, length=12):
        """Генерация случайного пароля."""
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for i in range(length))

    def test_change_password(self):
        driver = self.driver

        # Вход в личный кабинет
        logging.info("Переход на страницу авторизации.")
        login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
        login_link.click()
        logging.info("Клик по ссылке 'Войти'.")

        # Заполнение формы авторизации

        email_input = driver.find_element(By.NAME, "USER_LOGIN")
        password_input = driver.find_element(By.NAME, "USER_PASSWORD")

        logging.info("Заполнение формы авторизации.")
        email_input.clear()  # Очищаем поле email перед вводом
        email_input.send_keys(config.AUTH_EMAIL_CORRECT)
        password_input.clear()  # Очищаем поле пароля перед вводом
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

        # Переход в личный кабинет и смена пароля
        try:
            logging.info("Переход в личный кабинет.")
            driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").click()

            # Переход к изменению профиля
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/personal/profile/']")
                )
            )
            logging.info("Переход к изменению профиля.")
            driver.find_element(By.CSS_SELECTOR, "a[href='/personal/profile/']").click()

            # Сохранение старого пароля
            config.AUTH_PASSWORD_OLD = config.AUTH_PASSWORD_CORRECT
            logging.info(f"Старый пароль: {config.AUTH_PASSWORD_OLD}")

            # Генерация нового пароля
            config.AUTH_PASSWORD_CORRECT = self.generate_random_password()
            logging.info(
                f"Сгенерированный новый пароль: {config.AUTH_PASSWORD_CORRECT}"
            )

            config.update_config(config.AUTH_PASSWORD_OLD, config.AUTH_PASSWORD_CORRECT)

            # Заполнение полей для смены пароля
            new_password_input = driver.find_element(By.NAME, "NEW_PASSWORD")
            new_password_input.send_keys(config.AUTH_PASSWORD_CORRECT)

            confirm_password_input = driver.find_element(
                By.NAME, "NEW_PASSWORD_CONFIRM"
            )
            confirm_password_input.send_keys(config.AUTH_PASSWORD_CORRECT)

            # Сохранение нового пароля
            save_button = driver.find_element(By.CSS_SELECTOR, "input[name='save']")
            save_button.click()
            logging.info("Новый пароль сохранен.")

            # Ожидание перехода на главную страницу после смены пароля
            logging.info("Ожидание перехода на главную страницу после смены пароля.")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
            )

            # Переход на главную страницу после смены пароля
            driver.find_element(By.CSS_SELECTOR, "[href='/']").click()

            # Ожидание появления кнопки выхода перед нажатием на неё
            logging.info("Ожидание появления элемента выхода.")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[href='/?logout=yes']")
                )
            )

            logging.info("Выход из аккаунта.")
            driver.find_element(By.CSS_SELECTOR, "a[href='/?logout=yes']").click()

            try:
                # Попытка входа со старым паролем
                logging.info("Переход на страницу авторизации.")
                login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
                logging.info("Клик по ссылке 'Войти'.")
                login_link.click()

                # Заполнение формы авторизации
                email_input = driver.find_element(By.NAME, "USER_LOGIN")
                password_input = driver.find_element(By.NAME, "USER_PASSWORD")

                email_input.clear()  # Очищаем поле email перед вводом
                email_input.send_keys(config.AUTH_EMAIL_CORRECT)
                password_input.clear()  # Очищаем поле пароля перед вводом
                password_input.send_keys(config.AUTH_PASSWORD_OLD)
                password_input.send_keys(Keys.RETURN)

                # Ожидание перехода на главную страницу
                logging.info("Ожидание появления ссылки на главную страницу.")
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
                )

                logging.info("Переход на главную страницу.")
                driver.find_element(By.CSS_SELECTOR, "[href='/']").click()

                # Проверка успешного входа со старым паролем по наличию ссылки на вход
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "a[href='/login/']")
                    )
                )
                logging.info("Не удалось войти со старым паролем. Ожидаем неуспех.")

                # Проверка успешного входа с новым паролем
                try:
                    # Попытка входа со старым паролем
                    logging.info("Переход на страницу авторизации.")
                    login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
                    logging.info("Клик по ссылке 'Войти'.")
                    login_link.click()
                    # Теперь пробуем войти с новым паролем:
                    # Заполнение формы авторизации
                    email_input = driver.find_element(By.NAME, "USER_LOGIN")
                    password_input = driver.find_element(By.NAME, "USER_PASSWORD")

                    email_input.clear()  # Очищаем поле email перед вводом
                    email_input.send_keys(config.AUTH_EMAIL_CORRECT)
                    password_input.clear()  # Очищаем поле пароля перед вводом
                    password_input.send_keys(config.AUTH_PASSWORD_CORRECT)
                    password_input.send_keys(Keys.RETURN)

                    # Ожидание перехода на главную страницу
                    logging.info("Ожидание появления ссылки на главную страницу.")
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
                    )

                    logging.info("Переход на главную страницу.")
                    driver.find_element(By.CSS_SELECTOR, "[href='/']").click()

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "a[href='/personal/']")
                        )
                    )
                    logging.info("Успешный вход с новым паролем. Тест пройден.")

                    # Можно также проверить наличие элемента на главной странице
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "a[href='/personal/']")
                        )
                    )
                    logging.info("Авторизация успешна.")

                except Exception:
                    logging.error("Не удалось войти с новым паролем. Тест не пройден.")
                    self.fail("Не удалось войти с новым паролем.")

            except Exception:
                logging.error(Exception)
                logging.error("Успешный вход со старым паролем. Тест не пройден.")
                self.fail("Успешный вход со старым паролем.")

        except Exception as e:
            logging.error(f"Ошибка при смене пароля: {e}")
            self.fail("Не удалось выполнить тест смены пароля.")

    def tearDown(self):
        # Закрытие браузера
        logging.info("Закрытие браузера.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
