# Generated by Django 4.2 on 2023-05-16 03:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_regis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryaddres',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='customer',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='DeliveryAddres',
        ),
        migrations.DeleteModel(
            name='Rate',
        ),
    ]