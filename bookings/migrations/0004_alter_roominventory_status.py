# Generated by Django 5.1 on 2024-10-11 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_roominventory_amenity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roominventory',
            name='status',
            field=models.CharField(choices=[('in_repairs', 'in_repairs'), ('in_use', 'In Use'), ('decomitioned', 'decomitioned')], max_length=50),
        ),
    ]
