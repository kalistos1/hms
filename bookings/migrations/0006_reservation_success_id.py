# Generated by Django 5.1 on 2024-11-24 18:55

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_payment_online_reservation_alter_payment_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='success_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz1234567890', length=300, max_length=505, prefix=''),
        ),
    ]