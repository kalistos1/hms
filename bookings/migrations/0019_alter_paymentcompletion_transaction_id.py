# Generated by Django 5.1 on 2024-09-11 18:57

import shortuuid.django_fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0018_paymentcompletion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcompletion',
            name='transaction_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijklmnopqrstuvxyz', length=15, max_length=25, prefix='', unique=True),
        ),
    ]