# Generated by Django 5.1 on 2024-10-21 10:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='room',
        ),
        migrations.AddField(
            model_name='booking',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookings.room'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookings.room'),
        ),
    ]
