import allure

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.login_page_locators import LoginPageLocators
from locators.main_page_locators import MainPageLocators
from locators.account_page_locators import AccountPageLocators
from pages.base_page import BasePage
from urls import BASE_URL
from seletools.actions import drag_and_drop
import time


class MainPage(BasePage):
    @allure.step("Переходим на страницу входа через кнопку Войти в аккаунт")
    def go_to_login_page(self):
        with allure.step(f"Перейти на страницу входа"):
            self.wait_for_url(BASE_URL)
            self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)
            self.wait_for_element(MainPageLocators.LOGIN_BUTTON)
            self.scroll_to_element(MainPageLocators.LOGIN_BUTTON)
            self.click_element(MainPageLocators.LOGIN_BUTTON)

    @allure.step("Переходим на страницу входа через кнопку Личный кабинет")
    def go_to_login_page_buttom_lk(self):
        self.wait_for_url(BASE_URL)
        self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)
        self.wait_for_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)
        self.wait_for_element(LoginPageLocators.EMAIL_INPUT)

    @allure.step("Проверить авторизацию")
    def check_authorization(self):
        """Проверка что пользователь авторизован"""
        try:
            # Проверяем что мы на главной странице
            self.wait_for_url(BASE_URL, timeout=5)

            # Проверяем наличие кнопки "Личный кабинет" (признак авторизации)
            personal_account_btn = self.element_is_visible(AccountPageLocators.PERSONAL_ACCOUNT_BUTTON, timeout=5)

            # Проверяем что кнопка "Войти в аккаунт" отсутствует
            try:
                login_buttons = self.driver.find_elements(*MainPageLocators.LOGIN_BUTTON)
                for button in login_buttons:
                    if button.is_displayed():
                        return False
            except:
                pass

            return personal_account_btn.is_displayed()

        except Exception as e:
            print(f"Проверка авторизации: {e}")
            return False

    @allure.step("Кликнуть на Конструктор")
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA)

    @allure.step("Кликнуть на Лента заказов")
    def click_order_feed(self):
        self.click_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)
        #self.wait_for_element(MainPageLocators.ORDER_FEED_SECTION)

    @allure.step("Перейти на Ленту заказов")
    def go_to_order_feed(self):
        self.wait_for_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.scroll_to_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.click_order_feed()

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self, ingredient_locator):
        self.scroll_to_element(ingredient_locator)
        self.click_element(ingredient_locator)
        self.wait_for_element(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Нажать на кнопку Оформить заказ")
    def make_order(self):
        self.wait_for_element(MainPageLocators.ORDER_BUTTON)
        self.element_is_clickable(MainPageLocators.ORDER_BUTTON)
        self.scroll_to_element(MainPageLocators.ORDER_BUTTON)
        self.click_element(MainPageLocators.ORDER_BUTTON)

    @allure.step("Перетащить элемент")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.element_is_visible(source_locator)
        target = self.element_is_visible(target_locator)
        drag_and_drop(self.driver, source, target)

    @allure.step("Переходим на страницу личного кабинета")
    def go_to_personal_account(self):
        """Простой переход в личный кабинет"""
        self.wait_for_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        self.click_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)

        import time
        time.sleep(3)

    @allure.step("Добавить ингредиенты в заказ")
    def add_ingredients_to_order(self):
        """Добавление ингредиентов в заказ с конкретными локаторами"""
        try:
            # Добавляем булку
            self.drag_and_drop(
                source_locator=MainPageLocators.INGREDIENT_BUN,
                target_locator=MainPageLocators.CONSTRUCTOR_DROP_AREA
            )
            time.sleep(1)

            # Добавляем начинку
            self.drag_and_drop(
                source_locator=MainPageLocators.INGREDIENT_MAIN,
                target_locator=MainPageLocators.CONSTRUCTOR_DROP_AREA
            )

            print("✅ Ингредиенты добавлены в заказ")

        except Exception as e:
            print(f"❌ Ошибка при добавлении ингредиентов: {e}")
            raise

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, ingredient_locator):
        self.scroll_to_element(ingredient_locator)
        self.drag_and_drop(ingredient_locator, MainPageLocators.CONSTRUCTOR_DROP_AREA)