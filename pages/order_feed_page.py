import allure
import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from locators.order_feed_page_locators import OrderFeedPageLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class OrderFeedPage(BasePage):

    @allure.step("Получить номер нового заказа из модального окна")
    def get_new_order_number(self):
        """Получение номера нового заказа"""

        def wait_for_real_order_number(driver):
            try:
                order_number_element = self.wait_for_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER, timeout=2)
                order_text = order_number_element.text.strip()
                if order_text and order_text.isdigit() and len(order_text) >= 4 and order_text != "9999":
                    normalized_number = order_text.lstrip('0')
                    logger.info(f"Получен реальный номер заказа: {order_text} -> {normalized_number}")
                    return normalized_number
                return False
            except:
                return False

        logger.info("Ожидаем появления реального номера заказа в модальном окне")
        real_order_number = self.wait_for_custom_condition(
            wait_for_real_order_number,
            timeout=30
        )
        return real_order_number

    @allure.step("Закрыть модальное окно")
    def close_modal_window(self):
        """Закрытие модального окна"""
        try:
            overlay = self.element_is_clickable(OrderFeedPageLocators.MODAL_OVERLAY_LOCATOR, timeout=5)
            self.click_js(overlay)
            logger.info("Модальное окно закрыто через overlay")
        except Exception as e:
            logger.warning(f"Не удалось закрыть через overlay: {e}")
            try:
                close_btn = self.element_is_clickable(OrderFeedPageLocators.MODAL_CLOSE_ORDER, timeout=5)
                self.click_js(close_btn)
                logger.info("Модальное окно закрыто через крестик")
            except Exception as e2:
                logger.error(f"Не удалось закрыть через крестик: {e2}")
                raise Exception("Модальное окно НЕ закрыто")

        self.element_is_not_visible(OrderFeedPageLocators.MODAL_WINDOW, timeout=10)
        logger.info("Модальное окно успешно закрыто")

    @allure.step("Проверить что модальное окно заказа открылось")
    def assert_order_modal_opened(self):
        """Проверка что модальное окно заказа открылось"""
        try:
            # Пробуем разные локаторы для модального окна
            modal_opened = False

            # Сначала пробуем основной локатор
            try:
                modal = self.wait_for_element(OrderFeedPageLocators.MODAL_WINDOW, timeout=5)
                if modal and modal.is_displayed():
                    modal_opened = True
                    logger.info("Модальное окно найдено по основному локатору")
            except TimeoutException:
                logger.debug("Основной локатор модального окна не найден")

            # Если не нашли, пробуем альтернативный локатор
            if not modal_opened:
                try:
                    order_number = self.wait_for_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER, timeout=3)
                    if order_number and order_number.is_displayed():
                        modal_opened = True
                        logger.info("Модальное окно найдено по номеру заказа")
                except TimeoutException:
                    logger.debug("Локатор номера заказа не найден")

            # Если и это не сработало, проверяем любой модальный элемент
            if not modal_opened:
                modal_elements = self.find_elements(OrderFeedPageLocators.MODAL_WINDOW)
                modal_opened = len(modal_elements) > 0
                if modal_opened:
                    logger.info("Найдены элементы модального окна")

            assert modal_opened, "Модальное окно не открылось"
            logger.info("Модальное окно заказа успешно открылось")

        except Exception as e:
            logger.error(f"Ошибка при проверке модального окна заказа: {e}")
            raise AssertionError(f"Модальное окно заказа не открылось: {e}")

    @allure.step("Проверить что модальное окно закрылось")
    def assert_modal_closed(self):
        """Проверка что модальное окно закрылось"""
        try:
            self.assert_element_not_visible(OrderFeedPageLocators.MODAL_WINDOW, "модальное окно заказа", timeout=10)
            logger.info("Модальное окно заказа успешно закрыто")
        except Exception as e:
            logger.error(f"Ошибка при проверке закрытия модального окна: {e}")
            raise AssertionError("Модальное окно заказа не закрылось")

    @allure.step("Получить значение счетчика за все время")
    def get_all_orders_counter(self):
        """Получение значения счетчика за все время"""
        try:
            counter_text = self.get_element_text(OrderFeedPageLocators.ALL_ORDERS_LOCATOR)
            digits = ''.join([char for char in counter_text if char.isdigit()])
            counter_value = int(digits) if digits else 0
            logger.info(f"Счетчик за все время: {counter_value}")
            return counter_value
        except Exception as e:
            logger.error(f"Ошибка при получении счетчика за все время: {e}")
            return 0

    @allure.step("Получить значение счетчика за сегодня")
    def get_today_orders_counter(self):
        """Получение значения счетчика за сегодня"""
        try:
            counter_text = self.get_element_text(OrderFeedPageLocators.TODAY_ORDERS_LOCATOR)
            digits = ''.join([char for char in counter_text if char.isdigit()])
            counter_value = int(digits) if digits else 0
            logger.info(f"Счетчик за сегодня: {counter_value}")
            return counter_value
        except Exception as e:
            logger.error(f"Ошибка при получении счетчика за сегодня: {e}")
            return 0


    @allure.step("Проверить что лента заказов загрузилась")
    def assert_feed_loaded(self):
        """Проверка что лента заказов загрузилась"""
        try:
            self.assert_element_visible(OrderFeedPageLocators.ORDER_FEED_SECTION, "раздел ленты заказов", timeout=10)
            logger.info("Лента заказов успешно загрузилась")
        except Exception as e:
            logger.error(f"Ошибка при проверке загрузки ленты заказов: {e}")
            raise AssertionError("Лента заказов не загрузилась")

    @allure.step("Ждать появления заказов в ленте")
    def wait_for_orders_to_appear(self, timeout=10):
        """Ожидание появления заказов в ленте"""
        logger.info("Ожидаем появления заказов в ленте")
        try:
            return self.wait_for_custom_condition(
                lambda driver: len(self.find_orders_list()) > 0,
                timeout=timeout
            )
        except TimeoutException:
            logger.error(f"Заказы не появились в ленте за {timeout} секунд")
            raise

    @allure.step("Получить список номеров заказов в ленте")
    def find_orders_list(self):
        """Получение списка номеров заказов в ленте"""
        try:
            order_elements = self.find_elements(OrderFeedPageLocators.ORDER_NUMBERS)
            orders = []
            for element in order_elements:
                text = element.text.strip()
                if text and text.startswith('#'):
                    order_number = text.lstrip('#').lstrip('0')
                    orders.append(order_number)
                    logger.info(f"Найден заказ в ленте: {text} -> {order_number}")

            logger.info(f"Всего найдено заказов в ленте: {len(orders)}")
            return orders
        except Exception as e:
            logger.error(f"Ошибка при получении списка заказов: {e}")
            return []

    @allure.step("Получить номера заказов в разделе В работе")
    def get_orders_in_progress_list(self):
        """Получение списка заказов в работе"""
        try:
            self.wait_for_element(OrderFeedPageLocators.ORDERS_AT_WORK, timeout=5)
            order_elements = self.find_elements(OrderFeedPageLocators.ORDERS_IN_PROGRESS)

            if not order_elements:
                logger.info("В разделе 'В работе' нет заказов")
                return []

            order_numbers = []
            for element in order_elements:
                try:
                    if element.is_displayed():
                        text = element.text.strip()
                        if text and text != "Все текущие заказы готовы!":
                            order_number = text.lstrip('#').lstrip('0')
                            order_numbers.append(order_number)
                            logger.info(f"Найден заказ в работе: {text} -> {order_number}")
                except Exception as e:
                    logger.debug(f"Ошибка при обработке элемента: {e}")
                    continue

            logger.info(f"Найдено заказов в работе: {len(order_numbers)}")
            return order_numbers
        except TimeoutException:
            logger.info("Список заказов в работе не найден (таймаут)")
            return []
        except Exception as e:
            logger.error(f"Ошибка при получении заказов в работе: {e}")
            return []


    @allure.step("Дождаться обработки заказа и получить номер")
    def wait_for_order_processing(self, timeout=30):
        """Ожидание обработки заказа и получение номера"""
        self.wait_for_element(OrderFeedPageLocators.MODAL_WINDOW, timeout=10)
        logger.info("Модальное окно заказа открылось")
        order_number = self.get_new_order_number()
        logger.info(f"Заказ обработан, получен номер: {order_number}")
        return order_number

    @allure.step("Проверить что заказ появился в разделе 'В работе'")
    def assert_order_in_progress(self, order_number, timeout=30):
        """Проверка что заказ появился в разделе 'В работе'"""
        try:
            # Используем динамический локатор
            method, locator = OrderFeedPageLocators.ORDER_IN_PROGRESS_BY_NUMBER
            dynamic_locator = (method, locator.format(order_number))

            # Проверяем что элемент найден
            element = self.wait_for_element(dynamic_locator, timeout=timeout)
            assert element is not None, f"Элемент заказа {order_number} не найден"
            assert element.is_displayed(), f"Элемент заказа {order_number} не отображается"

            logger.info(f"Заказ {order_number} найден в разделе 'В работе'")

        except Exception as e:
            logger.error(f"Ошибка при проверке заказа в разделе 'В работе': {e}")
            raise AssertionError(f"Заказ {order_number} не найден в разделе 'В работе': {e}")