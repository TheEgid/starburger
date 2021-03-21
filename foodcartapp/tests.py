from rest_framework import status
from django.test.client import Client
from django.test import TestCase
from .models import Product, ProductCategory, Order, OrderItem
import json


def setUp(self):
    self.c = Client()


class ApiTestCase(TestCase):
    test_ordering_params1 = [
        #  // Продукты — это не список, а строка:
        {"products": "HelloWorld", "firstname": "1", "lastname": "2",
         "phonenumber": "3", "address": "4"},
        # // Продукты — это null:
        {"products": None, "firstname": "1", "lastname": "2",
         "phonenumber": "3",
         "address": "4"},
        # // Продукты — пустой список:
        {"products": [], "firstname": "some", "lastname": "some",
         "phonenumber": "+7 967 466 2380", "address": "Дом на Курской площади"},
        # // Продуктов нет:
        {"firstname": "1", "lastname": "2", "phonenumber": "3", "address": "4"}
    ]

    test_ordering_params2 = [
        # firstname == null:
        {"products": [{"product": 1, "quantity": 1}], "firstname": None,
         "lastname": "2", "phonenumber": "3", "address": "4"},
        # // Ключей заказа вообщенет:
        {"products": [{"product": 1, "quantity": 1}]},
        # // Ключи есть, но все со значением null:
        {"products": [{"product": 1, "quantity": 1}], "firstname": None,
         "lastname": None, "phonenumber": None, "address": None},
        # // Не указан номер телефона
        {"products": [{"product": 1, "quantity": 1}], "firstname": "Тимур",
         "lastname": "Иванов", "phonenumber": "",
         "address": "Москва, Новый Арбат 10"},
        # // Заказ с неуществующим id продукта:
        {"products": [{"product": "jngrtgntg", "quantity": 1}],
         "firstname": "1",
         "lastname": "2", "phonenumber": "3", "address": "4"},
        # // В поле firstname положили список:
        {"products": [{"product": 1, "quantity": 1}], "firstname": [],
         "lastname": "2", "phonenumber": "3", "address": "4"}
    ]

    def test_negative_create_product1(self):
        for test_product_data in self.test_ordering_params1:
            response = self.client.post('/api/order/',
                                        json.dumps(test_product_data),
                                        content_type="application/json")
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert b'product key not presented' in response.content

    def test_negative_create_product2(self):
        for test_product_data in self.test_ordering_params2:
            response = self.client.post('/api/order/',
                                        json.dumps(test_product_data),
                                        content_type="application/json")
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
            assert b'product key not presented' in response.content

    def test_positive_create_product(self):
        test_product_data = {"products": [{"product": 1, "quantity": 1}],
                             "firstname": "Василий", "lastname": "Васильевич",
                             "phonenumber": "+7 912 3456789",
                             "address": "Лондон"}
        category = ProductCategory.objects.create(name="new_category")
        Product.objects.create(name="new_product", category=category, price=100)
        response = self.client.post('/api/order/',
                                    json.dumps(test_product_data),
                                    content_type="application/json")
        assert response.status_code == status.HTTP_201_CREATED
        assert 'address' in response.json().keys()
        assert '+79123456789' in response.json().values()
        assert test_product_data['firstname'] in response.json().values()
