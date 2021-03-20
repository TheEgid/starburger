from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Order, OrderItem
import json


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


def add_one():
    largest = Order.objects.all().order_by('order_number').last()
    if not largest:
        return 1
    return largest.order_number + 1


def verify_order(in_data):
    empty_request = Response({"error": "empty_request"},
                             status=status.HTTP_204_NO_CONTENT)
    bad_key = Response({"error": "product key not presented or not list"},
                       status=status.HTTP_206_PARTIAL_CONTENT)
    out_data = ""
    if len(in_data) < 1:
        out_data = empty_request
    try:
        assert len(in_data["products"][0]) > 1
    except KeyError:
        out_data = bad_key
    except AssertionError:
        out_data = bad_key
    except IndexError:
        out_data = bad_key
    except TypeError:
        out_data = bad_key
    return out_data


@api_view(['POST'])
def register_order(request):
    order_json = request.data
    response = verify_order(order_json)
    if response:
        return response

    number = add_one()
    order = Order.objects.create(order_number=number,
                                 address=order_json['address'],
                                 firstname=order_json['firstname'],
                                 lastname=order_json['lastname'],
                                 phone_number=order_json['phonenumber'])

    for ordered in order_json['products']:
        product = Product.objects.get(id=ordered['product'])
        OrderItem.objects.create(product=product,
                                 quantity=ordered['quantity'],
                                 order=order)

    return Response({}, status=status.HTTP_201_CREATED)
