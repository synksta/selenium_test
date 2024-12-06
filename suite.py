import unittest
from test_page_load import TestPageLoad
from test_links import TestLinks
from test_login import TestLogin
from test_change_user_data import TestChangeUserData
from test_favorites import TestFavorites
from test_cart import TestCart
from test_search import TestSearch

# Список всех классов тестов
test_classes = [
    # TestPageLoad,
    # TestLinks,
    # TestLogin,
    # TestChangeUserData,
    # TestFavorites,
    # TestCart,
    TestSearch
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
