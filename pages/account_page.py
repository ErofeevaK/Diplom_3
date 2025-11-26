import allure
import logging
from locators.account_page_locators import AccountPageLocators
from locators.login_page_locators import LoginPageLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class AccountPage(BasePage):

    # ========== БАЗОВЫЕ МЕТОДЫ ==========

    @allure.step("Подождать загрузки страницы аккаунта")
    def wait_for_account_page_load(self):
        """Ожидание загрузки страницы аккаунта по вкладкам"""
        try:
            self.wait_for_url("/account")
            self.wait_for_element(AccountPageLocators.PROFILE, timeout=10)
            logger.info("Страница аккаунта загружена (найдена вкладка Профиль)")

        except Exception as e:
            logger.error(f"Страница аккаунта не загрузилась: {e}")
            logger.debug(f"Текущий URL: {self.driver.current_url}")
            self.take_screenshot("account_page_not_loaded")
            raise

    # ========== ДЕЙСТВИЯ ==========

    @allure.step("Кликнуть по кнопке История заказов")
    def click_on_order_history_button(self):
        element = self.element_is_clickable(AccountPageLocators.ORDER_HISTORY)
        self.click_js(element)

    @allure.step("Кликнуть по кнопке Выйти")
    def click_on_logout_button(self):
        element = self.element_is_clickable(AccountPageLocators.LOGOUT_BUTTON)
        self.click_js(element)

    # ========== ПРОВЕРКИ ==========

    @allure.step("Проверить что все вкладки загружены")
    def check_all_tabs_loaded(self):
        """Проверка что все основные вкладки аккаунта загружены"""
        try:
            tabs = [
                ("Профиль", AccountPageLocators.PROFILE),
                ("История заказов", AccountPageLocators.ORDER_HISTORY),
                ("Выход", AccountPageLocators.LOGOUT_BUTTON)
            ]

            all_tabs_found = True
            for tab_name, locator in tabs:
                try:
                    element = self.wait_for_element(locator, timeout=3)
                    logger.debug(f"Вкладка '{tab_name}' найдена")
                except Exception as e:
                    logger.warning(f"Вкладка '{tab_name}' не найдена: {e}")
                    all_tabs_found = False

            return all_tabs_found

        except Exception as e:
            logger.error(f"Ошибка при проверке вкладок: {e}")
            return False

    # ========== НОВЫЕ МЕТОДЫ ДЛЯ ТЕСТОВ ==========

    @allure.step("Проверить что страница истории заказов загружена")
    def is_order_history_page_loaded(self):
        """Проверка что мы на странице истории заказов"""
        try:
            current_url = self.get_current_url()
            return "/order-history" in current_url or "history" in current_url.lower()
        except Exception as e:
            logger.error(f"Ошибка при проверке страницы истории заказов: {e}")
            return False

    @allure.step("Выйти из аккаунта")
    def logout(self):
        """Полный процесс выхода из аккаунта"""
        self.scroll_to_element(AccountPageLocators.LOGOUT_BUTTON)
        self.click_on_logout_button()
        self.wait_for_element(LoginPageLocators.LOGIN_BUTTON_AUTH)

    @allure.step("Проверить что выход выполнен успешно")
    def is_logged_out(self):
        """Проверка что выход из аккаунта выполнен"""
        try:
            current_url = self.get_current_url()
            return "/login" in current_url or "auth" in current_url.lower()
        except Exception as e:
            logger.error(f"Ошибка при проверке выхода из аккаунта: {e}")
            return False

    # ========== ДОПОЛНИТЕЛЬНЫЕ МЕТОДЫ АККАУНТА ==========

    @allure.step("Перейти в профиль")
    def go_to_profile(self):
        """Переход в раздел профиля"""
        element = self.element_is_clickable(AccountPageLocators.PROFILE)
        self.click_js(element)
        self.wait_for_element(AccountPageLocators.PROFILE_CONTENT, timeout=5)

    @allure.step("Проверить активна ли вкладка профиля")
    def is_profile_tab_active(self):
        """Проверка что вкладка профиля активна"""
        try:
            element = self.wait_for_element(AccountPageLocators.PROFILE)
            return "active" in element.get_attribute("class").lower()
        except Exception as e:
            logger.error(f"Ошибка при проверке активности вкладки профиля: {e}")
            return False

    @allure.step("Получить имя пользователя в аккаунте")
    def get_username(self):
        """Получение имени пользователя из аккаунта"""
        try:
            element = self.wait_for_element(AccountPageLocators.USERNAME)
            return element.text.strip()
        except Exception as e:
            logger.error(f"Не удалось получить имя пользователя: {e}")
            return ""