import allure
import logging
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage

logger = logging.getLogger(__name__)


@allure.feature('Главная страница Stellar Burgers')
class TestMainPage:
    @allure.title("Переход в раздел Конструктор из раздела Лента заказов")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)

        # Переходим в ленту заказов
        main_page.click_order_feed()

        # Возвращаемся в конструктор
        main_page.click_constructor()

        # Проверяем что мы на главной странице
        main_page.assert_main_page_loaded()

        logger.info("Успешный переход из ленты заказов в конструктор")

    @allure.title("Переход в раздел Лента заказов")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)

        # Переходим в ленту заказов
        main_page.go_to_order_feed()

        # Проверяем что мы перешли
        main_page.assert_url_contains("/feed")

        logger.info("Успешный переход в ленту заказов")

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_open_ingredient_modal(self, driver):
        main_page = MainPage(driver)

        # Кликаем на ингредиент булку
        main_page.click_ingredient_bun()

        # Проверяем что модальное окно открылось
        main_page.assert_ingredient_modal_opened()

        logger.info("Модальное окно с деталями ингредиента успешно открыто")

    @allure.title("Закрытие модального окна с деталями ингредиента")
    def test_close_ingredient_modal(self, driver):
        main_page = MainPage(driver)

        # Открываем модальное окно
        main_page.click_ingredient_bun()
        main_page.assert_ingredient_modal_opened()

        # Закрываем модальное окно
        main_page.close_ingredient_modal()

        # Проверяем что модальное окно закрылось
        main_page.assert_ingredient_modal_closed()

        logger.info("Модальное окно с деталями ингредиента успешно закрыто")

    @allure.title("Увеличение счетчика при добавлении ингредиента")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)

        # Получаем начальное состояние счетчика
        initial_counter = main_page.get_ingredient_counter_text()

        # Добавляем ингредиенты в заказ
        main_page.add_ingredients_to_order()

        # Проверяем что счетчик изменился
        main_page.assert_counter_increased(initial_counter)

        logger.info("Счетчик ингредиента успешно увеличился")

    @allure.title('Авторизованный пользователь может оформить заказ')
    def test_authorized_user_can_make_order(self, driver, login_setup):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # Добавляем ингредиенты в заказ
        main_page.add_ingredients_to_order()

        # Проверяем что кнопка заказа активна
        main_page.assert_order_button_enabled()

        # Нажимаем кнопку оформления заказа
        main_page.make_order()

        # Проверяем что открылось модальное окно с деталями заказа
        order_feed_page.assert_order_modal_opened()

        # Закрываем модальное окно
        order_feed_page.close_modal_window()

        # Проверяем что модальное окно закрылось
        order_feed_page.assert_modal_closed()

        logger.info("Авторизованный пользователь успешно оформил заказ")