# Generated by Django 4.1.7 on 2023-11-15 13:23

import apps.product.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='characteristicimage',
            name='characteristic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.productcharacteristic'),
        ),
        migrations.AlterField(
            model_name='characteristicimage',
            name='image',
            field=models.ImageField(upload_to=apps.product.models.characteristic_image_path),
        ),
        migrations.AlterField(
            model_name='productcharacteristic',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
