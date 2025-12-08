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

    @allure.step("Проверить видимость элемента")
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

    @allure.step("Проверить, что элемент не виден")
    def element_is_not_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))


    @allure.step("Проверить наличие элемента")
    def assert_element_visible(self, locator, element_name="элемент", timeout=10):
        """Проверка что элемент видим на странице"""
        try:
            element = self.wait_for_element(locator, timeout)
            assert element is not None, f"Элемент '{element_name}' не найден"
            assert element.is_displayed(), f"Элемент '{element_name}' не отображается"
            logger.info(f"Элемент '{element_name}' видим на странице")
            return element
        except Exception as e:
            logger.error(f"Ошибка при проверке элемента '{element_name}': {e}")
            self.take_screenshot(f"element_not_found_{element_name}")
            raise AssertionError(f"Элемент '{element_name}' не видим на странице: {e}")

    @allure.step("Проверить что элемент отсутствует")
    def assert_element_not_visible(self, locator, element_name="элемент", timeout=5):
        """Проверка что элемент отсутствует на странице"""
        try:
            self.element_is_not_visible(locator, timeout)
            logger.info(f"Элемент '{element_name}' отсутствует на странице")
        except TimeoutException:
            error_msg = f"Элемент '{element_name}' все еще присутствует на странице"
            logger.error(error_msg)
            self.take_screenshot(f"element_still_present_{element_name}")
            raise AssertionError(error_msg)

    @allure.step("Проверить что элемент кликабелен")
    def assert_element_clickable(self, locator, element_name="элемент", timeout=5):
        """Проверка что элемент кликабелен"""
        try:
            element = self.element_is_clickable(locator, timeout)
            assert element is not None, f"Элемент '{element_name}' не кликабелен"
            logger.info(f"Элемент '{element_name}' кликабелен")
            return element
        except Exception as e:
            logger.error(f"Ошибка при проверке кликабельности элемента '{element_name}': {e}")
            self.take_screenshot(f"element_not_clickable_{element_name}")
            raise AssertionError(f"Элемент '{element_name}' не кликабелен: {e}")

    @allure.step("Проверить URL страницы")
    def assert_url_contains(self, expected_text, timeout=10):
        """Проверка что URL содержит ожидаемый текст"""
        try:
            self.wait_for_url(expected_text, timeout)
            current_url = self.get_current_url()
            logger.info(f"URL содержит '{expected_text}': {current_url}")
        except Exception as e:
            current_url = self.get_current_url()
            error_msg = f"URL не содержит '{expected_text}'. Текущий URL: {current_url}"
            logger.error(error_msg)
            self.take_screenshot(f"url_not_contains_{expected_text}")
            raise AssertionError(error_msg)

    @allure.step("Проверить наличие текста в элементе")
    def assert_text_in_element(self, locator, expected_text, element_name="элемент", timeout=5):
        """Проверка что элемент содержит ожидаемый текст"""
        try:
            element = self.wait_for_element(locator, timeout)
            actual_text = element.text.strip()
            assert expected_text in actual_text, \
                f"Текст не найден в '{element_name}'. Ожидалось: '{expected_text}', получено: '{actual_text}'"
            logger.info(f"Текст '{expected_text}' найден в элементе '{element_name}'")
        except Exception as e:
            logger.error(f"Ошибка при проверке текста в элементе '{element_name}': {e}")
            self.take_screenshot(f"text_not_found_{element_name}")
            raise AssertionError(f"Текст '{expected_text}' не найден в элементе '{element_name}': {e}")

    @allure.step("Проверить что элемент содержит класс")
    def assert_element_has_class(self, locator, class_name, element_name="элемент"):
        """Проверка что элемент содержит определенный CSS класс"""
        try:
            element = self.wait_for_element(locator)
            element_classes = element.get_attribute("class") or ""
            assert class_name in element_classes, \
                f"Элемент '{element_name}' не содержит класс '{class_name}'. Классы: {element_classes}"
            logger.info(f"Элемент '{element_name}' содержит класс '{class_name}'")
        except Exception as e:
            logger.error(f"Ошибка при проверке класса элемента '{element_name}': {e}")
            raise AssertionError(f"Элемент '{element_name}' не содержит класс '{class_name}': {e}")

    @allure.step("Проверить что элемент выбран")
    def assert_element_selected(self, locator, element_name="элемент", timeout=5):
        """Проверка что элемент выбран (для чекбоксов, радиокнопок)"""
        try:
            element = self.wait_for_element(locator, timeout)
            assert element.is_selected(), f"Элемент '{element_name}' не выбран"
            logger.info(f"Элемент '{element_name}' выбран")
        except Exception as e:
            logger.error(f"Ошибка при проверке выбранного элемента '{element_name}': {e}")
            raise AssertionError(f"Элемент '{element_name}' не выбран: {e}")

    @allure.step("Проверить количество элементов")
    def assert_elements_count(self, locator, expected_count, element_name="элементов", timeout=5):
        """Проверка количества элементов на странице"""
        try:
            elements = self.find_elements(locator)
            actual_count = len(elements)
            assert actual_count == expected_count, \
                f"Неверное количество {element_name}. Ожидалось: {expected_count}, найдено: {actual_count}"
            logger.info(f"Количество {element_name}: {actual_count} (ожидалось: {expected_count})")
        except Exception as e:
            logger.error(f"Ошибка при проверке количества элементов '{element_name}': {e}")
            raise AssertionError(f"Неверное количество {element_name}: {e}")


    @allure.step("Клик по элементу через JavaScript")
    def click_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

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

    @allure.step("Сделать скриншот")
    def take_screenshot(self, screenshot_name):
        """Сделать скриншот и прикрепить к allure отчету"""
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Найти все элементы по локатору")
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)


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

    @allure.step("Ждать пока элемент исчезнет из DOM")
    def wait_for_element_to_disappear(self, locator, timeout=10):
        element = self.driver.find_element(*locator)
        return WebDriverWait(self.driver, timeout).until(EC.staleness_of(element))

    @allure.step("Ожидание присутствия элемента в DOM")
    def wait_for_presence_of_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    @allure.step("Ожидание появления текста в элементе")
    def wait_for_text_in_element(self, locator, text, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.text_to_be_present_in_element(locator, text))

    @allure.step("Проверка что элемент выбран/активен")
    def element_is_selected(self, locator, timeout=5):
        element = self.driver.find_element(*locator)
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_selected(element))

    @allure.step("Ожидание видимости всех элементов")
    def wait_for_all_elements_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_all_elements_located(locator))

    @allure.step("Ожидание появления alert")
    def wait_for_alert(self, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.alert_is_present())

    @allure.step("Получить значение атрибута элемента")
    def get_element_attribute(self, locator, attribute):
        element = self.wait_for_element(locator)
        return element.get_attribute(attribute)

    @allure.step("Выполнить JavaScript код")
    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)