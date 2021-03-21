from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.serializers import ModelSerializer
from .models import Product, Order, OrderItem


class ProductItemSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id']


class OrderItemSerializer(ModelSerializer):
    class Meta:
        product = ProductItemSerializer(many=True)
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True)
    phonenumber = PhoneNumberField()
    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'products', 'address', 'phonenumber']
