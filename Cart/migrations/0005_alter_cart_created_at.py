# Generated by Django 5.0.2 on 2024-03-04 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cart', '0004_rename_customuser_cart_user_cart_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
