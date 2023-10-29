# Generated by Django 4.1.7 on 2023-10-26 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_review'),
        ('product', '0006_remove_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reviews',
            field=models.ManyToManyField(blank=True, related_name='products', to='user.review'),
        ),
    ]