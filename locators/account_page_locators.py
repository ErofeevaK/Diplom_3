from selenium.webdriver.common.by import By


class AccountPageLocators:
    PROFILE = (By.XPATH, '//a[@href = "/account/profile"]')
    ORDER_HISTORY = (By.XPATH, '//a[@href = "/account/order-history"]')
    BUTTON_LOGOUT = (By.XPATH, '//button[@type = "button"]')
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[contains(text(), 'Личный Кабинет')]")
    # Текст в личном кабинете: "В этом разделе вы можете изменить свои персональные данные"
    ACCOUNT_TEXT = (By.XPATH, '//p[contains(text(), "В этом разделе вы можете")]')
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(@class, 'Account_button__14Yp3') and contains(text(), 'Выход')]")

class HistoryPageLocators:
    # Основной контейнер
    ORDER_CARD = (By.XPATH, '//*[contains(@class, "OrderHistory_listItem")]')
    ORDER_HISTORY_TEXT_BOX = (By.CSS_SELECTOR, ".OrderHistory_textBox__3lgbs")
    # Номер заказа
    ORDER_NUMBER = (By.XPATH, '(//div[contains(@class, "OrderHistory_textBox")]'
                               '/p[contains(@class, "text_type_digits-default")])[2]')
    ORDER_NUMBER_FROM_HISTORY = (
        By.XPATH, "//a[@class='OrderHistory_link__1iNby']//p[contains(text(), 'Сегодня')]/preceding-sibling::p")
    # Локатор для получения всех блоков номеров заказов
    ALL_ORDERS_NUMBERS = (
        By.XPATH,
        '//div[contains(@class, "OrderHistory_listItem")]/*[contains(@class, "OrderHistory_textBox")]'
        '/p[contains(@class, "text_type_digits-default")]'
    )
    ORDER_PROFILE_LIST = (By.CSS_SELECTOR, ".OrderHistory_profileList__374GU.OrderHistory_list__KcLDB")
    CONTAINER_CSS_FIRST_CLASS = (By.CSS_SELECTOR, ".OrderHistory_profileList__374GU")