# Generated by Django 5.1 on 2024-09-13 14:06

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('expiration_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobPosting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('application_deadline', models.DateField()),
                ('application_status', models.CharField(choices=[('open', 'Open'), ('under_review', 'Under Review'), ('closed', 'Closed')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('application_deadline', models.DateField()),
                ('application_status', models.CharField(choices=[('open', 'Open'), ('under_review', 'Under Review'), ('closed', 'Closed')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('covered_by_company', models.BooleanField(default=True)),
                ('certification_expiry', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=255, null=True)),
                ('emergency_contact_relationship', models.CharField(blank=True, max_length=255, null=True)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator('^\\+?1?\\d{9,15}$', 'Enter a valid phone number.')])),
                ('address', models.TextField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True)),
                ('certifications', models.ManyToManyField(blank=True, related_name='employees', to='hrm.certification')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
                ('skills', models.ManyToManyField(blank=True, related_name='employees', to='hrm.skill')),
            ],
        ),
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('benefit_type', models.CharField(max_length=255)),
                ('provider', models.CharField(max_length=255)),
                ('coverage_details', models.TextField()),
                ('eligibility_criteria', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='benefits', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(choices=[('full_time', 'Full-Time'), ('part_time', 'Part-Time'), ('temporary', 'Temporary')], max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('renewal_date', models.DateField(blank=True, null=True)),
                ('amendments', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeExit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exit_date', models.DateField()),
                ('exit_reason', models.TextField()),
                ('last_working_day', models.DateField()),
                ('exit_interview', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exits', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_date', models.DateField()),
                ('survey_name', models.CharField(max_length=255)),
                ('feedback_comments', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeRecognition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recognition_date', models.DateField()),
                ('award_type', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recognitions', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='HealthAndSafety',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incident_date', models.DateField()),
                ('incident_description', models.TextField()),
                ('safety_training_completed', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='health_and_safety_reports', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='HRDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=255)),
                ('document_file', models.FileField(upload_to='hr_documents/')),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hr_documents', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='LeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('sick', 'Sick'), ('vacation', 'Vacation'), ('personal', 'Personal')], max_length=50)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=5)),
                ('accrual_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('carry_over_policy', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_balances', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('bonus', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('deductions', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('tax_deductions', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('payment_date', models.DateField()),
                ('overtime_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('overtime_pay', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payrolls', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='StaffOnDuty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift_type', models.CharField(choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')], max_length=50)),
                ('shift_location', models.CharField(blank=True, max_length=255, null=True)),
                ('shift_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='StaffSchedules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('shift_coverage', models.CharField(blank=True, max_length=255, null=True)),
                ('schedule_changes', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='hrm.employee')),
            ],
        ),
        migrations.CreateModel(
            name='DisciplinaryAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[('warning', 'Warning'), ('suspension', 'Suspension'), ('termination', 'Termination')], max_length=50)),
                ('action_date', models.DateField()),
                ('description', models.TextField()),
                ('follow_up_actions', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='disciplinary_actions', to='hrm.employee')),
            ],
            options={
                'indexes': [models.Index(fields=['action_date'], name='hrm_discipl_action__4e964f_idx')],
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField()),
                ('check_out', models.DateTimeField(blank=True, null=True)),
                ('late_arrival', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendances', to='hrm.employee')),
            ],
            options={
                'indexes': [models.Index(fields=['check_in'], name='hrm_attenda_check_i_7db142_idx'), models.Index(fields=['employee'], name='hrm_attenda_employe_514bde_idx')],
            },
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_type', models.CharField(choices=[('sick', 'Sick'), ('vacation', 'Vacation'), ('personal', 'Personal')], max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=50)),
                ('reason', models.TextField(blank=True, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='leave_attachments/')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='hrm.employee')),
            ],
            options={
                'indexes': [models.Index(fields=['start_date', 'end_date'], name='hrm_leavere_start_d_78a143_idx'), models.Index(fields=['employee'], name='hrm_leavere_employe_270fff_idx')],
            },
        ),
        migrations.CreateModel(
            name='PerformanceReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_date', models.DateField()),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comments', models.TextField(blank=True, null=True)),
                ('goals', models.TextField(blank=True, null=True)),
                ('improvement_plan', models.TextField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performance_reviews', to='hrm.employee')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['review_date'], name='hrm_perform_review__0e0aa7_idx')],
            },
        ),
        migrations.CreateModel(
            name='EmployeeTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm.employee')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hrm.training')),
            ],
            options={
                'unique_together': {('employee', 'training')},
            },
        ),
    ]