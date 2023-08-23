# Generated by Django 4.2.4 on 2023-08-23 05:18

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurantApi', '0006_rename_item_deliverycrew_orderid'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='deliverycrew',
            unique_together={('orderId', 'delivery')},
        ),
    ]
