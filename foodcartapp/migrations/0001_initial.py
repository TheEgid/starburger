# Generated by Django 3.0.7 on 2020-06-05 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10)),
                ('pincode', models.CharField(max_length=7)),
                ('address', models.CharField(max_length=256)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gst', models.DecimalField(decimal_places=2, max_digits=4)),
                ('hoteladmin',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='foodcartapp.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(default=1)),
                ('order_time', models.DateTimeField()),
                ('delivery_time', models.DateTimeField(blank=True,
                                                       null=True)),
                (
                    'amount', models.DecimalField(decimal_places=2,
                                                  max_digits=15)),
                ('order_type', models.SmallIntegerField(default=1)),
                ('customer', models.ForeignKey(
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    to='foodcartapp.CustomUser')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('half_price', models.DecimalField(decimal_places=2,
                                                   max_digits=8)),
                ('full_price', models.DecimalField(decimal_places=2,
                                                   max_digits=8)),
                ('availabilty', models.BooleanField(default=True)),
                ('image', models.ImageField(upload_to='')),
                ('special_status', models.BooleanField(default=False)),
                ('category', models.CharField(max_length=50)),
                ('hotel', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='foodcartapp.Hotel')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(
                    auto_created=True, primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(
                    decimal_places=2, max_digits=8)),
                ('order', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='foodcartapp.Order')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='foodcartapp.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=7)),
                ('city', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='foodcartapp.City')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='location',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to='foodcartapp.Location'),
        ),
    ]
