import allure

from locators.account_page_locators import AccountPageLocators, HistoryPageLocators
from pages.base_page import BasePage


class AccountPage(BasePage):
    @allure.step("Кликнуть по кнопке История заказов")
    def click_on_order_history_button(self):
        self.click_element(AccountPageLocators.ORDER_HISTORY)

    @allure.step("Кликнуть по кнопке Выйти")
    def click_on_logout_button(self):
        self.click_element(AccountPageLocators.LOGOUT_BUTTON)

    @allure.step("Подождать загрузки страницы аккаунта")
    def wait_for_account_page_load(self):
        """Ожидание загрузки страницы аккаунта по вкладкам"""
        try:
            # 1. Проверяем URL
            self.wait_for_url("/account")

            # 2. Проверяем что загрузились вкладки навигации
            self.wait_for_element(AccountPageLocators.PROFILE, timeout=10)
            print("✅ Страница аккаунта загружена (найдена вкладка Профиль)")

        except Exception as e:
            print(f"❌ Страница аккаунта не загрузилась: {e}")
            print(f"Текущий URL: {self.driver.current_url}")
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="account_page_not_loaded",
                attachment_type=allure.attachment_type.PNG
            )
            raise

    @allure.step("Проверить что все вкладки загружены")
    def check_all_tabs_loaded(self):
        """Проверка что все основные вкладки аккаунта загружены"""
        tabs = [
            ("Профиль", AccountPageLocators.PROFILE),
            ("История заказов", AccountPageLocators.ORDER_HISTORY),
            ("Выход", AccountPageLocators.LOGOUT_BUTTON)
        ]

        for tab_name, locator in tabs:
            try:
                element = self.wait_for_element(locator, timeout=5)
                print(f"✅ Вкладка '{tab_name}' найдена")
            except:
                print(f"❌ Вкладка '{tab_name}' не найдена")
                raise