# Generated by Django 5.0.2 on 2024-04-19 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manage', '0006_order_item_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_item',
            name='payment_status',
            field=models.CharField(default='Pending', max_length=20),
        ),
    ]