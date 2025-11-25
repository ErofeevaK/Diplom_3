import allure
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.login_page_locators import LoginPageLocators
from locators.main_page_locators import MainPageLocators
from locators.account_page_locators import AccountPageLocators
from pages.base_page import BasePage
from urls import BASE_URL
from seletools.actions import drag_and_drop

logger = logging.getLogger(__name__)

class MainPage(BasePage):
    @allure.step("Переходим на страницу входа через кнопку Войти в аккаунт")
    def go_to_login_page(self):
        with allure.step(f"Перейти на страницу входа"):
            self.wait_for_url(BASE_URL)
            self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)
            self.wait_for_element(MainPageLocators.LOGIN_BUTTON)
            self.scroll_to_element(MainPageLocators.LOGIN_BUTTON)
            element = self.wait_for_element(MainPageLocators.LOGIN_BUTTON)
            self.click_js(element)

    @allure.step("Переходим на страницу входа через кнопку Личный кабинет")
    def go_to_login_page_buttom_lk(self):
        self.wait_for_url(BASE_URL)
        self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)
        self.wait_for_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        element = self.wait_for_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        self.click_js(element)
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
                login_buttons = self.find_elements(MainPageLocators.LOGIN_BUTTON)
                for button in login_buttons:
                    if button.is_displayed():
                        return False
            except:
                pass

            return personal_account_btn.is_displayed()

        except Exception as e:
            logger.error(f"Ошибка при проверке авторизации: {e}")
            return False

    @allure.step("Кликнуть на Конструктор")
    def click_constructor(self):
        element = self.wait_for_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        self.click_js(element)
        self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA)

    @allure.step("Кликнуть на Лента заказов")
    def click_order_feed(self):
        element = self.wait_for_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.click_js(element)
        self.element_is_not_visible(MainPageLocators.MODAL_OVERLAY_LOCATOR)

    @allure.step("Перейти на Ленту заказов")
    def go_to_order_feed(self):
        self.wait_for_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.scroll_to_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.click_order_feed()

    @allure.step("Кликнуть на ингредиент")
    def click_ingredient(self, ingredient_locator):
        self.scroll_to_element(ingredient_locator)
        element = self.wait_for_element(ingredient_locator)
        self.click_js(element)
        self.wait_for_element(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Нажать на кнопку Оформить заказ")
    def make_order(self):
        self.wait_for_element(MainPageLocators.ORDER_BUTTON)
        self.element_is_clickable(MainPageLocators.ORDER_BUTTON)
        element = self.wait_for_element(MainPageLocators.ORDER_BUTTON)
        self.scroll_to_element(MainPageLocators.ORDER_BUTTON)
        self.click_js(element)

    @allure.step("Перетащить элемент")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.element_is_visible(source_locator)
        target = self.element_is_visible(target_locator)
        drag_and_drop(self.driver, source, target)

    @allure.step("Переходим на страницу личного кабинета")
    def go_to_personal_account(self):
        """Простой переход в личный кабинет"""
        self.wait_for_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        element = self.wait_for_element(MainPageLocators.PERSONAL_ACCOUNT_BUTTON)
        self.click_js(element)
        WebDriverWait(self.driver, 10).until(EC.url_contains("/account"))

    @allure.step("Добавить ингредиенты в заказ")
    def add_ingredients_to_order(self):
        """Добавление ингредиентов в заказ с проверками"""
        try:
            logger.info("Начинаем добавление ингредиентов в заказ")

            # Ждем загрузки ингредиентов
            self.wait_for_element(MainPageLocators.INGREDIENT_BUN, timeout=10)
            self.wait_for_element(MainPageLocators.INGREDIENT_MAIN, timeout=10)

            # Добавляем булку (обязательно!)
            logger.info("Добавляем булку в заказ")
            self.drag_and_drop(
                source_locator=MainPageLocators.INGREDIENT_BUN,
                target_locator=MainPageLocators.CONSTRUCTOR_DROP_AREA
            )

            # Ждем пока булка добавится в конструктор
            self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA, timeout=5)
            logger.info("Булка успешно добавлена")

            # Добавляем начинку
            logger.info("Добавляем начинку в заказ")
            self.drag_and_drop(
                source_locator=MainPageLocators.INGREDIENT_MAIN,
                target_locator=MainPageLocators.CONSTRUCTOR_DROP_AREA
            )

            # Ждем пока начинка добавится
            self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA, timeout=5)
            logger.info("Начинка успешно добавлена")

            # Проверяем что кнопка "Оформить заказ" стала активной
            try:
                order_button = self.wait_for_element(MainPageLocators.ORDER_BUTTON, timeout=5)
                if order_button.is_enabled():
                    logger.info("Кнопка 'Оформить заказ' активна - ингредиенты добавлены успешно")
                else:
                    logger.warning("Кнопка 'Оформить заказ' не активна - возможно ингредиенты не добавились")
            except Exception as e:
                logger.error(f"Ошибка при проверке кнопки заказа: {e}")

            logger.info("Все ингредиенты добавлены в заказ")

        except Exception as e:
            logger.error(f"Ошибка при добавлении ингредиентов: {e}")

            # Пробуем альтернативный способ добавления
            logger.info("Пробуем альтернативный способ добавления ингредиентов")
            self.add_ingredients_alternative()
            raise

    @allure.step("Альтернативный способ добавления ингредиентов")
    def add_ingredients_alternative(self):
        """Альтернативный способ добавления ингредиентов через клик"""
        try:
            # Добавляем булку через клик
            bun_element = self.wait_for_element(MainPageLocators.INGREDIENT_BUN)
            self.click_js(bun_element)

            # Добавляем начинку через клик
            main_element = self.wait_for_element(MainPageLocators.INGREDIENT_MAIN)
            self.click_js(main_element)

            logger.info("Ингредиенты добавлены альтернативным способом")
        except Exception as e:
            logger.error(f"Ошибка в альтернативном способе: {e}")
            raise

    @allure.step("Добавить ингредиент в заказ")
    def add_ingredient_to_order(self, ingredient_locator):
        self.scroll_to_element(ingredient_locator)
        self.drag_and_drop(ingredient_locator, MainPageLocators.CONSTRUCTOR_DROP_AREA)