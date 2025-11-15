import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.main_page import MainPage
from pages.login_page import LoginPage
from helpers import UserAPI
from urls import BASE_URL


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
        print(f"❌ Регистрация не удалась: {response.status_code} - {response_data}")
        pytest.fail(f"Регистрация через API не удалась: {response_data.get('message', 'Unknown error')}")

    access_token = response_data.get('accessToken')
    if not access_token:
        print(f"❌ Access Token не получен: {response_data}")
        pytest.fail("Access Token не получен при регистрации")

    user_info = {
        'email': user_data['email'],
        'password': user_data['password'],
        'name': user_data['name'],
        'access_token': access_token,
        'response': response,
        'response_data': response_data
    }

    print(f"✅ Пользователь зарегистрирован: {user_data['email']}")
    yield user_info

    # Удаляем пользователя после теста
    if user_info['access_token']:
        UserAPI.delete_user(user_info['access_token'])


# Основная фикстура для авторизации в UI
@pytest.fixture
def login(driver, registered_user):
    """Авторизация с гарантированным переходом на главную"""
    main_page = MainPage(driver)

    # Переходим на страницу логина
    main_page.go_to_login_page_buttom_lk()

    # Авторизуемся
    login_page = LoginPage(driver)
    login_page.user_authorization(registered_user['email'], registered_user['password'])

    # Ждем возврата на главную страницу
    main_page.wait_for_url(BASE_URL, timeout=15)

    # ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА: убедимся что мы действительно авторизованы
    import time
    time.sleep(2)
    current_url = driver.current_url
    if "login" in current_url:
        pytest.fail(f"Авторизация не прошла - остались на странице логина. URL: {current_url}")

    print(f"✅ UI-авторизация прошла успешно для: {registered_user['email']}")
    return main_page