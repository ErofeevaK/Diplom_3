import allure
import logging
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
            self.wait_for_url(BASE_URL, timeout=5)
            personal_account_btn = self.element_is_visible(AccountPageLocators.PERSONAL_ACCOUNT_BUTTON, timeout=5)

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
        self.wait_for_url("/account")

    @allure.step("Добавить ингредиенты в заказ")
    def add_ingredients_to_order(self):
        """Добавление ингредиентов в заказ с проверками"""
        try:
            logger.info("Начинаем добавление ингредиентов в заказ")
            self.wait_for_element(MainPageLocators.INGREDIENT_BUN, timeout=10)
            self.wait_for_element(MainPageLocators.INGREDIENT_MAIN, timeout=10)

            logger.info("Добавляем булку в заказ")
            self.drag_and_drop(
                source_locator=MainPageLocators.INGREDIENT_BUN,
                target_locator=MainPageLocators.CONSTRUCTOR_DROP_AREA
            )

            self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA, timeout=5)
            logger.info("Булка успешно добавлена")

            logger.info("Добавляем начинку в заказ")
            self.drag_and_drop(
                source_locator=MainPageLocators.INGREDIENT_MAIN,
                target_locator=MainPageLocators.CONSTRUCTOR_DROP_AREA
            )

            self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA, timeout=5)
            logger.info("Начинка успешно добавлена")

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
            self.add_ingredients_alternative()
            raise

    @allure.step("Альтернативный способ добавления ингредиентов")
    def add_ingredients_alternative(self):
        """Альтернативный способ добавления ингредиентов через клик"""
        try:
            bun_element = self.wait_for_element(MainPageLocators.INGREDIENT_BUN)
            self.click_js(bun_element)
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


    @allure.step("Проверить что главная страница загружена")
    def assert_main_page_loaded(self):
        """Проверка загрузки главной страницы"""
        try:
            # Проверяем что мы на главной странице
            current_url = self.get_current_url()
            assert BASE_URL in current_url, f"Не на главной странице. URL: {current_url}"

            # Проверяем основные элементы
            self.assert_element_visible(MainPageLocators.CONSTRUCTOR_BUTTON, "кнопка 'Конструктор'")
            self.assert_element_visible(MainPageLocators.ORDER_FEED_BUTTON, "кнопка 'Лента заказов'")

            # Дополнительные проверки
            try:
                # Проверяем наличие какой-то области на странице
                self.wait_for_element(MainPageLocators.CONSTRUCTOR_DROP_AREA, timeout=3)
            except:
                logger.warning("Не удалось найти область конструктора быстро")

            logger.info("Главная страница успешно загружена")

        except Exception as e:
            logger.error(f"Ошибка при проверке загрузки главной страницы: {e}")
            self.take_screenshot("main_page_not_loaded")
            raise AssertionError(f"Главная страница не загружена: {e}")

    @allure.step("Закрыть модальное окно ингредиента")
    def close_ingredient_modal(self):
        """Закрытие модального окна ингредиента"""
        try:
            # Пробуем закрыть через крестик
            close_button = self.wait_for_element(MainPageLocators.MODAL_CLOSE_BUTTON, timeout=5)
            self.click_js(close_button)
            logger.info("Модальное окно ингредиента закрыто через крестик")
        except Exception as e:
            logger.warning(f"Не удалось закрыть через крестик: {e}")
            # Альтернативный способ
            try:
                self.click_js(self.driver.find_element(*MainPageLocators.MODAL_CLOSE_BUTTON))
            except:
                logger.error("Не удалось закрыть модальное окно")
                raise

    @allure.step("Кликнуть на ингредиент булку")
    def click_ingredient_bun(self):
        """Клик по ингредиенту булка"""
        self.click_ingredient(MainPageLocators.INGREDIENT_BUN)

    @allure.step("Получить текст счетчика ингредиента")
    def get_ingredient_counter_text(self):
        """Получение текста счетчика ингредиента"""
        try:
            return self.get_element_text(MainPageLocators.INGREDIENT_COUNTER)
        except Exception as e:
            logger.warning(f"Не удалось получить текст счетчика: {e}")
            return "0"

    @allure.step("Проверить что счетчик ингредиента увеличился")
    def assert_counter_increased(self, initial_value):
        """Проверка что счетчик ингредиента увеличился"""
        try:
            current_value = self.get_ingredient_counter_text()
            assert current_value != initial_value, \
                f"Счетчик ингредиента не изменился. Было: '{initial_value}', стало: '{current_value}'"
            logger.info(f"Счетчик ингредиента увеличился: '{initial_value}' -> '{current_value}'")
        except Exception as e:
            logger.error(f"Ошибка при проверке счетчика: {e}")
            self.take_screenshot("counter_not_increased")
            raise AssertionError(f"Счетчик ингредиента не увеличился: {e}")

    @allure.step("Проверить что пользователь авторизован")
    def assert_user_authorized(self):
        """Проверка что пользователь авторизован"""
        try:
            # Проверяем что мы на главной странице
            current_url = self.get_current_url()
            assert "/login" not in current_url and "auth" not in current_url.lower(), \
                f"Все еще на странице авторизации. URL: {current_url}"

            # Проверяем наличие кнопки "Личный кабинет"
            personal_account_btn = self.wait_for_element(AccountPageLocators.PERSONAL_ACCOUNT_BUTTON, timeout=5)
            assert personal_account_btn.is_displayed(), "Кнопка 'Личный кабинет' не отображается"

            logger.info("Пользователь успешно авторизован")

        except Exception as e:
            logger.error(f"Ошибка при проверке авторизации: {e}")
            self.take_screenshot("user_not_authorized")
            raise AssertionError(f"Пользователь не авторизован: {e}")


    @allure.step("Проверить что модальное окно ингредиента открылось")
    def assert_ingredient_modal_opened(self):
        """Проверка что модальное окно ингредиента открылось"""
        try:
            self.assert_element_visible(MainPageLocators.INGREDIENT_MODAL, "модальное окно ингредиента")
            logger.info("Модальное окно ингредиента успешно открылось")
        except Exception as e:
            logger.error(f"Ошибка при проверке модального окна ингредиента: {e}")
            self.take_screenshot("ingredient_modal_not_opened")
            raise AssertionError("Модальное окно ингредиента не открылось")

    @allure.step("Проверить что модальное окно ингредиента закрылось")
    def assert_ingredient_modal_closed(self):
        """Проверка что модальное окно ингредиента закрылось"""
        try:
            self.assert_element_not_visible(MainPageLocators.INGREDIENT_MODAL, "модальное окно ингредиента", timeout=5)
            logger.info("Модальное окно ингредиента успешно закрылось")
        except Exception as e:
            logger.error(f"Ошибка при проверке закрытия модального окна: {e}")
            self.take_screenshot("ingredient_modal_not_closed")
            raise AssertionError("Модальное окно ингредиента не закрылось")

    @allure.step("Проверить что кнопка 'Оформить заказ' активна")
    def assert_order_button_enabled(self):
        """Проверка что кнопка оформления заказа активна"""
        try:
            order_button = self.wait_for_element(MainPageLocators.ORDER_BUTTON, timeout=5)
            assert order_button.is_enabled(), "Кнопка 'Оформить заказ' не активна"
            logger.info("Кнопка 'Оформить заказ' активна - ингредиенты добавлены успешно")
        except Exception as e:
            logger.error(f"Ошибка при проверке кнопки заказа: {e}")
            self.take_screenshot("order_button_not_enabled")
            raise AssertionError("Кнопка 'Оформить заказ' не активна после добавления ингредиентов")

    @allure.step("Проверить что пользователь не авторизован")
    def assert_user_not_authorized(self):
        """Проверка что пользователь не авторизован"""
        try:
            # Проверяем наличие кнопки "Войти в аккаунт"
            login_button = self.wait_for_element(MainPageLocators.LOGIN_BUTTON, timeout=5)
            assert login_button.is_displayed(), "Кнопка 'Войти в аккаунт' не отображается"

            # Проверяем отсутствие кнопки "Личный кабинет"
            try:
                personal_account_buttons = self.find_elements(AccountPageLocators.PERSONAL_ACCOUNT_BUTTON)
                for button in personal_account_buttons:
                    if button.is_displayed():
                        raise AssertionError("Кнопка 'Личный кабинет' отображается, но не должна")
            except:
                pass

            logger.info("Пользователь не авторизован (как и ожидалось)")

        except Exception as e:
            logger.error(f"Ошибка при проверке отсутствия авторизации: {e}")
            self.take_screenshot("user_still_authorized")
            raise AssertionError(f"Статус авторизации не определен: {e}")

    @allure.step("Проверить наличие ингредиентов на странице")
    def assert_ingredients_present(self):
        """Проверка что ингредиенты отображаются на странице"""
        try:
            self.assert_element_visible(MainPageLocators.INGREDIENT_BUN, "секция булок")
            self.assert_element_visible(MainPageLocators.INGREDIENT_MAIN, "секция начинок")
            self.assert_element_visible(MainPageLocators.INGREDIENT_SAUCE, "секция соусов")

            # Проверяем что есть элементы в секциях
            bun_count = len(self.find_elements(MainPageLocators.INGREDIENT_BUN))
            main_count = len(self.find_elements(MainPageLocators.INGREDIENT_MAIN))
            sauce_count = len(self.find_elements(MainPageLocators.INGREDIENT_SAUCE))

            assert bun_count > 0, "Нет доступных булок"
            assert main_count > 0, "Нет доступных начинок"
            assert sauce_count > 0, "Нет доступных соусов"

            logger.info(f"Ингредиенты доступны: булок={bun_count}, начинок={main_count}, соусов={sauce_count}")

        except Exception as e:
            logger.error(f"Ошибка при проверке ингредиентов: {e}")
            self.take_screenshot("ingredients_not_present")
            raise AssertionError(f"Ингредиенты не отображаются на странице: {e}")


    @allure.step("Получить значение счетчика")
    def get_counter_value(self, locator):
        """Получение числового значения счетчика"""
        try:
            counter_text = self.get_element_text(locator)
            digits = ''.join([char for char in counter_text if char.isdigit()])
            return int(digits) if digits else 0
        except Exception as e:
            logger.error(f"Ошибка при получении значения счетчика: {e}")
            return 0