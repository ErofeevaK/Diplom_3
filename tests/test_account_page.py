import allure
import logging
from pages.account_page import AccountPage
from pages.main_page import MainPage

logger = logging.getLogger(__name__)


class TestAccountPage:
    @allure.title("Тест проверки перехода в профиль по клику на Личный кабинет")
    def test_click_through_personal_account(self, driver, login_setup):
        main_page = MainPage(driver)
        account_page = AccountPage(driver)

        # Переходим в личный кабинет
        main_page.go_to_personal_account()

        # Проверяем загрузку страницы аккаунта
        account_page.wait_for_account_page_load()

        # Проверяем что все вкладки загружены (используем метод с assert)
        account_page.assert_all_tabs_loaded()

        # Проверяем URL страницы аккаунта
        account_page.assert_account_url_correct()

        logger.info("Личный кабинет загружен со всеми вкладками")

    @allure.title("Тест проверки перехода в раздел История заказов")
    def test_going_order_history(self, driver, login_setup):
        main_page = MainPage(driver)
        account_page = AccountPage(driver)

        # Переходим в личный кабинет
        main_page.go_to_personal_account()
        account_page.wait_for_account_page_load()

        # Переходим в историю заказов
        account_page.click_on_order_history_button()

        # Проверяем что страница истории заказов загрузилась (используем метод с assert)
        account_page.assert_order_history_page_loaded()

        logger.info("Успешный переход в раздел истории заказов")

    @allure.title("Тест проверки выхода из аккаунта")
    def test_logout_account(self, driver, login_setup):
        main_page = MainPage(driver)
        account_page = AccountPage(driver)

        # Переходим в личный кабинет
        main_page.go_to_personal_account()
        account_page.wait_for_account_page_load()

        # Выходим из аккаунта
        account_page.logout()

        # Проверяем что выход выполнен (используем метод с assert)
        account_page.assert_logged_out()

        logger.info("Успешный выход из аккаунта")