import allure
import logging
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from locators.order_feed_page_locators import OrderFeedPageLocators

logger = logging.getLogger(__name__)


class TestOrderFeed:
    @allure.title("Проверка при создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    def test_order_counter_all_time_increases(self, driver, login_setup):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        with allure.step("Идем на страницу заказов и получаем значение счетчика «Выполнено за всё время»"):
            main_page.go_to_order_feed()
            all_orders_count_initially = order_page.get_all_orders_counter()

        with allure.step("Создаем новый заказ"):
            main_page.click_constructor()
            main_page.add_ingredients_to_order()
            main_page.make_order()

            # Получаем номер заказа и закрываем модальное окно
            order_page.get_new_order_number()
            order_page.close_modal_window()

        with allure.step("Проверяем что счетчик «Выполнено за всё время» увеличился"):
            main_page.go_to_order_feed()
            all_orders_count_finish = order_page.get_all_orders_counter()

        assert all_orders_count_finish > all_orders_count_initially, \
            f"Счетчик за все время не увеличился. Было: {all_orders_count_initially}, стало: {all_orders_count_finish}"

    @allure.title("Проверка при создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_order_counter_today_increases(self, driver, login_setup):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        with allure.step("Идем на страницу заказов и получаем значение счетчика «Выполнено за сегодня»"):
            main_page.go_to_order_feed()
            today_orders_count_initially = order_page.get_today_orders_counter()

        with allure.step("Создаем новый заказ"):
            main_page.click_constructor()
            main_page.add_ingredients_to_order()
            main_page.make_order()

            # Получаем номер заказа и закрываем модальное окно
            order_page.get_new_order_number()
            order_page.close_modal_window()

        with allure.step("Проверяем что счетчик «Выполнено за сегодня» увеличился"):
            main_page.go_to_order_feed()
            today_orders_count_finish = order_page.get_today_orders_counter()

        assert today_orders_count_finish > today_orders_count_initially, \
            f"Счетчик за сегодня не увеличился. Было: {today_orders_count_initially}, стало: {today_orders_count_finish}"

    @allure.title("Проверка после оформления заказа его номер появляется в разделе «В работе»")
    def test_order_appears_in_progress_section(self, driver, login_setup):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        with allure.step("Создаем новый заказ"):
            main_page.click_constructor()
            main_page.add_ingredients_to_order()
            main_page.make_order()

            # Получаем номер заказа
            order_number = order_page.get_new_order_number()
            logger.info(f"Создан заказ с номером: {order_number}")

            # Закрываем модальное окно
            order_page.close_modal_window()

        with allure.step("Идем на страницу заказов и проверяем что заказ в разделе «В работе»"):
            main_page.go_to_order_feed()

            # Используем динамический локатор для поиска заказа
            method, locator = OrderFeedPageLocators.ORDER_IN_PROGRESS_BY_NUMBER
            dynamic_locator = (method, locator.format(order_number))

            # Проверяем что элемент найден
            element = order_page.wait_for_element(dynamic_locator, timeout=30)
            assert element is not None, f"Элемент заказа {order_number} не найден"
            assert element.is_displayed(), f"Элемент заказа {order_number} не отображается"

            logger.info(f"Заказ {order_number} найден в разделе «В работе»")