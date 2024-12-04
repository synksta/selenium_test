import unittest
from test_page_load import TestPageLoad
from test_links import TestLinks
from test_login import TestLogin
from test_change_password import TestChangePassword
from test_favorites import TestFavorites
from test_cart import TestCart

# Список всех классов тестов
test_classes = [
    TestPageLoad,
    TestLinks,
    TestLogin,
    TestChangePassword,
    TestFavorites,
    TestCart,
]


def suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

        # Вывод информации о каждом тесте
        for test in tests:
            print(f"Test ID: {test.id()}, Description: {test.shortDescription()}")

    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
