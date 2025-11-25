from selenium.webdriver.common.by import By


class MainPageLocators:
    # Основные элементы
    MODAL_OVERLAY_LOCATOR = (By.CLASS_NAME, "Modal_modal_overlay__x2ZCr")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти в аккаунт')]")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[contains(text(),'Конструктор')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[contains(text(),'Лента Заказов')]")
    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//p[contains(text(), 'Личный Кабинет')]")
    MAKE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    # Ингредиенты
    INGREDIENT_BUN = (By.XPATH, "//p[text()='Флюоресцентная булка R2-D3']")
    INGREDIENT_SAUCE = (By.XPATH, "//p[text()='Соус Spicy-X']")
    INGREDIENT_MAIN = (By.XPATH, "//p[text()='Мясо бессмертных моллюсков Protostomia']")

    # Модальное окно ингредиента
    INGREDIENT_MODAL = (By.XPATH, "//section[contains(@class,'Modal_modal')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//section[contains(@class, 'Modal_modal')]//button")
    MODAL_INGREDIENT_NAME = (By.XPATH, "//h2[contains(@class,'text_type_main-medium')]")

    # Локатор откуда тянуть
    BURGER_INGREDIENT_LINK = (By.CSS_SELECTOR, "[class*='ingredient__'][href*='/ingredient/']")

    # Конструктор заказа, локатор куда тянуть общий
    CONSTRUCTOR_DROP_AREA = (By.CSS_SELECTOR, "ul[class*='basket__']")

    # Локатор куда тянуть для верхнего элемента
    CONSTRUCTOR_ELEMENT_TOP = (By.XPATH, "//div[contains(@class, 'constructor-element_pos_top')]")

    # Локатор куда тянуть для нижнего элемента
    CONSTRUCTOR_ELEMENT_BOTTOM = (By.XPATH,"//div[contains(@class, 'constructor-element_pos_bottom')]")

    # Счетчик ингредиента
    INGREDIENT_COUNTER = (By.XPATH, "//p[text()='Флюоресцентная булка R2-D3']/ancestor::div[contains(@class, 'ingredient')]//div[contains(@class, 'counter')]")

    # Кнопка оформления заказа
    ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Оформить заказ')]")

    # Лента заказов
    ORDER_FEED_SECTION = (By.XPATH, "//h1[contains(text(), 'Лента заказов')] | //section[contains(@class, 'OrderFeed')]")

    # Локатор для заказа в ленте
    ORDER_IN_FEED = (By.XPATH, "//p[contains(@class, 'text_type_digits-default')]")

    # Модальное окно идентификатор заказа (при нажатии на кнопку "Оформить заказ")
    INGREDIENT_MODAL_DETAILS_TITLE = (By.XPATH, "//div[contains(@class, 'Modal_modal__contentBox__sCy8X')]")

    # Закрыть модальное окно идентификатор заказа
    CLOSE_BUTTON = (By.XPATH, "button.Modal_modal__close__TnseK")
    MODAL_CLOSE_ORDER = (By.XPATH, "//button//*[local-name()='svg' and @width='24' and @height='24' and @fill='#F2F2F3']")