# Generated by Django 5.1 on 2024-10-21 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0002_employee_role_delete_employeerole'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='shift_type',
            field=models.CharField(blank=True, choices=[('Morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night'), ('24_hours', '24_hours'), ('12_hours', '12_hours')], max_length=50, null=True),
        ),
    ]