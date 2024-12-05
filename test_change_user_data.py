import config
import unittest
import logging
from utils.password import generate_random_password
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.phonenumber import parse_phone_number


# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestChangeUserData(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера (например, Firefox)
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    @unittest.skip("Пропускаем этот тест")
    def test_change_password(self):
        """Проверяет процесс изменения пароля пользователя.

        Тест выполняет следующие шаги:
        1. Переходит на страницу авторизации и выполняет вход с корректными учетными данными.
        2. Переходит в личный кабинет и открывает страницу изменения профиля.
        3. Генерирует новый случайный пароль и сохраняет его.
        4. Выходит из аккаунта и пытается войти с использованием старого пароля, чтобы убедиться, что он больше не работает.
        5. Входит в аккаунт с новым паролем и проверяет отображение личного кабинета.

        Ожидается, что после смены пароля старый пароль не будет работать, а новый пароль позволит успешно войти в систему.
        """

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
        driver.find_element(By.CSS_SELECTOR, "a[href='/']").click()

        # Переход в личный кабинет и смена пароля
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

        # Сохранение старого пароля и генерация нового пароля
        config.AUTH_PASSWORD_OLD = config.AUTH_PASSWORD_CORRECT
        config.AUTH_PASSWORD_CORRECT = self.generate_random_password()

        logging.info(f"Старый пароль: {config.AUTH_PASSWORD_OLD}")
        logging.info(f"Сгенерированный новый пароль: {config.AUTH_PASSWORD_CORRECT}")

        config.update_config(config.AUTH_PASSWORD_OLD, config.AUTH_PASSWORD_CORRECT)

        # Заполнение полей для смены пароля
        new_password_input = driver.find_element(By.NAME, "NEW_PASSWORD")
        new_password_input.send_keys(config.AUTH_PASSWORD_CORRECT)

        confirm_password_input = driver.find_element(By.NAME, "NEW_PASSWORD_CONFIRM")
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
        driver.find_element(By.CSS_SELECTOR, "a[href='/']").click()

        # Ожидание появления кнопки выхода перед нажатием на неё
        logging.info("Ожидание появления элемента выхода.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/?logout=yes']"))
        )

        logging.info("Выход из аккаунта.")

        driver.find_element(By.CSS_SELECTOR, "a[href='/?logout=yes']").click()

        # Вход в личный кабинет
        logging.info("Переход на страницу авторизации.")
        login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
        logging.info("Клик по ссылке 'Войти'.")
        login_link.click()

        # Заполнение формы авторизации со старым паролем
        logging.info("Заполнение формы авторизации со старым паролем")

        # Заполнение формы авторизации
        email_input = driver.find_element(By.NAME, "USER_LOGIN")
        password_input = driver.find_element(By.NAME, "USER_PASSWORD")

        email_input.clear()

        email_input.send_keys(config.AUTH_EMAIL_CORRECT)

        password_input.clear()

        password_input.send_keys(config.AUTH_PASSWORD_OLD)

        password_input.send_keys(Keys.RETURN)

        # # Ожидание перехода на главную страницу
        logging.info("Ожидание появления ссылки на главную страницу.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
        )

        logging.info("Переход на главную страницу.")

        driver.find_element(By.CSS_SELECTOR, "a[href='/']").click()

        logging.info("Ожидание появления ссылки на вход.")
        # Проверка отображения личного кабинета
        self.assertTrue(
            driver.find_element(By.CSS_SELECTOR, "a.login").is_displayed(),
            "Ссылка на вход не отображается.",
        )
        logging.info("Ссылка на вход успешно отображается.")

        logging.info("Переход на страницу входа.")
        login_link = driver.find_element(By.CSS_SELECTOR, "a.login")
        login_link.click()

        # Заполнение формы авторизации с актуальным паролем
        logging.info("Заполнение формы авторизации с актуальным паролем")

        # Заполнение формы авторизации
        email_input = driver.find_element(By.NAME, "USER_LOGIN")
        password_input = driver.find_element(By.NAME, "USER_PASSWORD")

        email_input.clear()

        email_input.send_keys(config.AUTH_EMAIL_CORRECT)

        password_input.clear()

        password_input.send_keys(config.AUTH_PASSWORD_CORRECT)

        password_input.send_keys(Keys.RETURN)

        # # Ожидание перехода на главную страницу
        logging.info("Ожидание появления ссылки на главную страницу.")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
        )

        logging.info("Переход на главную страницу.")

        driver.find_element(By.CSS_SELECTOR, "a[href='/']").click()

        logging.info("Ожидание появления ссылки на вход.")
        # Проверка отображения личного кабинета
        self.assertTrue(
            driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").is_displayed(),
            "Ссылка на на личный кабинет не отображается.",
        )
        logging.info("Ссылка на личный кабинет успешно отображается - тест пройден")

        logging.info("Переход в личный кабинет.")
        personal_link = driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']")
        personal_link.click()

    def test_change_personal(self):
        """
        Тест для изменения пользовательских данных в личном кабинете.

        Этот тест выполняет следующие шаги:
        1. Переход на страницу авторизации и заполнение формы авторизации.
        2. Переход в личный кабинет пользователя.
        3. Переход к странице изменения профиля.
        4. Изменение имени, телефонного номера и адреса доставки:
            - Если текущее имя, телефон или адрес не пустые, они переворачиваются.
            - Если пустые, используются значения из конфигурации.
        5. Сохранение изменений.
        6. Проверка, что измененные данные отображаются корректно на странице профиля.

        Проверяемые данные:
        - Имя пользователя
        - Телефонный номер
        - Адрес доставки

        Исключения:
        - AssertionError будет вызвано, если имена, телефонные номера или адреса не совпадают с ожидаемыми значениями.

        Логирование:
        В процессе выполнения теста ведется логирование ключевых действий для упрощения отладки.

        Returns:
            None
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
        logging.info("Отправка формы авторизации.")
        submit_button = driver.find_element(By.NAME, "Login")
        submit_button.click()

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

        name_input = driver.find_element(By.NAME, "NAME")
        current_name = name_input.get_attribute("value")
        name_input.clear()

        new_name = ""
        new_phone = ""
        new_address = ""
        if len(current_name):
            new_name = current_name[::-1]
        else:
            new_name = config.NAME
        logging.info(f"Ввод нового имени: {new_name}")
        name_input.send_keys(config.NAME)

        phone_input = driver.find_element(By.NAME, "PERSONAL_PHONE")
        current_phone = parse_phone_number(phone_input.get_attribute("value"))
        phone_input.clear()
        if len(current_phone):
            new_phone = current_phone[::-1]
        else:
            new_phone = config.PHONE
        logging.info(f"Ввод нового телефонного номера: {new_phone}")
        phone_input.send_keys(new_phone)

        address_input = driver.find_element(By.NAME, "PERSONAL_STREET")
        current_address = address_input.get_attribute("innerHTML")
        address_input.clear()
        if len(current_address):
            new_address = current_address[::-1]
        else:
            new_address = config.ADDRESS
        logging.info(f"Ввод нового адреса доставки: {new_address}")
        address_input.send_keys(new_address)

        # logging.info(f"Ввод пароля в поле подтверждения")
        # password_confirmation_input = driver.find_element(By.NAME, "NEW_PASSWORD_CONFIRM")
        # password_confirmation_input.send_keys(config.AUTH_PASSWORD_CORRECT)

        logging.info(f"Нажатие на кнопку сохранения изменений")
        save_button = driver.find_element(By.NAME, "save")
        save_button.click()

        # Переход к изменению профиля
        logging.info("Перезагрузка профиля.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "a[href='/personal/profile/']")
            )
        )
        driver.find_element(By.CSS_SELECTOR, "a[href='/personal/']").click()

        logging.info("Проверка совпдаения имен.")
        displayed_name = driver.find_element(
            By.XPATH, "//div[contains(text(), 'Имя:')]/following-sibling::div"
        ).text
        self.assertTrue(
            displayed_name == new_name,
            f"Имена {displayed_name} и {new_name} не совпадают.",
        )

        logging.info("Проверка совпдаения телефонных номеров.")
        displayed_phone = parse_phone_number(
            driver.find_element(
                By.XPATH, "//div[contains(text(), 'Телефон:')]/following-sibling::div"
            ).text
        )
        self.assertTrue(
            displayed_phone == new_phone,
            f"Телефонные номера {displayed_phone} и {new_phone} не совпадают.",
        )

        logging.info("Проверка совпдаения адресов.")
        displayed_address = driver.find_element(
            By.XPATH,
            "//div[contains(text(), 'Адрес доставки:')]/following-sibling::div",
        ).text
        self.assertTrue(
            displayed_address == new_address,
            f"Адреса {displayed_address} и {new_address} не совпадают.",
        )

    def tearDown(self):
        # Закрытие браузера
        logging.info("Закрытие браузера.")
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
