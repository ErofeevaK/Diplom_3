import allure
import logging
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from locators.order_feed_page_locators import OrderFeedPageLocators
from locators.main_page_locators import MainPageLocators

logger = logging.getLogger(__name__)


class TestOrderFeed:
    @allure.title("Проверка открытия модального окна с деталями заказа")
    def test_click_order_opens_modal_window(self, driver, login):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Ждем появления заказов в ленте
        order_page.wait_for_orders_to_appear()

        # Используем element_is_clickable
        first_order_element = order_page.element_is_clickable(OrderFeedPageLocators.FIRST_ORDER_ITEM)

        # Кликаем на первый заказ
        order_page.click_js(first_order_element)

        # Пробуем разные локаторы для модального окна
        try:
            # Сначала пробуем основной локатор
            assert order_page.wait_for_element(OrderFeedPageLocators.MODAL_WINDOW,
                                               timeout=10), "Модальное окно не открылось"
        except:
            # Если не нашли, пробуем альтернативный локатор
            try:
                assert order_page.wait_for_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER,
                                                   timeout=5), "Модальное окно не открылось (альтернативный локатор)"
            except:
                # Если и это не сработало, проверяем любой модальный элемент
                modal_elements = order_page.find_elements(OrderFeedPageLocators.MODAL_WINDOW)
                assert len(modal_elements) > 0, "Модальное окно не открылось (нет элементов)"

    @allure.title("Проверка отображения заказа пользователя из Истории заказов в Ленте заказов")
    def test_displaying_order_from_history_in_feed_success(self, driver, login):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        # Создаем заказ (добавляем ингредиенты, включая булку)
        logger.info("Добавляем ингредиенты в заказ")
        main_page.add_ingredients_to_order()

        # ПРОВЕРКА: убеждаемся что кнопка заказа активна
        order_button = main_page.wait_for_element(MainPageLocators.ORDER_BUTTON)
        assert order_button.is_enabled(), "Кнопка 'Оформить заказ' не активна - возможно не добавлена булка"

        logger.info("Нажимаем кнопку 'Оформить заказ'")
        main_page.make_order()

        # Ждем обработки заказа (ждем пока заглушка 9999 сменится на реальный номер)
        logger.info("Ждем обработки заказа...")
        order_number = order_page.wait_for_order_processing()
        logger.info(f"Создан заказ с номером: {order_number}")

        # Проверяем что это не заглушка
        assert order_number != "9999", "Заказ не обработан - осталась заглушка 9999"
        assert order_number is not None, "Номер заказа не получен"

        order_page.close_modal_window()

        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Ждем появления заказов
        order_page.wait_for_orders_to_appear()

        # Ждем пока заказ появится в ленте с помощью кастомного условия
        order_page.wait_for_order_in_feed(order_number)

        # Проверяем что заказ есть в ленте
        orders_numbers = order_page.find_orders_list()
        logger.info(f"Заказы в ленте: {orders_numbers}")

        assert order_number in orders_numbers, f"Созданный заказ {order_number} не найден в ленте заказов. Найдены: {orders_numbers}"

    @allure.title("Проверка увеличения счетчика Выполнено за все время при создании нового заказа")
    def test_order_counter_all_time_increases(self, driver, login):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Получаем начальное значение счетчика
        initial_counter = order_page.get_all_orders_counter()
        logger.info(f"Начальное значение счетчика за все время: {initial_counter}")

        # Создаем заказ (добавляем ингредиенты, включая булку)
        main_page.click_constructor()
        main_page.add_ingredients_to_order()  # Этот метод должен добавлять булку и другие ингредиенты
        main_page.make_order()

        # Ждем обработки заказа (ждем пока заглушка 9999 сменится на реальный номер)
        order_page.wait_for_order_processing()
        order_page.close_modal_window()

        # Проверяем что счетчик увеличился
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Ждем увеличения счетчика с помощью кастомного условия
        order_page.wait_for_counter_increase(
            OrderFeedPageLocators.ALL_ORDERS_LOCATOR,
            initial_counter,
            timeout=15
        )

        updated_counter = order_page.get_all_orders_counter()
        logger.info(f"Обновленное значение счетчика за все время: {updated_counter}")

        assert updated_counter > initial_counter, f"Счетчик за все время не увеличился: было {initial_counter}, стало {updated_counter}"

    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    def test_order_counter_today_increases(self, driver, login):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        # Переходим в ленту заказов
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Получаем начальное значение счетчика
        initial_counter = order_page.get_today_orders_counter()
        logger.info(f"Начальное значение счетчика за сегодня: {initial_counter}")

        # Создаем заказ (добавляем ингредиенты, включая булку)
        main_page.click_constructor()
        main_page.add_ingredients_to_order()  # Этот метод должен добавлять булку и другие ингредиенты
        main_page.make_order()

        # Ждем обработки заказа (ждем пока заглушка 9999 сменится на реальный номер)
        order_page.wait_for_order_processing()
        order_page.close_modal_window()

        # Проверяем что счетчик увеличился
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Ждем увеличения счетчика с помощью кастомного условия
        order_page.wait_for_counter_increase(
            OrderFeedPageLocators.TODAY_ORDERS_LOCATOR,
            initial_counter,
            timeout=15
        )

        updated_counter = order_page.get_today_orders_counter()
        logger.info(f"Обновленное значение счетчика за сегодня: {updated_counter}")

        assert updated_counter > initial_counter, f"Счетчик за сегодня не увеличился: было {initial_counter}, стало {updated_counter}"

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    def test_order_appears_in_progress_section(self, driver, login):
        main_page = MainPage(driver)
        order_page = OrderFeedPage(driver)

        # Создаем заказ
        main_page.click_constructor()
        main_page.add_ingredients_to_order()
        main_page.make_order()

        # Получаем номер заказа
        order_number = order_page.wait_for_order_processing()
        logger.info(f"Создан заказ с номером: {order_number}")

        order_page.close_modal_window()

        with allure.step("Идем на страницу заказов и проверяем заказ в разделе 'В работе'"):
            # Переходим в ленту заказов
            main_page.click_order_feed()
            order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

            # Используем динамический локатор
            method, locator = OrderFeedPageLocators.ORDER_IN_PROGRESS_BY_NUMBER
            dynamic_locator = (method, locator.format(order_number))

            # Проверяем что элемент найден
            assert order_page.wait_for_element(dynamic_locator, timeout=30), \
                f"Заказ {order_number} не найден в разделе 'В работе'"

            logger.info(f" Заказ {order_number} найден в разделе 'В работе'")