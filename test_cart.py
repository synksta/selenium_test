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

    # @unittest.skip("Skipped")
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

    def test_additions_to_cart(self):
        """Проверяет наличие добавок к пицце и роллам на странице оформления заказа.

        Тест выполняет следующие шаги:
        1. Переходит на страницу салатов и добавляет любой салат в корзину.
        2. Открывает корзину и переходит к оформлению заказа.
        3. Проверяет, что добавки для пиццы и роллов отсутствуют на странице оформления заказа.
        4. Переходит на страницу роллов и добавляет любой ролл в корзину, запоминая его ID.
        5. Открывает корзину и переходит к оформлению заказа.
        6. Проверяет наличие добавок для роллов и отсутствие добавок для пиццы на странице оформления заказа.
        7. Переходит на страницу пиццы и добавляет любой товар в корзину.
        8. Открывает корзину и переходит к оформлению заказа.
        9. Проверяет наличие добавок для пиццы и роллов на странице оформления заказа.
        10. Удаляет ранее добавленный ролл из корзины.
        11. Перезагружает страницу оформления заказа.
        12. Проверяет наличие добавок для пиццы и отсутствие добавок для роллов после перезагрузки страницы.

        Ожидается, что добавки будут отображаться корректно в зависимости от выбранной категории товара (пицца или роллы) на всех этапах тестирования.
        """
        driver = self.driver

        # 1. Переходим на страницу салатов
        logging.info("Переход на страницу салатов.")
        driver.find_element(
            By.CSS_SELECTOR, "a.root-item[href='/catalog/salaty/']"
        ).click()

        # 2. Добавляем в корзину любой айтем из категории салатов
        logging.info("Добавление первого салата в корзину.")
        salad_button = driver.find_element(By.CSS_SELECTOR, "a.add_to_basket")
        salad_button.click()

        # 3. Переходим в корзину
        logging.info("Открытие корзины.")
        driver.find_element(By.CSS_SELECTOR, "a.basket_link.show_basket").click()

        logging.info("Открытие корзины")
        cart_reveal_button = driver.find_element(
            By.CSS_SELECTOR, "a.basket_link.show_basket"
        )
        WebDriverWait(driver, 10).until(EC.visibility_of(cart_reveal_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(cart_reveal_button))

        cart_reveal_button.click()

        # 4. Переходим к оформлению заказа
        logging.info("Переход к оформлению заказа.")
        checkout_button = driver.find_element(By.CSS_SELECTOR, "a.checkout")
        WebDriverWait(driver, 10).until(EC.visibility_of(checkout_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(checkout_button))
        checkout_button.click()

        # 5. Проверяем отсутствие добавок для пиццы и роллов
        logging.info("Проверка отсутствия добавок для пиццы и роллов.")
        for addition_id in [318, 319, 320, 321, 323]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertFalse(
                element, f"Добавка с ID {addition_id} отображается, хотя не должна."
            )

        # 6. Переходим на страницу роллов
        logging.info("Переход на страницу роллов.")
        rolls_link = driver.find_element(
            By.CSS_SELECTOR, "a.root-item[href='/catalog/rolly/']"
        )
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(rolls_link))
        rolls_link.click()

        # 7. Добавляем в корзину любой айтем из категории роллов и запоминаем его ID
        logging.info("Добавление первого ролла в корзину.")
        roll_button = driver.find_element(By.CSS_SELECTOR, "a.add_to_basket")
        product_id_roll = roll_button.get_attribute("product-id")  # Запоминаем ID ролла
        roll_button.click()

        # 8. Переходим в корзину
        logging.info("Открытие корзины.")
        driver.find_element(By.CSS_SELECTOR, "a.basket_link.show_basket").click()

        logging.info("Открытие корзины")
        cart_reveal_button = driver.find_element(
            By.CSS_SELECTOR, "a.basket_link.show_basket"
        )
        WebDriverWait(driver, 10).until(EC.visibility_of(cart_reveal_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(cart_reveal_button))

        cart_reveal_button.click()

        # 9. Переходим к оформлению заказа
        logging.info("Переход к оформлению заказа.")
        checkout_button = driver.find_element(By.CSS_SELECTOR, "a.checkout")
        WebDriverWait(driver, 10).until(EC.visibility_of(checkout_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(checkout_button))
        checkout_button.click()

        # 10. Проверяем наличие добавок для роллов и отсутствие добавок для пиццы
        logging.info(
            "Проверка наличия добавок для роллов и отсутствия добавок для пиццы."
        )

        for addition_id in [319, 320, 321]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertTrue(
                element, f"Добавка с ID {addition_id} не отображается, хотя должна."
            )

        for addition_id in [318, 323]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertFalse(
                element, f"Добавка с ID {addition_id} отображается, хотя не должна."
            )

        # 11. Переходим на страницу пиццы
        logging.info("Переход на страницу пиццы.")
        driver.find_element(
            By.CSS_SELECTOR, "a.root-item[href='/catalog/pitstsa/']"
        ).click()

        # 12. Добавляем в корзину любой айтем из категории пиццы
        logging.info("Добавление первого пиццы в корзину.")
        pizza_button = driver.find_element(By.CSS_SELECTOR, "a.add_to_basket")
        pizza_button.click()

        # 13. Переходим в корзину
        logging.info("Открытие корзины.")
        driver.find_element(By.CSS_SELECTOR, "a.basket_link.show_basket").click()

        logging.info("Открытие корзины")
        cart_reveal_button = driver.find_element(
            By.CSS_SELECTOR, "a.basket_link.show_basket"
        )
        WebDriverWait(driver, 10).until(EC.visibility_of(cart_reveal_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(cart_reveal_button))

        cart_reveal_button.click()

        # 14. Переходим к оформлению заказа
        logging.info("Переход к оформлению заказа.")
        checkout_button = driver.find_element(By.CSS_SELECTOR, "a.checkout")
        WebDriverWait(driver, 10).until(EC.visibility_of(checkout_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(checkout_button))
        checkout_button.click()

        # 15. Проверяем наличие добавок для пиццы и роллов
        logging.info("Проверка наличия добавок для пиццы и роллов.")

        for addition_id in [318, 323]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertTrue(
                element, f"Добавка с ID {addition_id} не отображается, хотя должна."
            )

        for addition_id in [319, 320, 321]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertTrue(
                element, f"Добавка с ID {addition_id} не отображается, хотя должна."
            )

        # 16. Удаляем айтем роллов из корзины
        logging.info(f"Удаление товара с ID {product_id_roll} из корзины.")

        delete_button = driver.find_element(
            By.CSS_SELECTOR, f"a.delete_in_basket[data-id-product='{product_id_roll}']"
        )

        # Ожидаем видимости кнопки удаления перед кликом
        WebDriverWait(driver, 10).until(EC.visibility_of(delete_button))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(delete_button))
        delete_button.click()

        logging.info(f"Товар с ID {product_id_roll} успешно удален из корзины.")

        # 17. Перезагружаем страницу
        driver.refresh()
        logging.info("Страница перезагружена.")

        # 18. Проверяем наличие добавок для пиццы и отсутствие добавок для роллов.
        for addition_id in [318, 323]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertTrue(
                element,
                f"Добавка с ID {addition_id} не отображается после перезагрузки страницы, хотя должна.",
            )

        for addition_id in [319, 320, 321]:
            element = driver.find_elements(
                By.CSS_SELECTOR,
                f"div.bp_count_content[data-id-product='{addition_id}']",
            )
            self.assertFalse(
                element,
                f"Добавка с ID {addition_id} отображается после перезагрузки страницы, хотя не должна.",
            )


if __name__ == "__main__":
    unittest.main()
