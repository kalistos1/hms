# Generated by Django 5.1 on 2024-11-24 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_reservation_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='online_reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='bookings.reservation'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='booking',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='bookings.booking'),
        ),
    ]
