import requests
import allure
import random
import string

from faker import Faker
from urls import Url

# Инициализация Faker
fake = Faker()

class UserAPI:
    @staticmethod
    @allure.step("Генерируем случайные данные пользователя")
    def generate_random_user():
        random_id = ''.join(random.choices(string.digits, k=8))  # 8 случайных цифр
        return {
            'email': f'test_user_{random_id}@test.com',
            'password': 'TestPassword123',  # Фиксированный надежный пароль
            'name': f'TestUser{random_id}'
        }


    @staticmethod
    @allure.step("Регистрируем пользователя с предоставленными данными")
    def register(user_data):
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(Url.BASE_URL + Url.USER_REGISTRATION_URL, json=user_data)
        return response


    @staticmethod
    @allure.step("Удаляем пользователя")
    def delete_user(access_token):

        headers  = {'Authorization': f'Bearer {access_token}'}

        # Выполняем DELETE-запрос с передачей токена в заголовке
        requests.delete(Url.BASE_URL + Url.USER_DATA_URL, headers=headers)


class OrderAPI:
    @staticmethod
    @allure.step("Создаем заказ с указанными ингредиентами")
    def create_order(registered_user, ingredients):
        user_data = registered_user
        headers = {
            'Authorization': user_data['access_token'],
            'Content-Type': 'application/json'
        }

        return requests.post(
            Url.BASE_URL + Url.ORDER_CREATION_POST_URL,
            json={"ingredients": ingredients},
            headers=headers
        )