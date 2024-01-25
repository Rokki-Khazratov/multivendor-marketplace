# Generated by Django 4.1.7 on 2024-01-25 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='characteristics',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='characteristics',
            field=models.ManyToManyField(through='product.CharacteristicQuantity', to='product.productcharacteristic'),
        ),
    ]
