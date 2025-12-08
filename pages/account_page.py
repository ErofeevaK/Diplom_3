import allure
import logging
from locators.account_page_locators import AccountPageLocators
from locators.login_page_locators import LoginPageLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class AccountPage(BasePage):


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


    @allure.step("Кликнуть по кнопке История заказов")
    def click_on_order_history_button(self):
        element = self.element_is_clickable(AccountPageLocators.ORDER_HISTORY)
        self.click_js(element)

    @allure.step("Кликнуть по кнопке Выйти")
    def click_on_logout_button(self):
        element = self.element_is_clickable(AccountPageLocators.LOGOUT_BUTTON)
        self.click_js(element)


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

    @allure.step("Проверить что страница истории заказов загружена")
    def is_order_history_page_loaded(self):
        """Проверка что мы на странице истории заказов"""
        try:
            current_url = self.get_current_url()
            return "/order-history" in current_url or "history" in current_url.lower()
        except Exception as e:
            logger.error(f"Ошибка при проверке страницы истории заказов: {e}")
            return False

    @allure.step("Проверить что выход выполнен успешно")
    def is_logged_out(self):
        """Проверка что выход из аккаунта выполнен"""
        try:
            current_url = self.get_current_url()
            return "/login" in current_url or "auth" in current_url.lower()
        except Exception as e:
            logger.error(f"Ошибка при проверке выхода из аккаунта: {e}")
            return False


    @allure.step("Проверить что все вкладки загружены (с assert)")
    def assert_all_tabs_loaded(self):
        """Проверка что все основные вкладки аккаунта загружены"""
        try:
            tabs = [
                ("Профиль", AccountPageLocators.PROFILE),
                ("История заказов", AccountPageLocators.ORDER_HISTORY),
                ("Выход", AccountPageLocators.LOGOUT_BUTTON)
            ]

            missing_tabs = []
            for tab_name, locator in tabs:
                try:
                    self.wait_for_element(locator, timeout=3)
                    logger.debug(f"Вкладка '{tab_name}' найдена")
                except Exception as e:
                    logger.warning(f"Вкладка '{tab_name}' не найдена: {e}")
                    missing_tabs.append(tab_name)

            assert len(missing_tabs) == 0, f"Не найдены вкладки: {', '.join(missing_tabs)}"
            logger.info("Все вкладки личного кабинета загружены")

        except Exception as e:
            logger.error(f"Ошибка при проверке вкладок: {e}")
            raise

    @allure.step("Проверить что страница истории заказов загружена (с assert)")
    def assert_order_history_page_loaded(self):
        """Проверка что мы на странице истории заказов"""
        try:
            current_url = self.get_current_url()
            assert "/order-history" in current_url or "history" in current_url.lower(), \
                f"Страница истории заказов не загружена. Текущий URL: {current_url}"
            logger.info("Страница истории заказов успешно загружена")

        except Exception as e:
            logger.error(f"Ошибка при проверке страницы истории заказов: {e}")
            raise

    @allure.step("Проверить что выход выполнен успешно (с assert)")
    def assert_logged_out(self):
        """Проверка что выход из аккаунта выполнен"""
        try:
            current_url = self.get_current_url()
            assert "/login" in current_url or "auth" in current_url.lower(), \
                f"Выход не выполнен. Текущий URL: {current_url}"
            logger.info("Выход из аккаунта выполнен успешно")

        except Exception as e:
            logger.error(f"Ошибка при проверке выхода из аккаунта: {e}")
            raise

    @allure.step("Проверить URL страницы аккаунта")
    def assert_account_url_correct(self):
        """Проверка корректности URL страницы аккаунта"""
        try:
            current_url = self.get_current_url()
            assert "/account" in current_url, \
                f"Некорректный URL страницы аккаунта: {current_url}"
            logger.info(f"URL страницы аккаунта корректен: {current_url}")

        except Exception as e:
            logger.error(f"Ошибка при проверке URL аккаунта: {e}")
            raise


    @allure.step("Выйти из аккаунта")
    def logout(self):
        """Полный процесс выхода из аккаунта"""
        self.scroll_to_element(AccountPageLocators.LOGOUT_BUTTON)
        self.click_on_logout_button()
        self.wait_for_element(LoginPageLocators.LOGIN_BUTTON_AUTH)

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

    @allure.step("Проверить активна ли вкладка профиля (с assert)")
    def assert_profile_tab_active(self):
        """Проверка что вкладка профиля активна"""
        try:
            element = self.wait_for_element(AccountPageLocators.PROFILE)
            class_attribute = element.get_attribute("class").lower()
            assert "active" in class_attribute, \
                f"Вкладка профиля не активна. Классы элемента: {class_attribute}"
            logger.info("Вкладка профиля активна")

        except Exception as e:
            logger.error(f"Ошибка при проверке активности вкладки профиля: {e}")
            raise

    @allure.step("Получить имя пользователя в аккаунте")
    def get_username(self):
        """Получение имени пользователя из аккаунта"""
        try:
            element = self.wait_for_element(AccountPageLocators.USERNAME)
            return element.text.strip()
        except Exception as e:
            logger.error(f"Не удалось получить имя пользователя: {e}")
            return ""

    @allure.step("Проверить имя пользователя")
    def assert_username_equals(self, expected_username):
        """Проверка имени пользователя в аккаунте"""
        try:
            element = self.wait_for_element(AccountPageLocators.USERNAME)
            actual_username = element.text.strip()
            assert actual_username == expected_username, \
                f"Имя пользователя не совпадает. Ожидалось: '{expected_username}', получено: '{actual_username}'"
            logger.info(f"Имя пользователя совпадает: {actual_username}")

        except Exception as e:
            logger.error(f"Не удалось проверить имя пользователя: {e}")
            raise