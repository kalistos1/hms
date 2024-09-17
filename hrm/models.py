from django.db import models
from accounts.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(r'^\+?1?\d{9,15}$', _('Enter a valid phone number.'))
    ])
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], null=True, blank=True)
    skills = models.ManyToManyField('Skill', related_name='employees', blank=True)
    certifications = models.ManyToManyField('Certification', related_name='employees', blank=True)

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name()} - {self.user.email}"
        else:
            return "Employee without system user"



# Skill Model
class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Certification Model
class Certification(models.Model):
    name = models.CharField(max_length=100)
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    

# Attendance Model
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True, blank=True)
    late_arrival = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['check_in']),
            models.Index(fields=['employee']),
        ]


    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.check_in}"


# Leave Request Model

class LeaveRequest(models.Model):
    class LeaveType(models.TextChoices):
        SICK = 'sick', 'Sick'
        VACATION = 'vacation', 'Vacation'
        PERSONAL = 'personal', 'Personal'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=50, choices=LeaveType.choices)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, choices=Status.choices)
    reason = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='leave_attachments/', null=True, blank=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be after end date.')

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
            models.Index(fields=['employee']),
        ]
    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.leave_type} from {self.start_date} to {self.end_date}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payrolls')
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    bonus = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    deductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    tax_deductions = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    payment_date = models.DateField()
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    overtime_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"Payroll for {self.employee.user.get_full_name()} - {self.payment_date}"

    def calculate_total_pay(self):
        """Calculate total pay including salary, bonus, and overtime pay"""
        return self.salary + (self.bonus or 0) + (self.overtime_pay or 0)

# Performance Review Model
class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    review_date = models.DateField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    improvement_plan = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['review_date']),
        ]

    def __str__(self):
        return f"Review for {self.employee.user.get_full_name()} - {self.review_date}"

# Recruitment Model
class Recruitment(models.Model):
    position = models.CharField(max_length=255)
    job_description = models.TextField()
    application_deadline = models.DateField()
    application_status = models.CharField(max_length=50, choices=[('open', 'Open'), ('under_review', 'Under Review'), ('closed', 'Closed')])

    def __str__(self):
        return f"Recruitment for {self.position} - {self.application_status}"

# Training Model
class Training(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    covered_by_company = models.BooleanField(default=True)
    certification_expiry = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    completion_date = models.DateField()

    class Meta:
        unique_together = ('employee', 'training')


# Employee Contract Model
class EmployeeContract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts')
    contract_type = models.CharField(max_length=50, choices=[('full_time', 'Full-Time'), ('part_time', 'Part-Time'), ('temporary', 'Temporary')])
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    amendments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Contract for {self.employee.user.get_full_name()} - {self.contract_type}"

# Benefits Model
class Benefits(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='benefits')
    benefit_type = models.CharField(max_length=255)
    provider = models.CharField(max_length=255)
    coverage_details = models.TextField()
    eligibility_criteria = models.TextField()

    def __str__(self):
        return f"Benefits for {self.employee.user.get_full_name()} - {self.benefit_type}"

# Disciplinary Action Model
class DisciplinaryAction(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='disciplinary_actions')
    action_type = models.CharField(max_length=50, choices=[('warning', 'Warning'), ('suspension', 'Suspension'), ('termination', 'Termination')])
    action_date = models.DateField()
    description = models.TextField()
    follow_up_actions = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['action_date']),
        ]

    def __str__(self):
        return f"Disciplinary Action for {self.employee.user.get_full_name()} - {self.action_type}"

# Staff On Duty Model
class StaffOnDuty(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='shifts')
    shift_type = models.CharField(max_length=50, choices=[('morning', 'Morning'), ('afternoon', 'Afternoon'), ('night', 'Night')])
    shift_location = models.CharField(max_length=255, blank=True, null=True)
    shift_date = models.DateField()

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.shift_type} shift on {self.shift_date}"

# Staff Schedules Model
class StaffSchedules(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules')
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift_coverage = models.CharField(max_length=255, blank=True, null=True)
    schedule_changes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Schedule for {self.employee.user.get_full_name()} - {self.schedule_date}"

# Leave Balance Model
class LeaveBalance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.CharField(max_length=50, choices=[('sick', 'Sick'), ('vacation', 'Vacation'), ('personal', 'Personal')])
    balance = models.DecimalField(max_digits=5, decimal_places=2)
    accrual_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    carry_over_policy = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Leave Balance for {self.employee.user.get_full_name()} - {self.leave_type}"

# HR Document Model
class HRDocument(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='hr_documents')
    document_type = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='hr_documents/')
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Document for {self.employee.user.get_full_name()} - {self.document_type}"

# Employee Exit Model
class EmployeeExit(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='exits')
    exit_date = models.DateField()
    exit_reason = models.TextField()
    last_working_day = models.DateField()
    exit_interview = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Exit for {self.employee.user.get_full_name()} - {self.exit_date}"

# Job Posting Model
class JobPosting(models.Model):
    position = models.CharField(max_length=255)
    job_description = models.TextField()
    application_deadline = models.DateField()
    application_status = models.CharField(max_length=50, choices=[('open', 'Open'), ('under_review', 'Under Review'), ('closed', 'Closed')])

    def __str__(self):
        return f"Job Posting for {self.position} - {self.application_status}"

# Employee Recognition Model
class EmployeeRecognition(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='recognitions')
    recognition_date = models.DateField()
    award_type = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Recognition for {self.employee.user.get_full_name()} - {self.award_type}"

# Health and Safety Model
class HealthAndSafety(models.Model):
    incident_date = models.DateField()
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='health_and_safety_reports')
    incident_description = models.TextField()
    safety_training_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Incident Report for {self.employee.user.get_full_name()} - {self.incident_date}"

# Employee Feedback Model
class EmployeeFeedback(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_date = models.DateField()
    survey_name = models.CharField(max_length=255)
    feedback_comments = models.TextField()

    def __str__(self):
        return f"Feedback for {self.employee.user.get_full_name()} - {self.feedback_date}"
