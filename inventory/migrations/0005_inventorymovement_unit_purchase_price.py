# Generated by Django 5.1 on 2024-10-16 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_stockreceipt_selling_price_per_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventorymovement',
            name='unit_purchase_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]
