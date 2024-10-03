from django.db import models
from accounts.models import User
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.db.models.signals import pre_save


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure department name is unique
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        
class DepartmentLocation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('department', 'name')

    def __str__(self):
        return f"{self.name} -> {self.department.name}"
    
    

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Prevent duplicate skill names

    def __str__(self):
        return self.name


class Certification(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Prevent duplicate certifications
    expiration_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name
    

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    department_location = models.ForeignKey(DepartmentLocation, on_delete=models.CASCADE, related_name='employee_department',blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_relationship = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, null=True, blank=True, )
    skills = models.ManyToManyField('Skill', related_name='employees', blank=True)
    certifications = models.ManyToManyField('Certification', related_name='employees', blank=True)
    
    # Contract-related fields
    contract_type = models.CharField(max_length=50, choices=[('full_time', 'Full-Time'), ('part_time', 'Part-Time'), ('temporary', 'Temporary')], null=True, blank=True)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    contract_renewal_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name() if self.user else 'No User'}"
    

class EmployeeRole(models.Model):

    WorkerRoles = (
        ('front_desk', 'front_desk'), 
        ('pos_staff', 'pos_staff'), 
        ('hr_staff', 'hr_ataff'), 
        ('manager', 'manager'),
        ('waiter', 'waiter'),
        ('supervisor', 'supervisor'),
        ('potter', 'potter'),
        ('accountant', 'accountant'),
        ('store_keeper', 'store_keeper'),
        ('security', 'security'), 
    )
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    department_location = models.ForeignKey(DepartmentLocation, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    role = models.CharField(max_length=50, choices=WorkerRoles)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"{self.employee.user.get_full_name()} -> {self.role}"


class Attendance(models.Model):
    SHIFTTYPE = (
        ('24_hours', '24_hours'), 
        ('Morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night')
    )

   
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    check_in = models.DateTimeField(auto_now_add= True)
    check_out = models.DateTimeField(null=True, blank=True)
    shift_type = models.CharField(max_length=50, choices=SHIFTTYPE,blank=True, null=True,)
    shift_location = models.ForeignKey(DepartmentLocation, blank=True, null=True, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    late_arrival = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=['check_in']), models.Index(fields=['employee'])]
        unique_together = ('employee', 'check_in')


    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.check_in}"
    

# Staff Schedules Model
class StaffSchedules(models.Model):
    
    SCHEDULESHIFTTYPE = (
        ('24_hours', '24_hours'), 
        ('Morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night')
    )
    scheduletype =(
        ('Pos_shift', 'Pos_shift'),
        ('Frontdesk_shift', 'Frontdesk_shift'),
        ('Potter_shift', 'Potter_shift'),
        ('Supervisor_shift', 'Supervisor_shift'),
        ('Waiter_shift', 'Waiter_shift'),
        ('Accountant_shift', 'Accountant_shift'),
        ('Store_keeper_shift', 'Store_keeper_shift'),
        ('Security_shift', 'Security_shift'), 
        ('Hr_shift', 'hr_shift'),
        ('Manager', 'Manager'), 
    )

    SCHEDULE_STATUS = (
        ('True','True'),
        ('False','False'),
        ('Ended','Ended'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='schedules')
    schedule_start_date = models.DateField()
    start_time = models.TimeField()
    schedule_end_date = models.DateField()
    end_time = models.TimeField()
    schedule_shift_type = models.CharField(max_length=50, choices =SCHEDULESHIFTTYPE, blank=True, null=True)
    schedule_type = models.CharField(max_length=50, choices= scheduletype,blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.CharField(max_length =20, default="False", choices = SCHEDULE_STATUS)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule for {self.employee.user.get_full_name()} - {self.schedule_start_date}"


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

    class Meta:
        indexes = [models.Index(fields=['start_date', 'end_date']), models.Index(fields=['employee'])]

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date cannot be after end date.')

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
        return f"Payroll for {self.employee} - {self.payment_date}"

    def calculate_total_pay(self):
        return self.salary + (self.bonus or 0) + (self.overtime_pay or 0)



class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_reviews')
    review_date = models.DateField()
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    improvement_plan = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=['review_date'])]

    def __str__(self):
        return f"Review for {self.employee} - {self.review_date}"


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
