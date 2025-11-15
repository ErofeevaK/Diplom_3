import allure

from data import TextDate
from locators.account_page_locators import AccountPageLocators
from locators.login_page_locators import LoginPageLocators
from pages.account_page import AccountPage
from pages.main_page import MainPage


class TestAccountPage:
    @allure.title("Тест проверки перехода в профиль по клику на Личный кабинет")
    def test_click_through_personal_account(self, driver, login):
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = AccountPage(driver)

        # Используем новую проверку по вкладкам
        account_page.wait_for_account_page_load()
        account_page.check_all_tabs_loaded()

        print("✅ Личный кабинет загружен со всеми вкладками")

    @allure.title("Тест проверки перехода в раздел История заказов")
    def test_going_order_history(self, driver, login):
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = AccountPage(driver)
        account_page.wait_for_account_page_load()
        account_page.click_on_order_history_button()
        current_url = account_page.get_current_url()
        assert TextDate.TEXT_ORDER_HISTORY in current_url

    @allure.title("Тест проверки выхода из аккаунта")
    def test_logout_account(self, driver, login):
        main_page = MainPage(driver)
        main_page.go_to_personal_account()
        account_page = AccountPage(driver)
        account_page.wait_for_account_page_load()
        account_page.scroll_to_element(AccountPageLocators.LOGOUT_BUTTON)
        account_page.click_on_logout_button()
        account_page.wait_for_element(LoginPageLocators.LOGIN_BUTTON_AUTH)
        current_url = account_page.get_current_url()
        assert TextDate.TEXT_LOGIN in current_url