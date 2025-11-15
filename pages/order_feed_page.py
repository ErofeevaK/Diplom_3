import allure

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from data import TextDate
from locators.main_page_locators import MainPageLocators
from locators.order_feed_page_locators import OrderFeedPageLocators
from pages.base_page import BasePage


class OrderFeedPage(BasePage):
    @allure.step("Получить номер оформленного заказа")
    def get_new_order_number(self):
        WebDriverWait(self.driver, 10).until(lambda driver: self.wait_and_find_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER).text != '9999')
        new_order_number_element = self.wait_and_find_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER)
        new_order_number = new_order_number_element.text
        return int(new_order_number)

    @allure.step("Закрыть модальное окно")
    def close_modal_window(self):
        OVERLAY = (By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr")
        MODAL_CONTENT = (By.CSS_SELECTOR, "div.Modal_modal__contentBox__sCy8X")

        # 1. Пытаемся закрыть через overlay
        try:
            overlay = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(OVERLAY)
            )
            self.click_js(overlay)  # <<< важный момент!
        except Exception as e:
            print(f"❌ Не удалось закрыть через overlay: {e}")

            # 2. Пробуем закрыть крестиком
            try:
                close_btn = self.wait_and_find_element(OrderFeedPageLocators.MODAL_CLOSE_ORDER)
                self.click_js(close_btn)
            except Exception as e2:
                print(f"❌ Не удалось закрыть через крестик: {e2}")
                raise Exception("Модальное окно НЕ закрыто")

        # 3. Обязательное ожидание: модалка исчезает
        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(MODAL_CONTENT)
        )
        print("✅ Модальное окно закрыто")

    @allure.step("Получить номер заказа в разделе В работе на экране Лента заказов")
    def get_order_id_in_progress_list(self):
        self.wait_and_find_element(OrderFeedPageLocators.ORDERS_AT_WORK)
        result = self.get_element_text(OrderFeedPageLocators.ORDERS_AT_WORK)
        return result

    @allure.step("Получить номера заказов из Ленты заказов")
    def find_orders_list(self):
        orders_section = self.get_element_text(OrderFeedPageLocators.ORDER_FEED_LIST)
        normalized_orders = [
            line.strip().lstrip('#').strip()
            for line in orders_section.splitlines()
            if line.startswith('#')
        ]
        return normalized_orders

    @allure.step("Кликнуть на Конструктор")
    def click_constructor(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA)

    @allure.step("Ждем пока исчезнет текст Все текущие заказы готовы!")
    def wait_for_status_text_to_disappear(self):
        self.wait_until_text_is_not_visible(OrderFeedPageLocators.STATUS_READY_TEXT,TextDate.TEXT_DISAPPEAR)