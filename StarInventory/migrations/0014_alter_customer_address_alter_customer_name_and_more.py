# Generated by Django 4.0.4 on 2022-05-26 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StarInventory', '0013_alter_customer_address_alter_supplier_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]