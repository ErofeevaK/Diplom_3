from selenium.webdriver.common.by import By

class OrderFeedPageLocators:
    MODAL_OVERLAY_LOCATOR = (By.CSS_SELECTOR, "div.Modal_modal_overlay__x2ZCr")
    # Лента заказов
    ORDER_FEED_SECTION = (By.XPATH, "//h1[contains(text(),'Лента заказов')]")
    FIRST_ORDER_ITEM = (By.XPATH, "(//li[contains(@class, 'OrderHistory_listItem__2x95r')])[1]")
    MODAL_WINDOW = (By.CSS_SELECTOR, ".Modal_modal__contentBox__sCy8X")
    MODAL_ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title__2L34m')]")
    MODAL_CLOSE_ORDER = (By.CSS_SELECTOR, "button.Modal_modal__closeBtn__3JQgr")
    # В работе
    ORDERS_AT_WORK = (By.CSS_SELECTOR, "ul.OrderFeed_orderListReady__1YFem")
    STATUS_READY_TEXT = (By.XPATH, "//li[@class='text text_type_main-small' and contains(text(), 'Все текущие заказы готовы!')]")
    # Основной контейнер списка заказов Готовы:
    ORDER_FEED_ORDER_LIST = (By.CSS_SELECTOR, ".OrderFeed_orderList__cBvyi")
    # Основной контейнер списка заказов
    ORDER_FEED_LIST = (By.CSS_SELECTOR, ".OrderFeed_list__OLh59")
    # Выполнено за все время
    All_ORDERS_LOCATOR = (By.XPATH, '//p[contains(text(), "Выполнено за все время:")]/following-sibling::p')
    # Выполнено за сегодня
    TODAY_ORDERS_LOCATOR = (By.XPATH, '//p[contains(text(), "Выполнено за сегодня:")]/following-sibling::p')