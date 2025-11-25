import allure
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Подождать загрузки страницы и проверить URL")
    def wait_for_url(self, url, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(url))

    @allure.step("Проверка существования элемента")
    def element_is_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    @allure.step("Подождать видимости элемента")
    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    @allure.step("Подождать готовности элемента к клику")
    def element_is_clickable(self, locator, timeout=5):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    @allure.step("Скролл до элемента")
    def scroll_to_element(self, locator):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        return element

    # ========== ДЕЙСТВИЯ ==========

    @allure.step("Клик по элементу через JavaScript")
    def click_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Перетащить элемент")
    def drag_and_drop(self, source_locator, target_locator):
        """
        Перетаскивает элемент из source_locator в target_locator с использованием JavaScript.
        :param source_locator: Локатор элемента, который нужно перетащить.
        :param target_locator: Локатор элемента, куда нужно перетащить.
        """
        # Ждем появления элементов
        self.wait_for_element(source_locator)
        self.wait_for_element(target_locator)

        element_from = self.driver.find_element(*source_locator)
        element_to = self.driver.find_element(*target_locator)

        self.driver.execute_script("""
            var source = arguments[0];
            var target = arguments[1];

            // Создаем и инициируем событие dragstart
            var dragStartEvent = new DragEvent('dragstart', {
                bubbles: true,
                cancelable: true,
                dataTransfer: new DataTransfer()
            });
            source.dispatchEvent(dragStartEvent);

            // Создаем и инициируем событие dragenter
            var dragEnterEvent = new DragEvent('dragenter', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            target.dispatchEvent(dragEnterEvent);

            // Создаем и инициируем событие dragover
            var dragOverEvent = new DragEvent('dragover', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            target.dispatchEvent(dragOverEvent);

            // Создаем и инициируем событие drop
            var dropEvent = new DragEvent('drop', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            target.dispatchEvent(dropEvent);

            // Создаем и инициируем событие dragend
            var dragEndEvent = new DragEvent('dragend', {
                bubbles: true,
                cancelable: true,
                dataTransfer: dragStartEvent.dataTransfer
            });
            source.dispatchEvent(dragEndEvent);
        """, element_from, element_to)

        logger.info("Элемент успешно перетащен с помощью JavaScript")

    @allure.step("Ввести текст в поле ввода")
    def input_text(self, locator, text):
        element = self.element_is_visible(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента")
    def get_element_text(self, locator):
        return self.wait_for_element(locator).text

    @allure.step("Вернуть текущий URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Проверить, что элемент не виден")
    def element_is_not_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    @allure.step("Проверить, появление элемента, поиск и возврат элемента")
    def wait_and_find_element(self, locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    @allure.step("Ждем пока указанный текст перестанет отображаться в элементе")
    def wait_until_text_is_not_visible(self, locator, text, timeout=10):
        WebDriverWait(self.driver, timeout).until_not(EC.text_to_be_present_in_element(locator, text))

    @allure.step("Ждать выполнения кастомного условия")
    def wait_for_custom_condition(self, condition, timeout=10):
        return WebDriverWait(self.driver, timeout).until(condition)

    @allure.step("Найти все элементы по локатору")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step("Ждать пока элемент исчезнет из DOM")
    def wait_for_element_to_disappear(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.staleness_of(self.driver.find_element(*locator)))