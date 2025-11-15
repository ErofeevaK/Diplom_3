import allure

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Подождать загрузки страницы и проверить URL")
    def wait_for_url(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.url_contains(locator))

    @allure.step("Проверка существования элемента")
    def element_is_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

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

    @allure.step("Кликнуть на элемент")
    def click_element(self, locator, timeout=10):
        element = self.element_is_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Клик по элементу через JavaScript")
    def click_js(self, element):
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввести текст в поле ввода")
    def input_text(self, locator, text):
        element = self.element_is_visible(locator)  # Уже содержит распаковку
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
    def wait_and_find_element(self, locator):
        WebDriverWait(self.driver, 5).until(expected_conditions.visibility_of_element_located(locator))
        return self.driver.find_element(*locator)

    @allure.step("Ждем пока указанный текст перестанет отображаться в элементе")
    def wait_until_text_is_not_visible(self, locator, text, timeout=10):
        WebDriverWait(self.driver, timeout).until_not(EC.text_to_be_present_in_element(locator, text))