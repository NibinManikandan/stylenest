# Generated by Django 5.0.2 on 2024-03-20 10:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_purchase', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('expiry_date', models.DateField()),
                ('usage_limit', models.PositiveIntegerField(default=1)),
                ('used_count', models.PositiveBigIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CouponUsage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.PositiveBigIntegerField(null=True)),
                ('appled_on', models.DateTimeField(auto_now_add=True)),
                ('coupon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='usage', to='coupon.coupons')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='coupon', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
