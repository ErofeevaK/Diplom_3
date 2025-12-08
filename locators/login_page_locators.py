from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON_AUTH = (By.XPATH, "//button[contains(text(), 'Войти')]")
    PERSONAL_CABINET_LINK = (By.XPATH, "//p[text()='Личный Кабинет']")