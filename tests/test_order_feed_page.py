import allure
import logging
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from locators.order_feed_page_locators import OrderFeedPageLocators
from locators.main_page_locators import MainPageLocators
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

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

        # Переходим в ленту заказов чтобы увидеть начальное состояние
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Ждем загрузки раздела "В работе"
        order_page.wait_for_element(OrderFeedPageLocators.ORDERS_AT_WORK, timeout=10)

        # ДИАГНОСТИКА: смотрим как выглядят существующие заказы в разделе "В работе"
        logger.info("=== ДИАГНОСТИКА ФОРМАТА НОМЕРОВ ЗАКАЗОВ ===")
        try:
            # Ищем все заказы в разделе "В работе"
            all_orders = order_page.find_elements((By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li"))
            logger.info(f"Найдено заказов в разделе 'В работе': {len(all_orders)}")

            for i, order_elem in enumerate(all_orders):
                order_text = order_elem.text.strip()
                logger.info(f"Заказ {i}: '{order_text}'")
                logger.info(f"HTML заказа {i}: {order_elem.get_attribute('outerHTML')}")

        except Exception as e:
            logger.warning(f"Не удалось получить заказы для диагностики: {e}")

        # Создаем заказ
        main_page.click_constructor()
        main_page.add_ingredients_to_order()
        main_page.make_order()

        # Ждем обработки заказа и получаем номер
        new_order_number = order_page.wait_for_order_processing()
        logger.info(f"Создан заказ с номером: {new_order_number}")

        # ДИАГНОСТИКА: смотрим как номер отображается в модальном окне
        try:
            order_number_element = order_page.wait_for_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER)
            modal_order_text = order_number_element.text.strip()
            logger.info(f"Номер заказа в модальном окне: '{modal_order_text}'")
        except Exception as e:
            logger.warning(f"Не удалось получить номер из модального окна: {e}")

        order_page.close_modal_window()

        # Возвращаемся в ленту заказов
        main_page.click_order_feed()
        order_page.wait_for_element(OrderFeedPageLocators.ORDER_FEED_SECTION)

        # Ждем загрузки раздела "В работе" после возврата
        order_page.wait_for_element(OrderFeedPageLocators.ORDERS_AT_WORK, timeout=10)

        # Пробуем разные форматы номера заказа
        possible_formats = [
            new_order_number,  # "12345"
            f"#{new_order_number}",  # "#12345"
            f"# {new_order_number}",  # "# 12345"
            f"00{new_order_number}",  # "0012345" (если есть ведущие нули)
        ]

        found = False
        for order_format in possible_formats:
            try:
                method, locator_template = OrderFeedPageLocators.ORDER_IN_PROGRESS_BY_NUMBER
                dynamic_locator = (method, locator_template.format(order_format))

                logger.info(f"Пробуем найти заказ в формате: '{order_format}'")
                order_element = order_page.wait_for_element(dynamic_locator, timeout=5)

                logger.info(f"Заказ найден в формате: '{order_format}'")
                assert order_element.is_displayed()
                found = True
                break

            except TimeoutException:
                logger.info(f"Формат '{order_format}' не сработал")
                continue

        if not found:
            # Если ни один формат не сработал, выводим полную диагностику
            logger.error("Ни один формат номера заказа не сработал")

            # Смотрим что сейчас в разделе "В работе"
            try:
                current_orders = order_page.find_elements(
                    (By.XPATH, "//ul[contains(@class, 'OrderFeed_orderListReady')]/li"))
                logger.info(f"Текущие заказы в разделе: {[order.text for order in current_orders]}")
            except Exception as e:
                logger.error(f"Ошибка при получении текущих заказов: {e}")

            raise AssertionError(
                f"Заказ {new_order_number} не найден в разделе 'В работе'. Испробованы форматы: {possible_formats}")