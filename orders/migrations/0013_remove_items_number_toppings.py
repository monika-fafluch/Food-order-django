# Generated by Django 2.0.3 on 2019-08-14 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20190814_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='number_toppings',
        ),
    ]
