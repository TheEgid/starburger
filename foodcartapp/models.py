from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import DecimalField, F, Sum, ExpressionWrapper, CharField, \
    Value
from django.db.models.functions import Concat


class Restaurant(models.Model):
    name = models.CharField('название', max_length=50)
    address = models.CharField('адрес', max_length=100, blank=True)
    contact_phone = PhoneNumberField('контактный телефон', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'


class ProductQuerySet(models.QuerySet):
    def available(self):
        return self.distinct().filter(menu_items__availability=True)


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    category = models.ForeignKey(ProductCategory, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name='категория',
                                 related_name='products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(0)])
    image = models.ImageField('картинка')
    special_status = models.BooleanField('спец.предложение', default=False,
                                         db_index=True)
    description = models.TextField('описание', max_length=1000, blank=True)

    objects = ProductQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,
                                   related_name='menu_items',
                                   verbose_name="ресторан")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='menu_items',
                                verbose_name='продукт')
    availability = models.BooleanField('в продаже', default=True, db_index=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]


class Order(models.Model):
    address = models.CharField('адрес', max_length=500)
    firstname = models.CharField('имя', max_length=255)
    lastname = models.CharField('фамилия', max_length=255, blank=True)
    phonenumber = PhoneNumberField('мобильный номер', db_index=True)

    def __str__(self):
        return f'Заказ {self.firstname} {self.address} {self.phonenumber}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItemQuerySet(models.QuerySet):

    def add_order_sum(self):
        return self.annotate(sum_total=ExpressionWrapper(Sum('product__price') *
                                                         F('quantity'),
                                                         output_field=
                                                         DecimalField()))

    def add_order_fields(self):
        return self.annotate(address=F('order__address')). \
            annotate(phonenumber=F('order__phonenumber')). \
            annotate(name=Concat(F('order__firstname'), Value(' '),
                                 F('order__lastname'),
                                 output_field=CharField()))


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_items',
                              verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='order_products',
                                verbose_name='продукт')
    quantity = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(500)],
                                   verbose_name='количество')

    def __str__(self):
        return f'{self.product} {self.quantity}'

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'
