from django.http import JsonResponse
from django.templatetags.static import static
import json
from .models import Product, Order, OrderItem


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


def register_order(request):
    order_json = json.loads(request.body.decode())

    if len(order_json['products']) < 1:
        return JsonResponse({})

    number = add_one()

    order = Order.objects.create(order_number=number,
                  address=order_json['address'],
                  firstname=order_json['firstname'],
                  lastname=order_json['lastname'],
                  phone_number=order_json['phonenumber'])

    for ordered in order_json['products']:
        product = Product.objects.get(id=ordered['product'])
        OrderItem.objects.create(
            product=product,
            quantity=ordered['quantity'],
            order=order)

    return JsonResponse({})
