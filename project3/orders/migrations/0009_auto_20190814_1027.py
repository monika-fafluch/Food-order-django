# Generated by Django 2.0.3 on 2019-08-14 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_auto_20190809_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='topping',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='toppings', to='orders.Items'),
        ),
        migrations.AddField(
            model_name='orders',
            name='topping_steak',
            field=models.ForeignKey(blank=True, default=0, on_delete=django.db.models.deletion.CASCADE, related_name='toppings_steak', to='orders.Items'),
        ),
    ]