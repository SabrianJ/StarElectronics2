# Generated by Django 4.0.4 on 2022-05-08 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StarInventory', '0004_part_available_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerorder',
            name='confirm',
            field=models.BooleanField(default=False),
        ),
    ]
