import pytest
import allure
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers import UserAPI
from urls import BASE_URL

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Настройка логирования для всех тестов"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('test.log'),
            logging.StreamHandler()
        ]
    )


# Фикстура для драйвера
@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.add_argument('--headless')
        options.set_preference("browser.tabs.remote.autostart", False)
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    driver.get(BASE_URL)

    yield driver
    driver.quit()


# Фикстура для зарегистрированного пользователя через API
@pytest.fixture
def registered_user():
    """Регистрация пользователя через API с проверкой успешности"""
    user_data = UserAPI.generate_random_user()
    response = UserAPI.register(user_data)
    response_data = response.json()

    # ПРОВЕРКА что регистрация прошла успешно
    if response.status_code != 200 or not response_data.get('success'):
        logger.error(f"Регистрация не удалась: {response.status_code} - {response_data}")
        pytest.fail(f"Регистрация через API не удалась: {response_data.get('message', 'Unknown error')}")

    access_token = response_data.get('accessToken')
    if not access_token:
        logger.error(f"Access Token не получен: {response_data}")
        pytest.fail("Access Token не получен при регистрации")

    user_info = {
        'email': user_data['email'],
        'password': user_data['password'],
        'name': user_data['name'],
        'access_token': access_token,
        'response': response,
        'response_data': response_data
    }

    logger.info(f"Пользователь зарегистрирован: {user_data['email']}")
    yield user_info

    # Удаляем пользователя после теста
    if user_info['access_token']:
        UserAPI.delete_user(user_info['access_token'])


# Основная фикстура для авторизации в UI
@pytest.fixture
def login_setup(driver, registered_user):
    """Авторизация с гарантированным переходом на главную"""
    main_page = MainPage(driver)

    # Логируем начало авторизации
    logger.info(f"Начинаем авторизацию для пользователя: {registered_user['email']}")

    try:
        # Переходим на страницу логина через существующий метод
        logger.info("Переходим на страницу логина...")
        main_page.go_to_login_page_buttom_lk()

        # Проверяем что мы действительно на странице логина
        current_url = main_page.get_current_url()
        logger.info(f"Текущий URL после перехода на логин: {current_url}")

        if "/login" not in current_url:
            logger.warning(f"Не на странице логина. URL: {current_url}")
            # Пробуем альтернативный способ
            main_page.go_to_login_page()

        # Авторизуемся через Page-класс
        logger.info("Вводим данные для авторизации...")
        login_page = LoginPage(driver)
        login_page.user_authorization(registered_user['email'], registered_user['password'])

        # Даем время для обработки авторизации
        logger.info("Ждем завершения авторизации...")
        time.sleep(3)

        # Проверяем текущий URL
        current_url = main_page.get_current_url()
        logger.info(f"Текущий URL после авторизации: {current_url}")

        # Если все еще на странице логина, проверяем есть ли ошибка
        if "/login" in current_url or "auth" in current_url.lower():
            logger.error(f"Остались на странице логина после авторизации: {current_url}")

            # Проверяем есть ли сообщение об ошибке
            try:
                from locators.login_page_locators import LoginPageLocators
                error_element = main_page.find_elements(LoginPageLocators.ERROR_MESSAGE)
                if error_element:
                    error_text = error_element[0].text
                    logger.error(f"Сообщение об ошибке: {error_text}")
            except:
                pass

            main_page.take_screenshot("auth_failed")

            # Пробуем подождать еще
            logger.info("Пробуем подождать еще 5 секунд...")
            time.sleep(5)
            current_url = main_page.get_current_url()

            if "/login" in current_url or "auth" in current_url.lower():
                raise AssertionError(f"Авторизация не удалась. Остались на странице логина: {current_url}")

        # Проверяем что мы на главной странице или произошел редирект
        logger.info(f"Проверяем успешность авторизации. URL: {current_url}")

        # Используем метод проверки авторизации из MainPage
        try:
            main_page.assert_user_authorized()
        except AttributeError:
            # Если метода еще нет, делаем простую проверку
            if "/login" in current_url or "auth" in current_url.lower():
                raise AssertionError(f"Авторизация не прошла, остались на странице логина: {current_url}")

        logger.info(f"UI-авторизация прошла успешно для: {registered_user['email']}")
        return main_page

    except Exception as e:
        logger.error(f"Ошибка в фикстуре login_setup: {e}")
        main_page.take_screenshot("login_setup_error")
        raise