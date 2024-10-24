# Generated by Django 5.1 on 2024-10-22 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_remove_couponusers_full_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomservices',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roomservice', to='bookings.booking'),
        ),
        migrations.DeleteModel(
            name='Refund',
        ),
    ]
