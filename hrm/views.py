
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def department_list(request):
    departments = Department.objects.all()
    form = DepartmentForm()
    
    context=  {
        'departments': departments,
        'form':form,
        }
    return render(request, 'pages/department.html',context)


# Create a new department
def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Department created successfully')
            return redirect('hrm:departments')
      
    else:
        messages.error(request,'Department created successfully')
        return redirect('hrm:departments')
  


# Update an existing department
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'department_form.html', {'form': form})


# Delete a department
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')
    return render(request, 'department_confirm_delete.html', {'department': department})



# List all department locations
def department_location_list(request):
    locations = DepartmentLocation.objects.all()
    return render(request, 'department_location_list.html', {'locations': locations})


# Create a new department location
def department_location_create(request):
    if request.method == 'POST':
        form = DepartmentLocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_location_list')
    else:
        form = DepartmentLocationForm()
    return render(request, 'department_location_form.html', {'form': form})


# Update an existing department location
def department_location_update(request, pk):
    location = get_object_or_404(DepartmentLocation, pk=pk)
    if request.method == 'POST':
        form = DepartmentLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect('department_location_list')
    else:
        form = DepartmentLocationForm(instance=location)
    return render(request, 'department_location_form.html', {'form': form})


# Delete a department location
def department_location_delete(request, pk):
    location = get_object_or_404(DepartmentLocation, pk=pk)
    if request.method == 'POST':
        location.delete()
        return redirect('department_location_list')
    return render(request, 'department_location_confirm_delete.html', {'location': location})


# List all employees
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})


# Create a new employee
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})


# Update an existing employee
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employee_form.html', {'form': form})


# Delete an employee
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'employee_confirm_delete.html', {'employee': employee})



# List all leave requests
def leave_request_list(request):
    leave_requests = LeaveRequest.objects.all()
    return render(request, 'leave_request_list.html', {'leave_requests': leave_requests})


# Create a new leave request
def leave_request_create(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('leave_request_list')
    else:
        form = LeaveRequestForm()
    return render(request, 'leave_request_form.html', {'form': form})


# Update an existing leave request
def leave_request_update(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES, instance=leave_request)
        if form.is_valid():
            form.save()
            return redirect('leave_request_list')
    else:
        form = LeaveRequestForm(instance=leave_request)
    return render(request, 'leave_request_form.html', {'form': form})


# Delete a leave request
def leave_request_delete(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    if request.method == 'POST':
        leave_request.delete()
        return redirect('leave_request_list')
    return render(request, 'leave_request_confirm_delete.html', {'leave_request': leave_request})


# List all staff schedules
def staff_schedule_list(request):
    schedules = StaffSchedules.objects.all()
    return render(request, 'staff_schedule_list.html', {'schedules': schedules})


# Create a new staff schedule
def staff_schedule_create(request):
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_schedule_list')
    else:
        form = StaffScheduleForm()
    return render(request, 'staff_schedule_form.html', {'form': form})


# Update an existing staff schedule
def staff_schedule_update(request, pk):
    schedule = get_object_or_404(StaffSchedules, pk=pk)
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('staff_schedule_list')
    else:
        form = StaffScheduleForm(instance=schedule)
    return render(request, 'staff_schedule_form.html', {'form': form})


# Delete a staff schedule
def staff_schedule_delete(request, pk):
    schedule = get_object_or_404(StaffSchedules, pk=pk)
    if request.method == 'POST':
        schedule.delete()
        return redirect('staff_schedule_list')
    return render(request, 'staff_schedule_confirm_delete.html', {'schedule': schedule})



# @login_required
def check_in(request):
   
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    
    # Get today's schedule for the employee
    today = timezone.now().date()
    schedule = StaffSchedules.objects.filter(employee=employee, schedule_date=today).first()

    if not schedule:
        messages.error(request, "No schedule found for today.")
        return redirect('home') 
    

    # Check if employee already checked in today
    if Attendance.objects.filter(employee=employee, check_in__date=today, check_out__isnull=True).exists():
        messages.warning(request, "You have already checked in.")
        return redirect('home')  # redirect to a relevant page
    
    # Check for lateness based on schedule
    scheduled_start_time = timezone.make_aware(timezone.datetime.combine(today, schedule.start_time))
    current_time = timezone.now()
    late_arrival = current_time > scheduled_start_time
    
  
    Attendance.objects.create(
        employee=employee,
        shift_type=schedule.schedule_shift_type,
        shift_location=schedule.employee.department.locations.first(),
        late_arrival=late_arrival,
    )
    
    messages.success(request, "Check-in successful!")
    return redirect('home')



# @login_required
def check_out(request):
    user = request.user

    employee = get_object_or_404(Employee, user=user)
    
    today = timezone.now().date()
    attendance = Attendance.objects.filter(employee=employee, check_in__date=today, check_out__isnull=True).first()

    if not attendance:
        messages.error(request, "No active check-in found.")
        return redirect('home')  
    
    # Update the attendance record with the check-out time
    attendance.check_out = timezone.now()
    attendance.save()
    
    messages.success(request, "Check-out successful!")
    return redirect('home')
