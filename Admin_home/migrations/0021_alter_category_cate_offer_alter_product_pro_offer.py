# Generated by Django 5.0.2 on 2024-03-29 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Admin_home', '0020_alter_category_cate_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='Cate_offer',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='Pro_offer',
            field=models.IntegerField(default=0),
        ),
    ]