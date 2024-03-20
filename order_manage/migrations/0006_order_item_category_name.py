# Generated by Django 5.0.2 on 2024-03-20 15:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_home', '0013_product_pro_offer_product_stock'),
        ('order_manage', '0005_alter_order_item_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_item',
            name='category_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Admin_home.category'),
        ),
    ]
