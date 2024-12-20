# Generated by Django 5.1 on 2024-10-28 19:31

import django.db.models.deletion
import shortuuid.django_fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hrm', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('discount_percentage', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PosCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=50, null=True)),
                ('customer_room_number', models.CharField(blank=True, max_length=10, null=True)),
                ('pos_customer', models.BooleanField(blank=True, default=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('icon_class', models.CharField(choices=[('fa-bowl-rice', 'fa-bowl-rice'), ('fa-cocktail', 'fa-cocktail'), ('fa-ice-cream', 'fa-ice-cream'), ('fa-drumstick-bite', 'fa-drumstick-bite'), ('fa-hamburger', 'fa-hamburger')], default='fa-utensils', max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('room_charge', models.BooleanField(default=False)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pos.discount')),
                ('staff', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hrm.employee')),
                ('waiter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='hrm.employee')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pos.poscustomer')),
            ],
        ),
        migrations.CreateModel(
            name='PosPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('CASH', 'CASH'), ('CARD', 'CARD'), ('ROOM_CHARGE', 'ROOM_CHARGE')], max_length=50)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_status', models.CharField(choices=[('PAID', 'PAID'), ('PARTIALLY_PAID', 'PARTIALLY_PAID'), ('UNPAID', 'UNPAID')], default='PAID', max_length=20)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz', length=10, max_length=20, prefix='', unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, default='pos.jpg', null=True, upload_to='pos')),
                ('stock_quantity', models.PositiveIntegerField()),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('department_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hrm.departmentlocation')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pos.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.product')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='pos.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.product')),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refund_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reason', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.order')),
            ],
        ),
    ]
