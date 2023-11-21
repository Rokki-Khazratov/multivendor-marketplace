# Generated by Django 4.1.7 on 2023-11-19 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_alter_characteristicimage_characteristic_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcharacteristic',
            name='images',
            field=models.ManyToManyField(related_name='characteristics', to='product.characteristicimage'),
        ),
        migrations.AlterField(
            model_name='characteristicimage',
            name='characteristic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristic_images', to='product.productcharacteristic'),
        ),
    ]