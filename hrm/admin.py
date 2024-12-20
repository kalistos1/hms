from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(DepartmentLocation)
admin.site.register( DepartmentUser)
admin.site.register(Employee)
# admin.site.register(EmployeeRole)
admin.site.register(Skill)
admin.site.register(Certification)

admin.site.register(StaffSchedules)
admin.site.register(Attendance)
admin.site.register(LeaveRequest)
admin.site.register(Payroll)
admin.site.register(PerformanceReview)
admin.site.register(Recruitment)
admin.site.register(Training)
admin.site.register(EmployeeTraining)
admin.site.register(Benefits)
admin.site.register(DisciplinaryAction)

admin.site.register(LeaveBalance)
admin.site.register(HRDocument)
admin.site.register(EmployeeExit)
admin.site.register(JobPosting)
admin.site.register(EmployeeRecognition)
admin.site.register(HealthAndSafety)
admin.site.register(EmployeeFeedback)