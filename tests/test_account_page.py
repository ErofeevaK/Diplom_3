import allure
import logging
from data import TextDate
from pages.account_page import AccountPage
from pages.main_page import MainPage

logger = logging.getLogger(__name__)


class TestAccountPage:
    @allure.title("Тест проверки перехода в профиль по клику на Личный кабинет")
    def test_click_through_personal_account(self, driver, login):
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = AccountPage(driver)

        # Используем новую проверку по вкладкам
        account_page.wait_for_account_page_load()

        # ПЕРЕНЕСЕМ ПРОВЕРКУ В PAGE-КЛАСС
        assert account_page.check_all_tabs_loaded(), "Не все вкладки личного кабинета загружены"

        logger.info("Личный кабинет загружен со всеми вкладками")

    @allure.title("Тест проверки перехода в раздел История заказов")
    def test_going_order_history(self, driver, login):
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = AccountPage(driver)
        account_page.wait_for_account_page_load()

        # ПЕРЕНЕСЕМ ЛОГИКУ В PAGE-КЛАСС
        account_page.click_on_order_history_button()

        # ПРОВЕРКА ЧЕРЕЗ PAGE-КЛАСС
        assert account_page.is_order_history_page_loaded(), "Не удалось перейти в раздел истории заказов"

    @allure.title("Тест проверки выхода из аккаунта")
    def test_logout_account(self, driver, login):
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = AccountPage(driver)
        account_page.wait_for_account_page_load()

        # ПЕРЕНЕСЕМ ЛОГИКУ В PAGE-КЛАСС
        account_page.logout()

        # ПРОВЕРКА ЧЕРЕЗ PAGE-КЛАСС
        assert account_page.is_logged_out(), "Не удалось выйти из аккаунта"
