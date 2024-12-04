import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import config
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TestCart(unittest.TestCase):
    def setUp(self):
        # Инициализация веб-драйвера
        self.driver = webdriver.Firefox()
        self.driver.get(config.MAIN_URL)
        logging.info(f"Открыт сайт: {config.MAIN_URL}")

    def tearDown(self):
        # Закрытие драйвера после завершения теста
        self.driver.quit()
        logging.info("Закрыт веб-драйвер.")

    def test_add_to_cart(self):
        """Проверяет функциональность добавления товара в корзину и его последующее удаление.

        Тест выполняет следующие шаги:
        1. Находит кнопку добавления товара в корзину и запоминает его идентификатор (product-id).
        2. Нажимает на кнопку добавления товара в корзину.
        3. Открывает корзину и проверяет, что товар успешно добавлен.
        4. Проверяет наличие товара в корзине по его идентификатору.
        5. Находит кнопку удаления товара из корзины и проверяет, что она доступна для взаимодействия.
        6. Наводит курсор на карточку товара, чтобы активировать кнопку удаления.
        7. Ожидает, пока кнопка удаления станет видимой и активной, и нажимает на нее для удаления товара из корзины.

        Ожидается, что товар будет успешно добавлен в корзину и затем удален без ошибок.
        """

        driver = self.driver

        # 1. Находим кнопку добавления товара в корзину и запоминаем product-id
        logging.info("Поиск кнопки добавления товара в корзину.")
        add_to_basket_button = driver.find_element(By.CSS_SELECTOR, "a.add_to_basket")
        product_id = add_to_basket_button.get_attribute("product-id")
        logging.info(f"Найден товар с ID: {product_id}. Добавление в корзину.")

        # Нажимаем на кнопку добавления в корзину
        add_to_basket_button.click()
        logging.info("Товар добавлен в корзину.")

        # 2. Открываем корзину
        logging.info("Открытие корзины.")
        basket_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.basket_link.show_basket"))
        )
        basket_link.click()
        logging.info("Корзина успешно открыта.")

        # 3. Проверяем наличие товара в корзине
        logging.info("Проверка наличия товара в корзине.")
        basket_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.basket_tab_content"))
        )

        # Проверяем наличие товара с соответствующим data-id-product
        product_in_basket = basket_content.find_element(
            By.CSS_SELECTOR,
            f"div.mb_product_count_container[data-id-product='{product_id}']",
        )

        self.assertTrue(
            product_in_basket is not None,
            f"Товар с ID {product_id} не найден в корзине.",
        )
        logging.info(f"Товар с ID {product_id} успешно найден в корзине.")

        # 4. Проверяем элемент удаления товара из корзины
        logging.info("Поиск кнопки удаления товара из корзины.")

        delete_button = basket_content.find_element(
            By.CSS_SELECTOR,
            f"a.mb_delete.delete_in_basket[data-id-product='{product_id}']",
        )

        self.assertTrue(
            delete_button is not None,
            f"Кнопка удаления товара с ID {product_id} не найдена.",
        )

        item_card = delete_button.find_element(By.XPATH, "..")

        # Ожидаем, пока кнопка удаления станет доступной для взаимодействия
        WebDriverWait(driver, 10).until(EC.visibility_of(item_card))

        # Проверяем, что кнопка отображается и активна перед кликом
        self.assertTrue(
            item_card.is_displayed(),
            f"Карточка товара с ID {product_id} не отображается.",
        )

        logging.info(f"Наведение курсора на карточку товара с ID {product_id}.")
        # Используем ActionChains для наведения курсора на кнопку удаления
        actions = ActionChains(driver)
        #  Наведение курсора на элемент
        actions.move_to_element(item_card).perform()
        logging.info(f"Ожидание кнопки удаления товара с ID {product_id}.")

        # Ожидаем, пока кнопка удаления станет доступной для взаимодействия
        WebDriverWait(driver, 10).until(EC.visibility_of(delete_button))

        # Проверяем, что кнопка отображается и активна перед кликом
        self.assertTrue(
            delete_button.is_displayed() and delete_button.is_enabled(),
            f"Кнопка удаления товара с ID {product_id} не активна.",
        )

        logging.info(
            f"Кнопка удаления товара с ID {product_id} найдена. Удаление товара из корзины."
        )

        delete_button.click()

        logging.info(f"Товар с ID {product_id} успешно удален из корзины.")


if __name__ == "__main__":
    unittest.main()
