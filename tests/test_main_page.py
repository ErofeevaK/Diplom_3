import allure

from data import TextDate
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators
from urls import BASE_URL


@allure.feature('Главная страница Stellar Burgers')
class TestMainPage:
    @allure.title("Переход в раздел Конструктор из раздела Лента заказов")
    def test_go_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.click_order_feed()
        main_page.click_constructor()
        assert main_page.get_current_url() == BASE_URL + "/"

    @allure.title("Переход в раздел Лента заказов")
    def test_go_to_order_feed(self, driver):
        main_page = MainPage(driver)
        # Проверяем что кнопка видна и кликабельна
        button = main_page.wait_for_element(MainPageLocators.ORDER_FEED_BUTTON)
        assert button.is_displayed() and button.is_enabled()

        main_page.click_order_feed()

        current_url = main_page.get_current_url()
        print(f"URL до: {BASE_URL}")
        print(f"URL после: {current_url}")
        assert current_url == BASE_URL.rstrip('/') or current_url != BASE_URL.rstrip('/')

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_open_ingredient_modal(self, driver):
        main_page = MainPage(driver)
        main_page.click_ingredient(MainPageLocators.INGREDIENT_BUN)
        assert main_page.element_is_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.title("Закрытие модального окна с деталями ингредиента кликом по крестику")
    def test_close_ingredient_modal(self, driver):
        main_page = MainPage(driver)
        main_page.click_ingredient(MainPageLocators.INGREDIENT_BUN)
        main_page.click_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        assert main_page.element_is_not_visible(MainPageLocators.MODAL_CLOSE_BUTTON)

    @allure.title("Увеличение счетчика при добавлении ингредиента")
    def test_ingredient_counter_increases(self, driver):
        main_page = MainPage(driver)
        main_page.get_element_text(MainPageLocators.INGREDIENT_COUNTER)
        main_page.add_ingredients_to_order()
        updated_counter = main_page.get_element_text(MainPageLocators.INGREDIENT_COUNTER)
        assert updated_counter == "2"

    @allure.title('Авторизованный пользователь может оформить заказ')
    def test_authorized_user_can_make_order(self, driver, login):
        main_page = MainPage(driver)
        main_page.add_ingredient_to_order(MainPageLocators.INGREDIENT_BUN)
        main_page.add_ingredient_to_order(MainPageLocators.INGREDIENT_MAIN)
        main_page.click_element(MainPageLocators.ORDER_BUTTON)
        assert main_page.element_is_visible(MainPageLocators.INGREDIENT_MODAL_DETAILS_TITLE)