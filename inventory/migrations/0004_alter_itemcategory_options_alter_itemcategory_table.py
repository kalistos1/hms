# Generated by Django 5.1 on 2024-10-04 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_itemcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemcategory',
            options={'verbose_name_plural': 'inventory_categories'},
        ),
        migrations.AlterModelTable(
            name='itemcategory',
            table='inventory_categories',
        ),
    ]
