# Generated by Django 4.2.4 on 2023-08-23 07:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurantApi', '0009_rename_delivery_deliverycrew_delivery_crew_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliverycrew',
            old_name='user',
            new_name='order',
        ),
        migrations.AlterUniqueTogether(
            name='deliverycrew',
            unique_together={('order', 'delivery_crew')},
        ),
    ]