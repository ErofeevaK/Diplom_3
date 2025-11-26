import allure
import logging
from selenium.common.exceptions import TimeoutException
from locators.order_feed_page_locators import OrderFeedPageLocators
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class OrderFeedPage(BasePage):

    @allure.step("Открыть страницу ленты заказов")
    def open_feed_page(self):
        """Открытие страницы ленты заказов"""
        self.driver.get("https://your-app.com/feed")
        logger.info("Страница ленты заказов открыта")

    # ========== ОСНОВНЫЕ ДЕЙСТВИЯ ==========

    @allure.step("Кликаем по последнему заказу")
    def click_last_order(self):
        """Клик по последнему заказу в ленте для открытия модального окна"""
        try:
            # Ждем появления хотя бы одного заказа в ленте
            self.wait_for_orders_to_appear(timeout=10)

            # Кликаем по первому (последнему) заказу в списке
            last_order = self.wait_for_element(OrderFeedPageLocators.FIRST_ORDER_ITEM, timeout=5)
            self.click_js(last_order)
            logger.info("Кликнут последний заказ в ленте")

        except TimeoutException:
            logger.error("Не удалось кликнуть по последнему заказу")
            raise

    @allure.step("Нажать кнопку 'Оформить заказ'")
    def click_place_in_order(self):
        """Клик по кнопке оформления заказа"""
        try:
            order_button = self.wait_for_element(MainPageLocators.MAKE_ORDER_BUTTON, timeout=10)
            self.click_js(order_button)
            logger.info("Нажата кнопка 'Оформить заказ'")
        except TimeoutException:
            logger.error("Не удалось найти кнопку 'Оформить заказ'")
            raise

    @allure.step("Закрыть детали заказа")
    def click_close_order_details(self):
        """Закрытие модального окна с деталями заказа"""
        try:
            close_btn = self.wait_for_element(OrderFeedPageLocators.MODAL_CLOSE_ORDER, timeout=5)
            self.click_js(close_btn)
            logger.info("Детали заказа закрыты")

            # Ждем пока модальное окно закроется
            self.element_is_not_visible(OrderFeedPageLocators.MODAL_WINDOW, timeout=5)

        except TimeoutException:
            logger.error("Не удалось закрыть детали заказа")
            raise

    @allure.step("Закрыть модальное окно")
    def close_modal_window(self):
        # 1. Пытаемся закрыть через overlay
        try:
            overlay = self.element_is_clickable(OrderFeedPageLocators.MODAL_OVERLAY_LOCATOR, timeout=5)
            self.click_js(overlay)
            logger.info("Модальное окно закрыто через overlay")
        except Exception as e:
            logger.warning(f"Не удалось закрыть через overlay: {e}")

            # 2. Пробуем закрыть крестиком
            try:
                close_btn = self.element_is_clickable(OrderFeedPageLocators.MODAL_CLOSE_ORDER, timeout=5)
                self.click_js(close_btn)
                logger.info("Модальное окно закрыто через крестик")
            except Exception as e2:
                logger.error(f"Не удалось закрыть через крестик: {e2}")
                raise Exception("Модальное окно НЕ закрыто")

        # 3. Обязательное ожидание: модалка исчезает
        self.element_is_not_visible(OrderFeedPageLocators.MODAL_WINDOW, timeout=10)
        logger.info("Модальное окно успешно закрыто")

    # ========== ПОЛУЧЕНИЕ ДАННЫХ ==========

    @allure.step("Получить содержимое модального окна с деталями заказа")
    def get_order_details_content(self):
        """Получение содержимого модального окна с деталями заказа"""
        try:
            # Ждем появления модального окна
            modal = self.wait_for_element(OrderFeedPageLocators.MODAL_WINDOW, timeout=5)

            # Получаем текст из модального окна
            content = modal.text
            logger.info(f"Получено содержимое модального окна, длина: {len(content)} символов")
            return content

        except TimeoutException:
            logger.error("Не удалось получить содержимое модального окна")
            return ""

    @allure.step("Получить идентификатор заказа из деталей")
    def get_order_id_from_details(self):
        """Получение номера заказа из модального окна деталей"""
        try:
            order_id_element = self.wait_for_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER, timeout=10)
            order_id = order_id_element.text.strip()
            logger.info(f"Получен идентификатор заказа: {order_id}")
            return order_id
        except TimeoutException:
            logger.error("Не удалось получить идентификатор заказа")
            return ""

    @allure.step("Получить номер нового заказа из модального окна")
    def get_new_order_number(self):
        # Ждем пока в модальном окне появится реальный номер заказа (не заглушка)
        def wait_for_real_order_number(driver):
            try:
                order_number_element = self.wait_for_element(OrderFeedPageLocators.MODAL_ORDER_NUMBER, timeout=2)
                order_text = order_number_element.text.strip()
                # Проверяем что это не заглушка (например, не "9999" или другие тестовые значения)
                if order_text and order_text.isdigit() and len(order_text) >= 4 and order_text != "9999":
                    # Нормализуем номер: убираем ведущие нули для сравнения
                    normalized_number = order_text.lstrip('0')
                    logger.info(f"Получен реальный номер заказа: {order_text} -> {normalized_number}")
                    return normalized_number
                return False
            except:
                return False

        # Ждем появления реального номера заказа
        logger.info("Ожидаем появления реального номера заказа в модальном окне")
        real_order_number = self.wait_for_custom_condition(
            wait_for_real_order_number,
            timeout=30
        )

        return real_order_number

    @allure.step("Получить список номеров заказов в ленте")
    def find_orders_list(self):
        try:
            order_elements = self.find_elements(OrderFeedPageLocators.ORDER_NUMBERS)
            orders = []
            for element in order_elements:
                text = element.text.strip()
                if text and text.startswith('#'):
                    # Нормализуем номер: убираем # и ведущие нули
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
        try:
            # Ждем появления списка заказов в работе
            self.wait_for_element(OrderFeedPageLocators.ORDERS_AT_WORK, timeout=5)

            # Получаем все элементы заказов в работе
            order_elements = self.find_elements(OrderFeedPageLocators.ORDERS_AT_WORK)

            if not order_elements:
                logger.info("В разделе 'В работе' нет заказов")
                return []

            # Извлекаем номера заказов из текста элементов
            order_numbers = []
            for element in order_elements:
                text = element.text.strip()
                if text and text != "Все текущие заказы готовы!" and text.startswith('#'):
                    # Нормализуем номер: убираем # и ведущие нули
                    order_number = text.lstrip('#').lstrip('0')
                    order_numbers.append(order_number)
                    logger.info(f"Найден заказ в работе: {text} -> {order_number}")

            logger.info(f"Найдено заказов в работе: {len(order_numbers)}")
            return order_numbers

        except TimeoutException:
            logger.info("Список заказов в работе не найден (таймаут)")
            return []
        except Exception as e:
            logger.error(f"Ошибка при получении заказов в работе: {e}")
            return []

    @allure.step("Получить значение счетчика за все время")
    def get_all_orders_counter(self):
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
        try:
            counter_text = self.get_element_text(OrderFeedPageLocators.TODAY_ORDERS_LOCATOR)
            digits = ''.join([char for char in counter_text if char.isdigit()])
            counter_value = int(digits) if digits else 0
            logger.info(f"Счетчик за сегодня: {counter_value}")
            return counter_value
        except Exception as e:
            logger.error(f"Ошибка при получении счетчика за сегодня: {e}")
            return 0

    @allure.step("Получить номер заказа в разделе 'В работе'")
    def get_order_id_in_progress_list(self):
        """Получить номер первого заказа в разделе 'В работе'"""
        try:
            orders = self.get_orders_in_progress_list()
            if orders:
                logger.info(f"Первый заказ в работе: {orders[0]}")
                return orders[0]
            else:
                logger.info("В разделе 'В работе' нет заказов")
                return "Все текущие заказы готовы!"
        except Exception as e:
            logger.error(f"Ошибка при получении заказа в работе: {e}")
            return "Все текущие заказы готовы!"

    # ========== ЯВНЫЕ ОЖИДАНИЯ (СПЕЦИФИЧНЫЕ ДЛЯ ЛЕНТЫ ЗАКАЗОВ) ==========

    @allure.step("Ждать появления заказов в ленте")
    def wait_for_orders_to_appear(self, timeout=10):
        """Ждет появления хотя бы одного заказа в ленте"""
        logger.info("Ожидаем появления заказов в ленте")
        try:
            return self.wait_for_custom_condition(
                lambda driver: len(self.find_orders_list()) > 0,
                timeout=timeout
            )
        except TimeoutException:
            logger.error(f"Заказы не появились в ленте за {timeout} секунд")
            raise

    @allure.step("Ждать появления конкретного заказа в разделе 'В работе'")
    def wait_for_order_in_progress(self, order_number, timeout=60):  # Увеличили до 60 секунд
        """Ждет пока заказ появится в разделе 'В работе'"""
        logger.info(f"Ожидаем появления заказа {order_number} в разделе 'В работе' (таймаут: {timeout}сек)")

        def order_in_progress(driver):
            try:
                current_orders = self.get_orders_in_progress_list()
                logger.info(f"Текущие заказы в работе: {current_orders}")
                is_found = order_number in current_orders
                if is_found:
                    logger.info(f"Заказ {order_number} найден в разделе 'В работе'")
                return is_found
            except Exception as e:
                logger.warning(f"Ошибка при получении заказов в работе: {e}")
                return False

        try:
            return self.wait_for_custom_condition(
                order_in_progress,
                timeout=timeout
            )
        except TimeoutException:
            # Получаем финальный список для отладки
            final_orders = self.get_orders_in_progress_list()
            logger.error(
                f"Заказ {order_number} не появился в разделе 'В работе' за {timeout} секунд. Текущие заказы: {final_orders}")
            raise TimeoutException(
                f"Заказ {order_number} не появился в разделе 'В работе'. Последние заказы: {final_orders}")

    @allure.step("Ждать увеличения счетчика")
    def wait_for_counter_increase(self, counter_locator, initial_value, timeout=15):  # Увеличиваем таймаут
        """Ждет увеличения значения счетчика"""
        logger.info(f"Ожидаем увеличения счетчика. Текущее значение: {initial_value}")

        def counter_increased(driver):
            try:
                if counter_locator == OrderFeedPageLocators.ALL_ORDERS_LOCATOR:
                    current_value = self.get_all_orders_counter()
                else:
                    current_value = self.get_today_orders_counter()
                logger.info(f"Текущее значение счетчика: {current_value}")
                return current_value > initial_value
            except Exception as e:
                logger.warning(f"Ошибка при получении счетчика: {e}")
                return False

        try:
            return self.wait_for_custom_condition(
                counter_increased,
                timeout=timeout
            )
        except TimeoutException:
            # Получаем финальное значение для отладки
            if counter_locator == OrderFeedPageLocators.ALL_ORDERS_LOCATOR:
                final_value = self.get_all_orders_counter()
            else:
                final_value = self.get_today_orders_counter()
            logger.error(f"Счетчик не увеличился за {timeout} секунд. Было: {initial_value}, стало: {final_value}")
            raise

    @allure.step("Дождаться обработки заказа и получить номер")
    def wait_for_order_processing(self, timeout=30):
        """Ждет пока заказ обработается и возвращает реальный номер"""
        # Ждем пока модальное окно откроется
        self.wait_for_element(OrderFeedPageLocators.MODAL_WINDOW, timeout=10)
        logger.info("Модальное окно заказа открылось")

        # Используем существующий метод get_new_order_number, который уже ждет реальный номер
        order_number = self.get_new_order_number()
        logger.info(f"Заказ обработан, получен номер: {order_number}")
        return order_number

    @allure.step("Ждать исчезновения статусного текста")
    def wait_for_status_text_to_disappear(self, timeout=10):
        """Ждет пока текст 'Все текущие заказы готовы!' исчезнет"""
        logger.info("Ожидаем исчезновения текста 'Все текущие заказы готовы!'")
        try:
            self.wait_until_text_is_not_visible(
                OrderFeedPageLocators.STATUS_READY_TEXT,
                "Все текущие заказы готовы!",
                timeout
            )
            logger.info("Текст 'Все текущие заказы готовы!' исчез")
        except TimeoutException:
            logger.info("Текст 'Все текущие заказы готовы!' не исчез в течение таймаута")

    # ========== ПРОВЕРКИ ==========

    @allure.step("Проверить, что заказ отображается в ленте заказов")
    def is_order_id_in_feed(self, order_id):
        """Проверка наличия идентификатора заказа в ленте заказов"""
        try:
            # Получаем все заказы из ленты
            orders_in_feed = self.find_orders_list()

            # Проверяем наличие заказа
            is_found = order_id in orders_in_feed
            logger.info(f"Заказ {order_id} найден в ленте: {is_found}")

            return is_found

        except Exception as e:
            logger.error(f"Ошибка при проверке заказа в ленте: {e}")
            return False

    @allure.step("Ждать появления заказа в ленте")
    def wait_for_order_in_feed(self, order_number, timeout=15):
        """Ждет пока заказ появится в ленте заказов"""
        logger.info(f"Ожидаем появления заказа {order_number} в ленте")

        def order_in_feed(driver):
            orders = self.find_orders_list()
            is_found = order_number in orders
            if is_found:
                logger.info(f"Заказ {order_number} найден в ленте")
            return is_found

        try:
            return self.wait_for_custom_condition(
                order_in_feed,
                timeout=timeout
            )
        except TimeoutException:
            final_orders = self.find_orders_list()
            logger.error(f"Заказ {order_number} не появился в ленте за {timeout} секунд. Текущие заказы: {final_orders}")
            raise

        pass
