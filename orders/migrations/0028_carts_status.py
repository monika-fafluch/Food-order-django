# Generated by Django 2.0.3 on 2019-08-19 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0027_carts'),
    ]

    operations = [
        migrations.AddField(
            model_name='carts',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
