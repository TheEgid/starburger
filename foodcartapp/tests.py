import json
from rest_framework import status
from django.test.client import Client
from django.test import TestCase


def setUp(self):
    """initialize the Django test client"""
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
        {"products": [], "firstname": "1", "lastname": "2", "phonenumber": "3",
         "address": "4"},
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

    test_ordering_params3 = [{"products": [{"product": 1, "quantity": "1"}], "firstname": "Димон", "lastname": "Димонов", "phonenumber": "+7 967 4782385", "address": "Дом на Курской площади"}]

    # def test_product_api1(self):
    #     for test_product_data in self.test_ordering_params1:
    #         response = self.client.post('/api/order/',
    #                                     json.dumps(test_product_data),
    #                                     content_type="application/json")
    #         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    #         assert b'product key not presented' in response.content
    #
    # def test_product_api2(self):
    #     for test_product_data in self.test_ordering_params2:
    #         response = self.client.post('/api/order/',
    #                                     json.dumps(test_product_data),
    #                                     content_type="application/json")
    #         assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    #         assert b'product key not presented' in response.content

    def test_product_api3(self):
        for test_product_data in self.test_ordering_params3:
            response = self.client.post('/api/order/',
                                        test_product_data,
                                        content_type="application/json")
            assert response.status_code == status.HTTP_200_OK
            #assert b'product key not presented' in response.content
