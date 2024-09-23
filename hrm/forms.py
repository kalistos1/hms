from django import forms
from .models import *
import datetime


# Generate all hours in 24-hour format
TIME_CHOICES = [(datetime.time(hour=i), '{:02d}:00'.format(i)) for i in range(24)]



class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name',]

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Department Name'})
      

class DepartmentLocationForm(forms.ModelForm):
    class Meta:
        model = DepartmentLocation
        fields = ['department', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super(DepartmentLocationForm, self).__init__(*args, **kwargs)
        self.fields['department'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Department'})
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter Location Name'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Location Description'})



class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'department', 'emergency_contact_name', 'emergency_contact_relationship', 'emergency_contact_phone']

    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select User'})
        self.fields['department'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Department Location'})
        self.fields['emergency_contact_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Emergency Contact Name'})
        self.fields['emergency_contact_relationship'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Relationship with Emergency Contact'})
        self.fields['emergency_contact_phone'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Emergency Contact Phone Number'})
        
 
class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee', 'leave_type', 'start_date', 'end_date', 'status', 'reason', 'attachment']

    def __init__(self, *args, **kwargs):
        super(LeaveRequestForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Employee'})
        self.fields['leave_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Leave Type'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Start Date'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select End Date'})
        self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Status'})
        self.fields['reason'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Provide Reason for Leave'})
        self.fields['attachment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload Attachment'})
        


class StaffScheduleForm(forms.ModelForm):
    class Meta:
        model = StaffSchedules
        fields = ['employee', 'schedule_date', 'start_time', 'end_time', 'schedule_shift_type', 'schedule_type']
    
    start_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    end_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super(StaffScheduleForm, self).__init__(*args, **kwargs)
        
        self.fields['employee'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Adults'})
        self.fields['schedule_date'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
        self.fields['schedule_shift_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
        self.fields['schedule_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Children'})
       
       

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = [
            'employee', 'salary', 'bonus', 'deductions', 'tax_deductions',
            'payment_date', 'overtime_hours', 'overtime_pay'
        ]

    def __init__(self, *args, **kwargs):
        super(PayrollForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['salary'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Salary'
        })
        self.fields['bonus'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Bonus Amount'
        })
        self.fields['deductions'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Deductions'
        })
        self.fields['tax_deductions'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Tax Deductions'
        })
        self.fields['payment_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Payment Date'
        })
        self.fields['overtime_hours'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Overtime Hours'
        })
        self.fields['overtime_pay'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Overtime Pay'
        })


class PerformanceReviewForm(forms.ModelForm):
    class Meta:
        model = PerformanceReview
        fields = [
            'employee', 'review_date', 'reviewer', 'rating',
            'comments', 'goals', 'improvement_plan'
        ]

    def __init__(self, *args, **kwargs):
        super(PerformanceReviewForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['review_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Review Date'
        })
        self.fields['reviewer'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Reviewer'
        })
        self.fields['rating'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Rating'
        })
        self.fields['comments'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Comments'
        })
        self.fields['goals'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Set Goals'
        })
        self.fields['improvement_plan'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Improvement Plan'
        })


class RecruitmentForm(forms.ModelForm):
    class Meta:
        model = Recruitment
        fields = [
            'position', 'job_description', 'application_deadline',
            'application_status'
        ]

    def __init__(self, *args, **kwargs):
        super(RecruitmentForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Position Title'
        })
        self.fields['job_description'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Job Description'
        })
        self.fields['application_deadline'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Application Deadline'
        })
        self.fields['application_status'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Application Status'
        })


class TrainingForm(forms.ModelForm):
    class Meta:
        model = Training
        fields = [
            'name', 'description', 'start_date', 'end_date', 'cost',
            'covered_by_company', 'certification_expiry'
        ]

    def __init__(self, *args, **kwargs):
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Training Name'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Description'
        })
        self.fields['start_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Start Date'
        })
        self.fields['end_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select End Date'
        })
        self.fields['cost'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Cost'
        })
        self.fields['covered_by_company'].widget.attrs.update({
            'class': 'form-check-input', 'placeholder': ''
        })
        self.fields['certification_expiry'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Certification Expiry Date'
        })


class EmployeeTrainingForm(forms.ModelForm):
    class Meta:
        model = EmployeeTraining
        fields = ['employee', 'training', 'completion_date']

    def __init__(self, *args, **kwargs):
        super(EmployeeTrainingForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['training'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Training'
        })
        self.fields['completion_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Completion Date'
        })


class BenefitsForm(forms.ModelForm):
    class Meta:
        model = Benefits
        fields = [
            'employee', 'benefit_type', 'provider',
            'coverage_details', 'eligibility_criteria'
        ]

    def __init__(self, *args, **kwargs):
        super(BenefitsForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['benefit_type'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Benefit Type'
        })
        self.fields['provider'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Provider Name'
        })
        self.fields['coverage_details'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Coverage Details'
        })
        self.fields['eligibility_criteria'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Eligibility Criteria'
        })


class DisciplinaryActionForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryAction
        fields = [
            'employee', 'action_type', 'action_date',
            'description', 'follow_up_actions'
        ]

    def __init__(self, *args, **kwargs):
        super(DisciplinaryActionForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['action_type'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Action Type'
        })
        self.fields['action_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Action Date'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Description'
        })
        self.fields['follow_up_actions'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Follow-Up Actions (Optional)'
        })


class LeaveBalanceForm(forms.ModelForm):
    class Meta:
        model = LeaveBalance
        fields = [
            'employee', 'leave_type', 'balance',
            'accrual_rate', 'carry_over_policy'
        ]

    def __init__(self, *args, **kwargs):
        super(LeaveBalanceForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['leave_type'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Leave Type'
        })
        self.fields['balance'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Balance'
        })
        self.fields['accrual_rate'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Accrual Rate (Optional)'
        })
        self.fields['carry_over_policy'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Carry Over Policy (Optional)'
        })


class HRDocumentForm(forms.ModelForm):
    class Meta:
        model = HRDocument
        fields = [
            'employee', 'document_type', 'document_file', 'expiration_date'
        ]

    def __init__(self, *args, **kwargs):
        super(HRDocumentForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['document_type'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Document Type'
        })
        self.fields['document_file'].widget.attrs.update({
            'class': 'form-control-file'
        })
        self.fields['expiration_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Expiration Date (Optional)'
        })


class EmployeeExitForm(forms.ModelForm):
    class Meta:
        model = EmployeeExit
        fields = [
            'employee', 'exit_date', 'exit_reason',
            'last_working_day', 'exit_interview'
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeExitForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['exit_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Exit Date'
        })
        self.fields['exit_reason'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Exit Reason'
        })
        self.fields['last_working_day'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Last Working Day'
        })
        self.fields['exit_interview'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Exit Interview Details (Optional)'
        })


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'position', 'job_description', 'application_deadline',
            'application_status'
        ]

    def __init__(self, *args, **kwargs):
        super(JobPostingForm, self).__init__(*args, **kwargs)
        self.fields['position'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Position Title'
        })
        self.fields['job_description'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Job Description'
        })
        self.fields['application_deadline'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Application Deadline'
        })
        self.fields['application_status'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Application Status'
        })


class EmployeeRecognitionForm(forms.ModelForm):
    class Meta:
        model = EmployeeRecognition
        fields = [
            'employee', 'recognition_date', 'award_type', 'description'
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeRecognitionForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['recognition_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Recognition Date'
        })
        self.fields['award_type'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Award Type'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Description'
        })


class HealthAndSafetyForm(forms.ModelForm):
    class Meta:
        model = HealthAndSafety
        fields = [
            'incident_date', 'employee', 'incident_description',
            'safety_training_completed'
        ]

    def __init__(self, *args, **kwargs):
        super(HealthAndSafetyForm, self).__init__(*args, **kwargs)
        self.fields['incident_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Incident Date'
        })
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['incident_description'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Describe the Incident'
        })
        self.fields['safety_training_completed'].widget.attrs.update({
            'class': 'form-check-input'
        })


class EmployeeFeedbackForm(forms.ModelForm):
    class Meta:
        model = EmployeeFeedback
        fields = [
            'employee', 'feedback_date', 'survey_name', 'feedback_comments'
        ]

    def __init__(self, *args, **kwargs):
        super(EmployeeFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['employee'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Employee'
        })
        self.fields['feedback_date'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Select Feedback Date'
        })
        self.fields['survey_name'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Survey Name'
        })
        self.fields['feedback_comments'].widget.attrs.update({
            'class': 'form-control', 'placeholder': 'Enter Feedback Comments'
        })
