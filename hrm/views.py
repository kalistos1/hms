
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
        messages.error(request,'unable to  delete department')
        return redirect('hrm:departments')
  


# Update an existing department
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('hrm:departments')
    else:
       return redirect('hrm:departments')


# Delete a department
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
        messages.success(request, 'Department deleted successfully')
        return redirect('hrm:departments')
    messages.error(request, 'Unable to delete selected department')
    return redirect('hrm:departments')



# List all department locations
def department_location_list(request):
    locations = DepartmentLocation.objects.all()
    form  = DepartmentLocationForm()
    context = {
        'locations': locations,
        'form':form,
        }
    return render(request, 'pages/department_location.html', context)


# Create a new department location
def department_location_create(request):
    if request.method == 'POST':
        form = DepartmentLocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'location for the department added succesfully')
            return redirect('hrm:department_location')
    else:
        messages.error(request, 'unable to Location for the department')
        return redirect('hrm:department_location')

# Update an existing department location
def department_location_update(request, pk):
    location = get_object_or_404(DepartmentLocation, pk=pk)
    if request.method == 'POST':
        form = DepartmentLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'location for the department updated succesfully')
            return redirect('hrm:department_location')
    else:
        form = DepartmentLocationForm(instance=location)
        messages.error(request, "Unable to update the department location")
        return redirect('hrm:department_location')
    


# Delete a department location
def department_location_delete(request, pk):
    location = get_object_or_404(DepartmentLocation, pk=pk)
    if request.method == 'POST':
        location.delete()
        messages.success(request, "department location was deleted successfully")
        return redirect('hrm:department_location')
    
    else:
        messages.error(request, "unable to delete department location ")
        return redirect('hrm:department_location')


# List all employees
def employee_list(request):
    employees = Employee.objects.all()
    form = EmployeeForm()
    context = {
        'employees': employees,
        'form':form,
        }
    
    return render(request, 'pages/employee_list.html', context)


# Create a new employee
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Employee Added Successfully")
            return redirect('hrm:employee_list')
    else:
        messages.error(request, "unable to add employee")
        return redirect('hrm:employee_list')


# Update an existing employee
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request,'employee information updated successfully')
            return redirect('hrm:employee_list')
    else:
        messages.success(request,'Unable to Update employee Information')
        return redirect('hrm:employee_list')


# Delete an employee
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        messages.success('Employee deleted succcessfully')
        return redirect('hrm:employee_list')
    else:
        messages.error('Unable to delete Employee')
        return redirect('hrm:employee_list')



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
