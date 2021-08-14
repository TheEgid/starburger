# Generated by Django 3.2.5 on 2021-07-09 16:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ('foodcartapp', '0044_auto_20210404_2345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addresspoint',
            name='query_at',
        ),
        migrations.AddField(
            model_name='addresspoint',
            name='registered_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name='дата и время регистрации'),
        ),
    ]