from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import DecimalField, CharField
from django.db.models import Value, Sum, F, ExpressionWrapper
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


class RestaurantMenuItemQuerySet(models.QuerySet):
    def add_available_rests(self):
        return self.filter(availability=True). \
            annotate(rest_name=ExpressionWrapper(F('restaurant__name'),
                                                 output_field=CharField())). \
            annotate(rest_address=ExpressionWrapper(F('restaurant__address'),
                                                 output_field=CharField()))

class RestaurantMenuItem(models.Model):

    objects = RestaurantMenuItemQuerySet.as_manager()

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


class OrderQuerySet(models.QuerySet):

    def add_name(self):
        return self.annotate(
            name=Concat(F('firstname'), Value(' '), F('lastname'),
                        output_field=CharField()))

    def add_sum_ordered_prices(self):
        return self.prefetch_related('order_items__product'). \
            annotate(sum_order_prices=Sum('order_items__value'))

    def add_sum_current_prices(self):
        return self.annotate(sum_current_prices=Sum(
            F('order_items__product__price') * F('order_items__quantity'),
            output_field=DecimalField()))


class Order(models.Model):
    objects = OrderQuerySet.as_manager()

    class Statuses(models.TextChoices):
        UNTREATED = 'UN', _('Необработанный')
        CANCELED = 'CA', _('Отмененный')
        ACCEPTED = 'AC', _('Принятый')
        PRODUCED = 'PR', _('Приготовленный')
        SHIPPED = 'SH', _('Отгруженный')
        COMPLETED = 'CO', _('Выполненный')

    class PaymentMethods(models.TextChoices):
        NOCASH = 'NOCASH', _('Безналично')
        CASH = 'CASH', _('Наличные')

    status = models.CharField('статус', max_length=2, choices=Statuses.choices,
                              default=Statuses.UNTREATED)
    payment_method = models.CharField('способ оплаты', max_length=6,
                                      choices=PaymentMethods.choices,
                                      default=PaymentMethods.NOCASH)
    address = models.CharField('адрес', max_length=500)
    firstname = models.CharField('имя', max_length=255)
    lastname = models.CharField('фамилия', max_length=255, blank=True)
    phonenumber = PhoneNumberField('мобильный номер', db_index=True)
    comment = models.TextField("комментарий", blank=True,
                               help_text='Необязательный комментарий к заказу')
    registrated_at = models.DateTimeField('дата и время регистрации',
                                          default=timezone.now, blank=True,
                                          null=True)
    called_at = models.DateTimeField('дата и время созвона', blank=True,
                                     null=True)
    delivered_at = models.DateTimeField('дата и время доставки',
                                        blank=True, null=True)

    def __str__(self):
        return f'Заказ {self.firstname} {self.address} {self.phonenumber}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_items',
                              verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='order_products',
                                verbose_name='продукт')

    quantity = models.IntegerField(validators=[MinValueValidator(0),
                                               MaxValueValidator(500)],
                                   verbose_name='количество')
    value = models.DecimalField(decimal_places=2, default=0,
                                verbose_name='стоимость', max_digits=8,
                                validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.product} {self.quantity}'

    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказа'

    def save(self, *args, **kwargs):
        self.value = self.product.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
