# Generated by Django 5.1 on 2024-09-12 17:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0021_alter_payment_status'),
        ('inventory', '0002_alert'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consumableitem',
            name='reorder_level',
        ),
        migrations.AddField(
            model_name='consumableitem',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='consumableitem',
            name='unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='equipment',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('in_repair', 'In Repair'), ('out_of_service', 'Out of Service')], db_index=True, default='active', max_length=20),
        ),
        migrations.AddField(
            model_name='supplier',
            name='notes',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='alert',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='consumableitem',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consumable_items', to='bookings.hotel'),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='equipments', to='inventory.supplier'),
        ),
        migrations.AlterField(
            model_name='equipmentauditlog',
            name='changed_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment_audit_logs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='equipmentauditlog',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_logs', to='inventory.equipment'),
        ),
        migrations.AlterField(
            model_name='equipmentusagelog',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usage_logs', to='inventory.equipment'),
        ),
        migrations.AlterField(
            model_name='equipmentusagelog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='equipment_usage_logs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='inspectionchecklist',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inspection_checklists', to='inventory.equipment'),
        ),
        migrations.AlterField(
            model_name='insurancepolicy',
            name='equipment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='insurance_policies', to='inventory.equipment'),
        ),
    ]