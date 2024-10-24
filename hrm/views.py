
from .models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.db import transaction
from datetime import timedelta
from django.db.models import Q
from datetime import datetime
from django.utils import timezone


def hrm_dashboard(request):
    return render(request, )


def hrm_quick_links(request):

    return render(request,'pages/hrm_quick_links.html' )



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
            messages.error(request,'unable to create department check form data and resubmit')
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
    if request.method == 'GET':
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
            return redirect('hrm:department_locations')
    else:
        messages.error(request, 'unable to Location for the department')
        return redirect('hrm:department_locations')

# Update an existing department location
def department_location_update(request, pk):
    location = get_object_or_404(DepartmentLocation, pk=pk)
    if request.method == 'POST':
        form = DepartmentLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'location for the department updated succesfully')
            return redirect('hrm:department_locations')
    else:
        form = DepartmentLocationForm(instance=location)
        messages.error(request, "Unable to update the department location")
        return redirect('hrm:department_locations')
    


# Delete a department location
def department_location_delete(request, pk):
    location = get_object_or_404(DepartmentLocation, pk=pk)
    if request.method == 'GET':
        location.delete()
        messages.success(request, "department location was deleted successfully")
        return redirect('hrm:department_locations')
    
    else:
        messages.error(request, "unable to delete department location ")
        return redirect('hrm:department_locations')


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
            return redirect('hrm:employees')
        else:
            # Get form errors and pass them to messages framework
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect('hrm:employees')  # Redirect to the same page with error messages

        
    else:
        messages.error(request, "unable to add employee")
        return redirect('hrm:employees')


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
    if request.method == 'GET':
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
    if request.method == 'GET':
        leave_request.delete()
        return redirect('leave_request_list')
    return render(request, 'leave_request_confirm_delete.html', {'leave_request': leave_request})


# List all staff schedules
def staff_schedule_list(request):
    schedules = StaffSchedules.objects.all()
    form = StaffScheduleForm(request.POST)
    context={
        'schedules': schedules,
        'form':form,
        }
    return render(request, 'pages/schedule_list.html', context)

# Create a new staff schedule
def staff_schedule_create(request):
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Roaster item created successfully")
            return redirect('hrm:staff_schedule')
        else:
            # Print out the form errors for debugging
            
            messages.error(request, "Unable to create Roaster")
            return redirect('hrm:staff_schedule')
    else:
        messages.error(request, "Unable to create roaster item")
        return redirect('hrm:staff_schedule')


# Update an existing staff schedule
def staff_schedule_update(request, pk):
    schedule = get_object_or_404(StaffSchedules, pk=pk)
    if request.method == 'POST':
        form = StaffScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request,"roaster item updated successfully")
            return redirect('hrm:staff_schedule')
    else:
        messages.error(request,"Unable to update roaster item")
        return redirect('hrm:staff_schedule')


# Delete a staff schedule
def staff_schedule_delete(request, pk):
    schedule = get_object_or_404(StaffSchedules, pk=pk)
    if request.method == 'GET':
        schedule.delete()
        messages.success(request,"roaster item deleted successfully")
        return redirect('hrm:staff_schedule')
    else:
        messages.success(request,"Unable to roaster item")
        return redirect('hrm:staff_schedule')


def admin_worker_attendance(request):

    # Get the current date or a date passed via GET parameter
    selected_date = request.GET.get('date', timezone.now().date())
    
    # Find schedules that intersect with the selected date (either start or end date falls on or spans the date)
    schedules = StaffSchedules.objects.filter(
        Q(schedule_start_date__lte=selected_date) & Q(schedule_end_date__gte=selected_date)
    ).select_related('employee')

    # Retrieve attendances that started on the selected day or earlier but are still active on the selected date
    attendances = Attendance.objects.filter(
        Q(check_in__date=selected_date) | (Q(check_in__date__lte=selected_date) & Q(check_out__isnull=True))
    ).select_related('employee')

    context = {
        'selected_date': selected_date,
        'schedules': schedules,
        'attendances': attendances,
    }
    return render(request, 'pages/daily_attendance.html', context)






@transaction.atomic
def checkout_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    now = timezone.now()

    # Fetch the active attendance record
    attendance = Attendance.objects.filter(employee=employee, active=True).first()
    
    if not attendance:
        messages.error(request, "No active attendance found for this employee.")
        return redirect('hrm:daily_attendance')  # Adjust redirect as needed

    # Update check-out time and mark attendance as inactive
    attendance.check_out = now
    attendance.active = False
    attendance.save()

    # Fetch the related active staff schedule
    schedule = StaffSchedules.objects.filter(
        employee=employee,
        schedule_start_date__lte=now.date(),
        schedule_end_date__gte=now.date(),
        active='True'
    ).first()

    if schedule:
        # Check if attendance is already processed (inactive)
        if not attendance.active:
            # Mark the schedule as 'Ended' regardless of the schedule end time
            schedule.active = 'Ended'
            schedule.save()
        else:
            schedule_end_datetime = datetime.combine(schedule.schedule_end_date, schedule.end_time)

            # Check if the current date is after the schedule's end date or
            # the end date is today and the end time has passed
            if (now.date() > schedule.schedule_end_date) or (now.date() == schedule.schedule_end_date and now.time() >= schedule.end_time):
                # Mark the schedule as 'Ended'
                schedule.active = 'Ended'
                schedule.save()


    # Send success message to the user
    messages.success(request, f"{employee.user.get_full_name()} has successfully checked out and their schedule has been ended.")
    return redirect('hrm:daily_attendance')  # Adjust redirect as needed


# @login_required
def check_in(request):
    user = request.user
    employee = get_object_or_404(Employee, user=user)
    
    # Get today's schedule for the employee
    today = timezone.now().date()
    schedule = StaffSchedules.objects.filter(employee=employee, active="False", schedule_start_date=today).first()

    if not schedule:
        messages.error(request, "No schedule found for today.")
        return redirect('signin') 
    
    # Check if employee already checked in today
    if Attendance.objects.filter(employee=employee, check_in__date=today, check_out__isnull=True).exists():
        messages.warning(request, "You have already checked in.")
        return redirect('signin')  # redirect to a relevant page
    
    # Check for lateness based on schedule
    scheduled_start_time = timezone.make_aware(timezone.datetime.combine(today, schedule.start_time))
    current_time = timezone.now()
    late_arrival = current_time > scheduled_start_time

    # Check if user is trying to sign in before their time
    if current_time < scheduled_start_time:
        messages.error(request, "It is not yet time for you to sign in!")
        return redirect('signin')
    
    # Retrieve the employee's department location (linked via DepartmentLocation)
    department_location = employee.department_location

    Attendance.objects.create(
        employee=employee,
        shift_type=schedule.schedule_shift_type,
        shift_location=department_location,  # Use employee's department location directly
        late_arrival=late_arrival,
        active=True,

    )

    # Update schedule status
    schedule.active = "True"
    schedule.save()
    messages.success(request, "Attendance Signed successfully!")
    return redirect('signin')



# def check_out(request):
#     now = timezone.now()  # Current date and time
#     today = now.date()
#     user = request.user
#     employee = get_object_or_404(Employee, user=user)

#     # Fetch the schedule that spans today
#     schedule = StaffSchedules.objects.filter(
#         employee=employee,
#         schedule_start_date__lte=today,  # Schedule that started before or on today
#         schedule_end_date__gte=today      # Schedule that ends on or after today
#     ).first()

#     # Fetch active attendance record where check-out is not yet recorded
#     attendance = Attendance.objects.filter(employee=employee, check_out__isnull=True).first()

#     if not attendance:
#         messages.error(request, "No active check-in found.")
#         return redirect('signin')

#     # Update attendance with check-out time and deactivate it
#     attendance.check_out = now
#     attendance.active = False
#     attendance.save()

#     if schedule:
#         schedule_end_datetime = datetime.combine(schedule.schedule_end_date, schedule.end_time)

#         # If attendance is inactive (False) but the schedule is still marked as active (True)
#         if not attendance.active and schedule.active == 'True':
#             # Mark the schedule as 'Ended' to ensure consistency
#             schedule.active = 'Ended'
#             schedule.save()
#         # If the schedule's end datetime has passed or is happening right now
#         elif now >= schedule_end_datetime:
#             # Mark the schedule as 'Ended'
#             schedule.active = 'Ended'
#             schedule.save()

#     # Log out the user after successful check-out
#     logout(request)
#     messages.success(request, "You have successfully checked out.")
#     return redirect('core:index')




def check_out(request):
    import datetime
    now = timezone.now()  # Timezone-aware current date and time
    today = now.date()    # Current date (timezone-naive, but safe for date comparisons)
    user = request.user
    employee = get_object_or_404(Employee, user=user)

    # Fetch the schedule that spans today
    schedule = StaffSchedules.objects.filter(
        employee=employee,
        schedule_start_date__lte=today,  # Schedule that started before or on today
        schedule_end_date__gte=today     # Schedule that ends on or after today
    ).first()

    # Fetch active attendance record where check-out is not yet recorded
    attendance = Attendance.objects.filter(employee=employee, check_out__isnull=True).first()

    if not attendance:
        messages.error(request, "No active check-in found.")
        return redirect('signin')

    # Update attendance with check-out time and deactivate it
    attendance.check_out = now
    attendance.active = False
    attendance.save()

    if schedule:
        # Combine the schedule end date and time (this is a naive datetime)
        schedule_end_datetime_naive = datetime.combine(schedule.schedule_end_date, schedule.end_time)

        # Make the schedule_end_datetime timezone-aware to match with 'now'
        schedule_end_datetime = timezone.make_aware(schedule_end_datetime_naive, timezone.get_current_timezone())

        # Check if the employee checks out BEFORE the schedule's end date and time
        if now < schedule_end_datetime:
            # Mark the schedule as 'Ended' since the employee checked out early
            schedule.active = 'Ended'
            schedule.save()
            messages.warning(request, "You checked out before your scheduled end time.")

        # Check if the current time is now or past the schedule's end datetime
        elif now >= schedule_end_datetime:
            # Mark the schedule as 'Ended'
            schedule.active = 'Ended'
            schedule.save()

        # Additionally, check if today's date is past the schedule's end date
        elif today > schedule.schedule_end_date:
            # If the current date is past the schedule end date, mark it as 'Ended'
            schedule.active = 'Ended'
            schedule.save()

        # Check if attendance is inactive and schedule is still marked active as 'True' (since it's stored as a string)
        elif not attendance.active and schedule.active == 'True':
            # Mark the schedule as 'Ended' for consistency if check-out is done
            schedule.active = 'Ended'
            schedule.save()

    # Log out the user after successful check-out
    logout(request)
    messages.success(request, "You have successfully checked out.")
    return redirect('core:index')
