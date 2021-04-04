import requests
from functools import lru_cache
from requests.exceptions import HTTPError
from itertools import groupby
from geopy import distance
from django.conf import settings
from foodcartapp.models import AddressPoint


def fetch_coordinates(place):
    apikey = settings.GEOCODE_API_KEY
    base_url = "https://geocode-maps.yandex.ru/1.x"
    params = {"geocode": place, "apikey": apikey, "format": "json"}
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        found_places = response.json()['response']['GeoObjectCollection'][
            'featureMember']
        most_relevant = found_places[0]
        lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
        return lat, lon
    except HTTPError:
        return None


@lru_cache
def get_coordinates(place):
    try:
        _address = AddressPoint.objects.filter(address=place).get()
    except AddressPoint.DoesNotExist:
        lat, lon = fetch_coordinates(place)
        _address = AddressPoint.objects.create(address=place,
                                               latitude=lat, longitude=lon)
    return float(_address.latitude), float(_address.longitude)


def get_distance(restaurant, order_address):
    restaurant_name, restaurant_address = restaurant.split('|%|')

    if not isinstance(order_address, str) or not \
        isinstance(restaurant_address, str):
        return restaurant_name

    start = get_coordinates(restaurant_address)
    finish = get_coordinates(order_address)
    _distance = round(distance.distance(start, finish).km, 2)
    if _distance <= 0:
        return restaurant_name
    return f'{restaurant_name} - {_distance} км'


def get_available_restaurants(restaurants_menus, order):
    global restaurants_for_order
    rest_products = []
    all_restaurants = []

    [rest_products.append((restaurants_menu.rest_name,
                           restaurants_menu.rest_address,
                           restaurants_menu.product_id))
     for restaurants_menu in restaurants_menus]

    ordered_products_ids = [x.product.id for x in order.order_items.all()]
    for ordered_products_id in ordered_products_ids:
        for rest_product in rest_products:
            _name, _address, _id = rest_product
            if ordered_products_id == _id:
                all_restaurants.append(f'{_name}|%|{_address}')
        all_restaurants.append(None)  # delimiter
    restaurants_for_order = [set(group) for delimiter, group in groupby(
        all_restaurants, lambda x: x is None) if not delimiter]

    return list(set.intersection(*restaurants_for_order))
