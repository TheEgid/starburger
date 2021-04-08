from django.http import JsonResponse
from django.db import transaction
from django.templatetags.static import static
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Order, OrderItem
from .serializers import OrderSerializer, ProductSerializer
from rest_framework.serializers import ValidationError


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()
    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    try:
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_order = serializer.validated_data
        if not new_order['products']:
            raise ValidationError
    except ValidationError:
        return Response({"error": "product key not presented or not list"},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    with transaction.atomic():
        order = Order.objects.create(address=new_order['address'],
                                     firstname=new_order['firstname'],
                                     lastname=new_order['lastname'],
                                     phonenumber=new_order['phonenumber'])

        for new_order_item in new_order['products']:
            value = new_order_item['product'].price * new_order_item['quantity']
            OrderItem.objects.create(product=new_order_item['product'],
                                     quantity=new_order_item['quantity'],
                                     value=value,
                                     order=order)
        serializer_order = OrderSerializer(order)

    return Response(serializer_order.data,
                    status=status.HTTP_201_CREATED)
