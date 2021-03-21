from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer, ListSerializer
from .models import Product, Order, OrderItem


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id']


class OrderItemSerializer(ModelSerializer):

    class Meta:
        product = ProductSerializer(many=True)
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, write_only=True)
    phonenumber = PhoneNumberField()

    class Meta:
        model = Order
        write_only = ['products']
        fields = ['id', 'firstname', 'lastname',
                  'products', 'address', 'phonenumber']
