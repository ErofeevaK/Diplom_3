class Url:
    BASE_URL = 'https://stellarburgers.education-services.ru'
    USER_REGISTRATION_URL = '/api/auth/register'    # регистрация пользователя
    USER_LOGIN_URL = '/api/auth/login'              # авторизация пользователя
    USER_LOGOUT_URL = '/api/auth/logout'            # выход из системы
    TOKEN_UPDATE_URL = '/api/auth/token'            # обновление токена
    USER_DATA_URL = '/api/auth/user'                # получение/обновление/удаление данных о пользователе
    USER_GET_ORDERS_URL = '/api/orders'             # получение заказов конкретного пользователя, только после авторизации
    ORDER_CREATION_POST_URL = '/api/orders'         # создание заказов
    INGREDIENTS_GET_URL = '/api/ingredients'        # получение данных об ингредиентах

BASE_URL = "https://stellarburgers.education-services.ru"
ORDER_FEED_URL = f"{BASE_URL}/feed"
LOGIN_URL = f"{BASE_URL}/login"
PROFILE_URL= f"{BASE_URL}/account/profile"
USER_REGISTER = f"{BASE_URL}/register"
ORDER_HISTORY_URL = f"{BASE_URL}/account/order-history"