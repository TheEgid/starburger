from django.db import migrations


def move_backward(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for item in OrderItem.objects.all():
        item.value = 0
        item.save()


def fill_values(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    for item in OrderItem.objects.all():
        if item.value != 0:
            continue
        item.value = item.product.price * item.quantity
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0040_auto_20210331_2222'),
    ]

    operations = [
        migrations.RunPython(fill_values, move_backward),
    ]
