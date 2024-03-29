# Generated by Django 4.1.7 on 2024-02-02 14:25

import apps.seller.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SellerApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255, null=True, unique=True, validators=[apps.seller.models.validate_seller_name])),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('approved', 'Одобрено'), ('rejected', 'Отклонено')], max_length=20)),
                ('status_changed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_applications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255, null=True, unique=True, validators=[apps.seller.models.validate_seller_name])),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('premium_tariff', models.IntegerField(choices=[(1, 'Basic'), (2, 'Standard'), (3, 'Premium')], default=1)),
                ('avatarka', models.ImageField(blank=True, null=True, upload_to='sellers_avatarka/')),
                ('background', models.ImageField(blank=True, null=True, upload_to='sellers_background/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
