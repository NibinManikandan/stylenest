# Generated by Django 5.0.2 on 2024-02-13 06:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userAuth', '0007_alter_customuser_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
