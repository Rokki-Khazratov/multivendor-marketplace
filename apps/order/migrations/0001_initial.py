# Generated by Django 4.1.7 on 2024-01-30 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0003_remove_cartitem_characteristics_and_more'),
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneClickOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'В ожидании'), (2, 'В пути'), (3, 'Доставлен и ожидает'), (4, 'Забран')], default=1)),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, 'В ожидании'), (2, 'В пути'), (3, 'Доставлен и ожидает'), (4, 'Забран')], default=1)),
                ('is_paid', models.BooleanField(default=False)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('characteristic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcharacteristic')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.ManyToManyField(related_name='order_history', to='order.order')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='OneClickOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('characteristic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productcharacteristic')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.oneclickorder')),
            ],
        ),
    ]
