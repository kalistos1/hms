from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib import messages
from dashboard . models import *
from hrm .models import *
from accounts.models import *
from bookings.models import *
import string
from .forms import *
from django.db.models import Count
from accounts.forms import *
from formtools.wizard.views import SessionWizardView
from datetime import timedelta
from django.db.models import Sum, Case, When, F, IntegerField, Q, Count
from django.contrib.auth import login
from bookings.forms import (
    BasicUserInfoForm, ProfileInfoForm, 
    BookingChoiceForm, RoomBookingForm, RoomReservationForm, 
    RoomServiceForm, PaymentForm,AdditionalChargeForm, PaymentCheckoutForm,UpdateCheckOutDateForm,HotelForm
)
from django.http import JsonResponse,HttpResponse
import datetime
today = datetime.date.today()
from datetime import datetime
from pos.models import *
from inventory.forms import  WarehouseForm
from inventory.models import *
from pos.forms import updateReceivedItemForm
from django.utils.timezone import make_aware,is_aware
from accounting . models import *
from inventory.forms import InventoryMovementForm,  InventoryMovementForm2
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from hrm.models import Employee, Attendance, StaffSchedules
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from core.decorators import required_roles


def admin_dashboard(request):
    # template = "admin_user/dashboard.html"
    return redirect( 'dashboard:account_dashboard' )


@required_roles('is_supervisor', 'is_pos_officer')
def hotel_setup(request):

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'setup was successfully!')
            return redirect('dashboard:hotel_info')  
        else:
            print(form.errors)
            messages.error(request, 'could not setup hotel, Error settingup hotel.')
            return redirect('dashboard:hotel_info')  
            
    else:
        messages.error(request, 'Something Went Wrong, Try Again.')
        return redirect('dashboard:hotel_info') 


def admin_hotel_info(request):
    hotels =  Hotel.objects.all()
    form = HotelForm()   
    context = {
        'hotels': hotels,
        'form':form,
        }
    return render(request, 'admin_user/hotel_info.html',context)


def admin_delete_hotel(request, pk):    
    hotel = get_object_or_404(Hotel, pk=pk)
    if request.method == 'GET':
        hotel.delete()
        messages.success(request, 'hotel deleted successfully!')
        return redirect('dashboard:hotel_info')
    
    return redirect('dashboard:hotel_info')



#warehouse setup
def warehouse_setup(request):

    if request.method == 'POST':
        form = WarehouseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'setup was successfully!')
            return redirect('dashboard:warehouse_info')  
        else:
            messages.error(request, 'could not setup hotel, Error settingup hotel.')
            return redirect('dashboard:warehouse_info')  
            
    else:
        return redirect('dashboard:warehouse_info') 


def warehouse_info(request):
    # inventory data

    total_quantity = Item.objects.aggregate(total=Sum('stock_quantity'))['total']
    quantity_by_stock_type = Item.objects.values('stock_type').annotate(total_quantity=Sum('stock_quantity'))
    stock_by_category = Item.objects.values('stock_type').annotate(
        total_quantity=Sum('stock_quantity'),
        total_value=Sum('stock_quantity') * Sum('unit_price')
    )
    movements_by_type = InventoryMovement.objects.values('movement_type').annotate(total_quantity=Sum('quantity'))

    warehouse =  Warehouse.objects.first()
    total_stock = WarehouseStock.objects.filter(warehouse=warehouse).aggregate(Sum('quantity'))['quantity__sum']

    if total_stock is None:
        total_stock = 0

    form = WarehouseForm() 
    inventory_form = InventoryMovementForm(exclude_types=True)  
    inventory_form2 = InventoryMovementForm2(exclude_types=True) 
    context = {
        'total_quantity': total_quantity,
        'quantity_by_stock_type': quantity_by_stock_type,
        'stock_by_category': stock_by_category,
        'movements_by_type': movements_by_type,
        'total_stock':total_stock,

        # others
        'warehouse': warehouse,
        'form':form,
        'inventory_form':inventory_form,
        'inventory_form2':inventory_form2,

        }

    return render(request, 'admin_user/warehouse_info.html',context)



def warehouse_stock(request):
    # Get the first warehouse as a default example (you may want to adjust this logic)
    warehouse = Warehouse.objects.first()

    try:   
        stocks = WarehouseStock.objects.filter(warehouse=warehouse).select_related('item__category')
        context = {
            'stocks': stocks,
        }
    except WarehouseStock.DoesNotExist:
        context = {
            'error': 'No stock found in the warehouse.'
        }
    form = InventoryMovementForm(exclude_types=True)
    form2 = InventoryMovementForm2(exclude_types=True)
    context.update({
        'form': form,
        'form2':form2,
    })

    return render(request, 'supervisor/move_item.html', context)


def warehouse_delete(request, pk):    
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'GET':
        warehouse.delete()
        messages.success(request, 'warehouse deleted successfully!')
        return redirect('dashboard:warehouse_info')
    
    return redirect('dashboard:warehouse_info')


# Amenities
def admin_create_room_amenity(request):
    if request.method == 'POST':
        warehouse = Warehouse.objects.first()
        form = RoomAmenityForm(request.POST, request.FILES)
        if form.is_valid():
            facility = form.save(commit=False)
            facility.warehouse = warehouse
            facility.save()
            messages.success(request, 'Room Amenity created successfully!')
            return redirect('dashboard:admin_list_room_amenities')  
        else:
            messages.error(request, 'Error creating Room Amenity. Please correct the errors below.')
            return redirect('dashboard:admin_list_room_amenities')  
            
    else:
        messages.error(request, 'Something Went Wrong. Try Again.')
        return redirect('dashboard:admin_list_room_amenities') 
    
    

def admin_list_room_amenities(request):
    amenities =  RoomInventory.objects.all()
    form = RoomAmenityForm()   
    context = {
        'amenities': amenities,
        'form':form,
        }
    return render(request, 'admin_user/room_amenities_list.html',context)


def admin_update_room_amenity(request, pk):
    amenity = get_object_or_404( RoomInventory, pk=pk)
    if request.method == 'POST':
        form = RoomAmenityForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Amenity updated successfully!')
            return redirect('list_room_amenities')
        else:
            messages.error(request, 'Error updating Room Amenity. Please correct the errors below.')
    else:
        form = RoomAmenityForm(instance=amenity)

    return render(request, 'room_amenities/update.html', {'form': form})


def admin_delete_room_amenity(request, pk):    
    amenity = get_object_or_404( RoomInventory, pk=pk)
    if request.method == 'GET':
        amenity.delete()
        messages.success(request, 'Room Amenity deleted successfully!')
        return redirect('dashboard:admin_list_room_amenities')
    
    return redirect('dashboard:admin_list_room_amenities')


#rooms
def admin_create_room(request):
    hotel = Hotel.objects.filter(status='Live').first()
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            
            messages.success(request, 'Room created successfully!')
            return redirect('dashboard:admin_list_room')  
        else:
            messages.error(request, 'Error creating Room . Please correct the errors below.')
            return redirect('dashboard:admin_list_room')  
            
    else:
        messages.error(request, 'Something Went Wrong. Try Again.')
        return redirect('dashboard:admin_list_room') 
    


def admin_list_room(request):
    
    rooms = Room.objects.select_related('room_type').all()
    form = RoomForm()
    
    context = {
        'rooms':rooms,
        'form':form,
        }
    return render(request, 'admin_user/room_list.html',context)



def admin_update_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomAmenityForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Amenity updated successfully!')
            return redirect('list_room_amenities')
        else:
            messages.error(request, 'Error updating Room Amenity. Please correct the errors below.')
    else:
        form = RoomAmenityForm(instance=room)

    return render(request, 'room_amenities/update.html', {'form': form})



def admin_delete_room(request, pk):    
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'GET':
        room.delete()
        messages.success(request, 'Room Amenity deleted successfully!')
        return redirect('dashboard:admin_list_room')
    
    return redirect('dashboard:admin_list_room')


#room type
def admin_create_room_type(request):
    hotel = Hotel.objects.filter(status='Live').first()
    if request.method == 'POST':
        form =  RoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.hotel = hotel
            room_type.save()
            
            messages.success(request, 'Room Type created successfully!')
            return redirect('dashboard:admin_list_room_types')  
        else:
            messages.error(request, 'Error creating Room Type. Please correct the errors below.')
            return redirect('dashboard:admin_list_room_types')  
            
    else:
        messages.error(request, 'Something Went Wrong. Try Again.')
        return redirect('dashboard:admin_list_room_types') 
    


def admin_list_room_type(request):
    room_types = RoomType.objects.annotate(num_rooms=Count('room'))
    form = RoomTypeForm()
    
    context = {
        'room_types': room_types,
        'form':form,
        }
    return render(request, 'admin_user/room_type_list.html',context)



def admin_update_room_type(request, pk):
    amenity = get_object_or_404(RoomAmenity, pk=pk)
    if request.method == 'POST':
        form = RoomAmenityForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Amenity updated successfully!')
            return redirect('dashboard:admin_list_room_types')
        else:
            messages.error(request, 'Error updating Room Amenity. Please correct the errors below.')
    else:
        form = RoomAmenityForm(instance=amenity)

    return render(request, 'room_amenities/update.html', {'form': form})



def admin_delete_room_type(request, pk):   
    room_type = get_object_or_404(RoomType, pk=pk)
    if request.method == 'GET':
        room_type.delete()
        messages.success(request, 'Room Amenity deleted successfully!')
        return redirect('dashboard:admin_list_room_types')
    
    return redirect('dashboard:admin_list_room_types')


#coupons
def admin_create_coupon(request):
    hotel = Hotel.objects.filter(status='Live').first()
    if request.method == 'POST':
        form =  CreateCouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Type created successfully!')
            return redirect('dashboard:admin_list_coupon')  
        else:
            messages.error(request, 'Error creating Room Type. Please correct the errors below.')
            return redirect('dashboard:admin_list_coupon')  
            
    else:
        messages.error(request, 'Something Went Wrong. Try Again.')
        return redirect('dashboard:admin_list_coupon') 
    


def admin_list_coupon(request):
    coupons = Coupon.objects.all()
    form = CreateCouponForm()
    
    context = {
        'coupons': coupons,
        'form':form,
        }
    return render(request, 'admin_user/coupon_list.html',context)



def admin_update_coupon(request, pk):
    amenity = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CreateCouponForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Amenity updated successfully!')
            return redirect('dashboard:admin_list_coupon')
        else:
            messages.error(request, 'Error updating Room Amenity. Please correct the errors below.')
    else:
        form = CreateCouponForm(instance=amenity)

    return render(request, {'form': form})



def admin_delete_coupon(request, pk):
    
    room_type = get_object_or_404(Coupon, pk=pk)
    if request.method == 'GET':
        room_type.delete()
        messages.success(request, 'Room Amenity deleted successfully!')
        return redirect('dashboard:admin_list_coupon')
    
    return redirect('dashboard:admin_list_coupon')


# Privilaged Users
# =================

def admin_users_list(request):
    template ="admin_user/admin_user.html"
  
    admin_form = AddAdminForm()
    supervisor_form = AddSupervisorForm()
    frontdesk_form = AddFrontdeskForm()
    pos_officer_form = AddPosOfficerForm()
    account_officer_form = AddAccountOfficerForm()
    worker_form = AddWorkerForm()
    
    privilage_users = User.objects.filter(
                            is_admin=True
                        ) | User.objects.filter(
                            is_supervisor=True
                        ) | User.objects.filter(
                            is_account_officer=True
                        ) | User.objects.filter(
                            is_worker=True
                        ) | User.objects.filter(
                            is_frontdesk_officer=True
                        ) | User.objects.filter(
                            is_pos_officer=True
                )
    
    
    context = {
        'privilage_users':privilage_users,
        'admin_form':admin_form,
        'supervisor_form':supervisor_form,
        'frontdesk_form':frontdesk_form,
        'pos_officer_form':pos_officer_form,  
        'account_officer_form':account_officer_form,
        'worker_form':worker_form,
    }
    return render(request, template, context)



def add_admin_privilaged_user(request):
    
    admin_form = AddAdminForm()
    supervisor_form = AddSupervisorForm()
    frontdesk_form = AddFrontdeskForm()
    pos_officer_form = AddPosOfficerForm()
    account_officer_form = AddAccountOfficerForm()
    worker_form = AddWorkerForm()

    if request.method == "POST":
        # Determine which form was submitted based on form data
        if 'admin_submit' in request.POST:
            admin_form = AddAdminForm(request.POST)
            if admin_form.is_valid():
                user = admin_form.save(commit=False)
                user.set_password(admin_form.cleaned_data['password'])
                user.save()
                messages.success(request, f"Admin user {user.username} was created successfully")
                return redirect('dashboard:admin_users_list')
        
        elif 'supervisor_submit' in request.POST:
            supervisor_form = AddSupervisorForm(request.POST)
            if supervisor_form.is_valid():
                user = supervisor_form.save(commit=False)
                user.set_password(supervisor_form.cleaned_data['password'])
                user.save()
                messages.success(request, f"Supervisor {user.username} was created successfully")
                return redirect('dashboard:admin_users_list')

        elif 'frontdesk_submit' in request.POST:
            frontdesk_form = AddFrontdeskForm(request.POST)
            if frontdesk_form.is_valid():
                user = frontdesk_form.save(commit=False)
                user.set_password(frontdesk_form.cleaned_data['password'])
                user.save()
                messages.success(request, f"Frontdesk Officer {user.username} was created successfully")
                return redirect('dashboard:admin_users_list')

        elif 'pos_officer_submit' in request.POST:
            pos_officer_form = AddPosOfficerForm(request.POST)
            if pos_officer_form.is_valid():
                user = pos_officer_form.save(commit=False)
                user.set_password(pos_officer_form.cleaned_data['password'])
                user.save()
                messages.success(request, f"POS Officer {user.username} was created successfully")
                return redirect('dashboard:admin_users_list')

        elif 'account_officer_submit' in request.POST:
            account_officer_form = AddAccountOfficerForm(request.POST)
            if account_officer_form.is_valid():
                user = account_officer_form.save(commit=False)
                user.set_password(account_officer_form.cleaned_data['password'])
                user.save()
                messages.success(request, f"Account Officer {user.username} was created successfully")
                return redirect('dashboard:admin_users_list')
            
        elif 'worker_submit' in request.POST:
            worker_form = AddWorkerForm(request.POST)
            if worker_form.is_valid():
                user = worker_form.save(commit=False)
                user.set_password(worker_form.cleaned_data['password'])
                user.save()
                messages.success(request, f"Account Officer {user.username} was created successfully")
                return redirect('dashboard:admin_users_list')

    messages.error(request, f"Something Went Wrong, Account Officer was not created!")
    return redirect('dashboard:admin_users_list')


def admin_delete_privilaged_user(request, pk):
    
    room_type = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        room_type.delete()
        messages.success(request, 'user deleted successfully!')
        return redirect('dashboard:admin_users_list')
    
    return redirect('dashboard:admin_users_list')


#booking list
def admin_booking_list(request):
    template = "admin_user/admin_bookinglist.html"
  
    
    bookin_list = Booking.objects.all()
    room_service_form =  RoomServiceForm()
    additional_charge_form =  AdditionalChargeForm()
    context = {
        'bookings':bookin_list,
        'room_service_form': room_service_form,
        "additional_charge_form":additional_charge_form,
    }
    
    return render (request,template, context)
    

#room status 
def admin_room_status(request):
    template = "admin_user/admin_roomstatus.html"

        
    room_status = Room.objects.all()
    context = {
        'room_status':room_status
    }
    
    return render (request,template, context)



#admin views end here
# ===========================================================================================================
# ===========================================================================================================


# supervisor view starts here 
# ===========================================================================================================
# ==========================================================================================================




def supervisor_dashboard(request):
    template = "supervisor/dashboard.html"
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Get today's and yesterday's bookings
    todays_bookings = Booking.objects.filter(date__date=today).order_by('-date')
    yesterdays_bookings = Booking.objects.filter(date__date=yesterday).order_by('-date')

    # Calculate total amount for today's bookings in Payment and PaymentCompletion models
    todays_payment_total = Payment.objects.filter(
        booking__in=todays_bookings
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    todays_completion_total = PaymentCompletion.objects.filter(
        payment__booking__in=todays_bookings
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    # Calculate total amount for yesterday's bookings in Payment and PaymentCompletion models
    yesterdays_payment_total = Payment.objects.filter(
        booking__in=yesterdays_bookings
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    yesterdays_completion_total = PaymentCompletion.objects.filter(
        payment__booking__in=yesterdays_bookings
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

    todays_total_payment = todays_payment_total + todays_completion_total 
    yesterdays_total_payment =  yesterdays_payment_total + yesterdays_completion_total 

    context = {
        'todays_bookings': todays_bookings,
        'yesterdays_bookings': yesterdays_bookings,
        'todays_total_payment': todays_total_payment,
        'yesterdays_total_payment':yesterdays_total_payment,
        
    }

    return render(request, template, context)

def supervisor_transaction_list (request):
    template = "supervisor/transactions.html"


    # Calculate date ranges for today and yesterday
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)

    # Fetch orders by department for yesterday and include items
    orders_yesterday = (
        Order.objects
        .filter(created_at__date=yesterday)
        .select_related('staff__department_location')  # Access department location
        .prefetch_related('items', 'pospayment_set')  # Prefetch items and payments for the orders
        .annotate(total_amount_paid=Sum('pospayment__amount_paid'))  # Calculate total amount paid for each order
    )

    # Fetch orders by department for today and include items
    orders_today = (
        Order.objects
        .filter(created_at__date=today)
        .select_related('staff__department_location')
        .prefetch_related('items', 'pospayment_set')
        .annotate(total_amount_paid=Sum('pospayment__amount_paid'))
    )

    context = {
        'orders_yesterday': orders_yesterday,
        'orders_today': orders_today,
    }

    return render(request, template,context)



def supervisor_view_bookings (request):
    template = "supervisor/supervisor_bookinglist.html"
    today =timezone.now().date()
    bookings = Booking.objects.filter(date=today).order_by('-date') 
    context = {
        'bookings':bookings,
    }
    return render(request, template, context)


def supervisor_view_roomstatus (request):
    template="supervisor/supervisor_room_status.html"
    if request.user.is_supervisor:

        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
        
        room_status = Room.objects.all()
        context = {
            'room_status':room_status,
             'active_attendance': active_attendance,
        }
        
        return render (request,template, context)
    else:
        return redirect('core:index')
    

#room checkout
def supervisor_checkout_list (request):
    template="supervisor/supervisor_room_checkout.html"

    if request.user.is_supervisor:
        booking_list = Booking.objects.filter(
                check_out_date__lte=timezone.now().date(),
                is_active=True,
                checked_in=True
            )
        context ={
            'bookings': booking_list,
        }
        return render(request,template,context)
    else:
        return redirect('core:index')


#supervisor views ends here 
# ==========================================================================================================
# ==========================================================================================================




# Accountant views starts here 
# ===========================================================================================================
# ==========================================================================================================




# def account_dashboard(request):
#     template = "account_officer/dashboard.html"    
    
#     today = timezone.now().date()

#     # 1. Get all bookings done today
#     todays_bookings = Booking.objects.filter(date_created__date=today)

#     # 2. Get all payments made today
#     todays_payments = Payment.objects.filter(date_created__date=today)

#     # 3. Get the last ended session of the front desk user
#     last_ended_session = Attendance.objects.filter(
#         employee__employee_profile__role='front_desk',
#         check_out__isnull=False
#     ).order_by('-check_out').first()

#     last_session_bookings = last_session_payments = None
#     if last_ended_session:
#         last_session_bookings = Booking.objects.filter(
#             date_created__range=(last_ended_session.check_in, last_ended_session.check_out)
#         )
#         last_session_payments = Payment.objects.filter(
#             date_created__range=(last_ended_session.check_in, last_ended_session.check_out)
#         )

#     # 4. Get the active session of the front desk user
#     current_active_session = Attendance.objects.filter(
#         employee__employee_profile__role='front_desk',
#         active=True
#     ).first()

#     active_session_bookings = active_session_payments = None
#     if current_active_session:
#         active_session_bookings = Booking.objects.filter(
#             date_created__range=(current_active_session.check_in, timezone.now())
#         )
#         active_session_payments = Payment.objects.filter(
#             date_created__range=(current_active_session.check_in, timezone.now())
#         )

#     context = {
#         'todays_bookings': todays_bookings,
#         'todays_payments': todays_payments,
#         'last_session_bookings': last_session_bookings,
#         'last_session_payments': last_session_payments,
#         'active_session_bookings': active_session_bookings,
#         'active_session_payments': active_session_payments,
#     }


#     return render (request,template, context)
@required_roles('is_admin','is_account_officer')
def account_dashboard(request):
    template = "account_officer/dashboard.html"    
    today = timezone.now().date()

    # Count customers who are not staff members
    customers = Employee.objects.filter(
                role__in=['customer']  # Assuming 'customer' is the role in your Employee model
            ).count()

    # Count staff members with any of the specified roles
    staff_count = Employee.objects.filter(
        Q(role__in=['admin', 'supervisor', 'account_officer', 'front_desk_officer', 'pos_officer', 'worker'])
    ).count()

    # 1. Get all bookings done today
    todays_bookings = Booking.objects.filter(date_created__date=today)

    # Filter PaymentRecords for the current month and statuses 'advance' or 'completed'
    first_day_of_month = today.replace(day=1)
    monthly_income = Payment.objects.filter(
        date__date__gte=first_day_of_month,  # Payments in the current month
        status__in=['advance', 'completed']  # Payments with status 'advance' or 'completed'
    ).aggregate(monthly_income=Sum('amount'))['monthly_income'] or 0

    # 2. Get all payments made today
    todays_booking_payments = Payment.objects.filter(
        date__date=today, 
        status__in=['advance', 'completed']
    )
    todays_booking_payment_completions = PaymentCompletion.objects.filter(
        completion_date__date=today
    )
    todays_payment_sum = todays_booking_payments.aggregate(total=Sum('amount'))['total'] or 0.00
    todays_payment_completion_sum = todays_booking_payment_completions.aggregate(total=Sum('amount'))['total'] or 0.00
    todays_total_booking_payments = Decimal(todays_payment_sum) + Decimal(todays_payment_completion_sum)

    # 3. Sum of all POS orders done today
    total_pos_orders_today = Order.objects.filter(created_at__date=today).aggregate(total=Sum(F('total_amount')))['total'] or 0

    # 4. Sum of all POS payments made today
    total_pos_orders_payments_today = PosPayment.objects.filter(payment_date__date=today).aggregate(total=Sum(F('amount_paid')))['total'] or 0

    # Initialize data structure to hold totals for each department
    department_data = []

    # Get all departments
    departments = Department.objects.all()

    for department in departments:
        department_locations = department.locations.all()

        # Get the last ended session for POS staff in this department's locations
        last_pos_ended_session = Attendance.objects.filter(
            employee__role='pos_staff',
            check_out__isnull=False,
            shift_location__in=department_locations
        ).order_by('-check_out').first()

        total_pos_orders_recent_session = 0
        total_pos_payments_recent_session = 0

        if last_pos_ended_session:
            session_start = last_pos_ended_session.check_in
            session_end = last_pos_ended_session.check_out

            # Sum orders for the recent session in this department
            total_pos_orders_recent_session = Order.objects.filter(
                staff=last_pos_ended_session.employee,  # Use Employee instance directly
                staff__department_location__in=department_locations,
                created_at__range=[session_start, session_end]
            ).aggregate(total=Sum(F('total_amount')))['total'] or 0


           # Sum payments for the recent session in this department
            total_pos_payments_recent_session = PosPayment.objects.filter(
                order__staff=last_pos_ended_session.employee,  # Use Employee instance directly
                order__staff__department_location__in=department_locations,
                payment_date__range=[session_start, session_end]
            ).aggregate(total=Sum(F('amount_paid')))['total'] or 0


        # Get the active POS session for this department
        pos_active_session = Attendance.objects.filter(
            employee__role='pos_staff',
            check_out__isnull=True,
            shift_location__in=department_locations
        ).order_by('-check_in').first()

        total_pos_orders_active_session = 0
        total_pos_payments_active_session = 0

        if pos_active_session:
            session_start = pos_active_session.check_in

            # Sum orders for the active session in this department
            total_pos_orders_active_session = Order.objects.filter(
                staff=pos_active_session.employee.user,
                staff__employee_profile__department_location__in=department_locations,
                created_at__gte=session_start
            ).aggregate(total=Sum(F('total_amount')))['total'] or 0

            # Sum payments for the active session in this department
            total_pos_payments_active_session = PosPayment.objects.filter(
                order__staff=pos_active_session.employee.user,
                order__staff__employee_profile__department_location__in=department_locations,
                payment_date__gte=session_start
            ).aggregate(total=Sum(F('amount_paid')))['total'] or 0

        # Append data for this department
        department_data.append({
            'department_name': department.name,
            'total_orders_recent_session': total_pos_orders_recent_session,
            'total_payments_recent_session': total_pos_payments_recent_session,
            'total_orders_active_session': total_pos_orders_active_session,
            'total_payments_active_session': total_pos_payments_active_session,
        })

    # Get the last ended session for front desk user
    last_ended_session = Attendance.objects.filter(
        employee__role='front_desk',
        check_out__isnull=False
    ).order_by('-check_out').first()

    last_session_bookings = last_session_payments = last_session_payment_completions = None
    if last_ended_session:
        last_session_bookings = Booking.objects.filter(
            date_created__range=(last_ended_session.check_in, last_ended_session.check_out)
        )
        last_session_payments = Payment.objects.filter(
            date__range=(last_ended_session.check_in, last_ended_session.check_out),
            status__in=['advance', 'completed']
        )
        last_session_payment_completions = PaymentCompletion.objects.filter(
            completion_date__range=(last_ended_session.check_in, last_ended_session.check_out)
        )

    # Get the active session of the front desk user
    current_active_session = Attendance.objects.filter(
        employee__role='front_desk',
        active=True
    ).first()

    active_session_bookings = active_session_payments = active_session_payment_completions = None
    if current_active_session:
        active_session_bookings = Booking.objects.filter(
            date_created__range=(current_active_session.check_in, timezone.now())
        )
        active_session_payments = Payment.objects.filter(
            date__range=(current_active_session.check_in, timezone.now()),
            status__in=['advance', 'completed']
        )
        active_session_payment_completions = PaymentCompletion.objects.filter(
            completion_date__range=(current_active_session.check_in, timezone.now())
        )

    # Summarize last session and active session total payments
    last_session_payment_sum = last_session_payments.aggregate(total=Sum('amount'))['total'] if last_session_payments else 0.00
    last_session_payment_completion_sum = last_session_payment_completions.aggregate(total=Sum('amount'))['total'] if last_session_payment_completions else 0.00
    last_session_total_payments = last_session_payment_sum + last_session_payment_completion_sum

    active_session_payment_sum = active_session_payments.aggregate(total=Sum('amount'))['total'] if active_session_payments else 0.00
    active_session_payment_completion_sum = active_session_payment_completions.aggregate(total=Sum('amount'))['total'] if active_session_payment_completions else 0.00
    active_session_total_payments = Decimal(active_session_payment_sum) + Decimal(active_session_payment_completion_sum)


    context = {
        'todays_bookings': todays_bookings,
        'todays_bookings_payments': todays_total_booking_payments,
        'last_session_bookings': last_session_bookings,
        'last_session_payments': last_session_payments,
        'active_session_bookings': active_session_bookings,
        'active_session_payments': active_session_payments,
        'last_session_total_payments': last_session_total_payments,
        'active_session_total_payments': active_session_total_payments,
        'total_orders_today': total_pos_orders_today,
        'total_pos_payments_today': total_pos_orders_payments_today,
        'department_data': department_data,
        'customers': customers,
        'staff_count': staff_count,
        'monthly_income': monthly_income
    }
    return render(request, template, context)




#Accountant views ends here 
# ==========================================================================================================
# ==========================================================================================================



#Frontdesk  views starts here 
# ==========================================================================================================
# ==========================================================================================================

def frontdesk_dashboard(request):
    template = "front_desk/dashboard.html"
    
    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()

        if active_attendance:
            check_in_time = active_attendance.check_in
            check_out_time = active_attendance.check_out or timezone.now()  # If checked out, use check-out time; otherwise, use current time

            # Ensure to use the correct date field from the Booking model
            todays_bookings = Booking.objects.filter(
                # date_created__date=today, 
                date_created__range=(check_in_time, check_out_time)
            )

            # Payments made for these bookings within the same time range
            todays_payments = Payment.objects.filter(
                # booking__in=todays_bookings,
                date__range=(check_in_time, check_out_time)
            )

            # Sum of payments by status
            advance_payments_total = todays_payments.filter(status='advance').aggregate(total=Sum('amount'))['total'] or 0
            completed_payments_total = todays_payments.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0
            payment_completion_total = PaymentCompletion.objects.filter(
                payment__in=todays_payments
            ).aggregate(total=Sum('amount'))['total'] or 0

            # Calculate total money realized during the active session
            todays_total_money = advance_payments_total + completed_payments_total + payment_completion_total

            
            customers = User.objects.filter(
                is_admin=False,
                is_supervisor=False,
                is_account_officer=False,
                is_frontdesk_officer=False,
                is_pos_officer=False,
                 is_worker=False,
                date_joined__date=today,
                date_joined__range=(check_in_time, check_out_time)

            )

            context = {
                'all_bookings': todays_bookings.count(),
                'todays_bookings': todays_bookings,
                'total_todays_booking': todays_bookings.count(),
                'todays_total_money': todays_total_money,
                'customers': customers.count(),
                'active_attendance': active_attendance,
            }
            
            return render(request, template, context)
        
        else:
            # Handle case where there is no active attendance for the employee
            return render(request, template, {'error': 'No active attendance found for the session.'})

#room status 
def frontdesk_room_status(request):
    template = "front_desk/roomstatus.html"
    
    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
        
        room_status = Room.objects.all()
        context = {
            'room_status':room_status,
             'active_attendance': active_attendance,
        }
        
        return render (request,template, context)
    else:
        return redirect('core:index')


# bookings

def frontdesk_booking_list(request):
    template = "front_desk/bookinglist.html"
    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get active attendance and schedule
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
        active_schedule = StaffSchedules.objects.filter(employee=employee, active=True).first()
       
        if active_attendance and active_schedule:

                        # Construct the start and end datetime of the active schedule
            schedule_start = timezone.make_aware(
                datetime.combine(active_schedule.schedule_start_date, active_schedule.start_time)
            )
            schedule_end = timezone.make_aware(
                datetime.combine(active_schedule.schedule_end_date, active_schedule.end_time)
            )
            # Validate schedule start and end times
            start_time = active_schedule.start_time
            end_time = active_schedule.end_time

            if start_time is None or end_time is None:
                return render(request, template, {'error': 'Schedule times are missing.'})

                
            # Fetch all bookings
            booking_list = Booking.objects.filter(date__range=(schedule_start, schedule_end)).order_by('-date') 

            # Add payment info for each booking
            bookings_with_payment_info = []
            for booking in booking_list:
                # Fetch payments related to the booking
                payments = Payment.objects.filter(booking=booking)

                # Sum the amounts based on payment status
                total_payment_amount = 0.0
                payment_status = 'No Payments'

                # Check for completed or advance payments
                if payments.exists():
                    completed_payments = payments.filter(status='completed')
                    advance_payments = payments.filter(status='advance')

                    if completed_payments.exists():
                        payment_status = 'completed'
                        total_payment_amount = completed_payments.aggregate(Sum('amount'))['amount__sum'] or 0.0

                        # Sum up the payment completion amounts if applicable
                        for payment in completed_payments:
                            payment_completion = PaymentCompletion.objects.filter(payment=payment).first()
                            if payment_completion:
                                total_payment_amount += payment_completion.amount

                    elif advance_payments.exists():
                        payment_status = 'advance'
                        total_payment_amount = advance_payments.aggregate(Sum('amount'))['amount__sum'] or 0.0

                bookings_with_payment_info.append({
                    'booking': booking,
                    'total_payment_amount': total_payment_amount,
                    'payment_status': payment_status
                })

            room_service_form = RoomServiceForm()
            additional_charge_form = AdditionalChargeForm()
            context = {
                'bookings': bookings_with_payment_info,
                'room_service_form': room_service_form,
                "additional_charge_form": additional_charge_form,
                'active_attendance': active_attendance,
            }

            return render(request, template, context)
        messages.error(request," You are not on an Active schedule")
    return render (request, template, context)



def frontdesk_update_checkout_date(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        form = UpdateCheckOutDateForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Check-out date updated successfully.')
            return redirect('dashboard:checkout_list')  
    else:
        messages.error(request, 'Unable to Update Check-out date updated.')
        return redirect('dashboard:checkout_list')
     

# checkout list
def frontdesk_checkout_list(request):
    template = "front_desk/check_out_list.html"

    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
 
       
        booking_list = Booking.objects.filter(
            check_out_date__lte=timezone.now(),
            is_active=True,
            checked_in=True
        )
        
        form = UpdateCheckOutDateForm()
        context = {
            'form': form,
            'bookings': booking_list,
            'active_attendance':active_attendance,
        }
        return render(request, template, context)
    else:
        return redirect('core:index')
    

def generate_unique_username(base_username):
    username = base_username
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{get_random_string(4, allowed_chars=string.ascii_lowercase)}"
    return username


# #htmx view for avaiilable room 
def available_rooms_view(request):
    room_type_id = request.GET.get('room_type')
    rooms = Room.objects.filter(room_type_id=room_type_id, is_available=True)

    return render(request, 'partials/htmx/available-rooms.html', {'rooms': rooms})


def front_desk_booking(request):
    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)
        hide_completed = True

        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
        room_type_id = request.POST.get('room_type') if request.method == 'POST' else None
        coupon_code = request.POST.get('coupon_code', '').strip().lower()

        if request.method == 'POST':
            basic_info_form = BasicUserInfoForm(request.POST)
            profile_info_form = ProfileInfoForm(request.POST)
            booking_choice_form = BookingChoiceForm(request.POST)
            room_booking_form = RoomBookingForm(request.POST, room_type_id=room_type_id)
            room_reservation_form = RoomReservationForm(request.POST)
            payment_form = PaymentForm(request.POST, exclude_completed=hide_completed)

            if basic_info_form.is_valid() and profile_info_form.is_valid() and booking_choice_form.is_valid():
                email = basic_info_form.cleaned_data['email']
                phone = basic_info_form.cleaned_data['phone']

                user = User.objects.filter(email=email).first()

                if not user:
                    user = basic_info_form.save(commit=False)
                    user.set_password(user.phone)
                    user.username = user.email
                    user.save()

                    profile, created = Profile.objects.get_or_create(user=user)
                    profile_form_data = profile_info_form.cleaned_data
                    for field, value in profile_form_data.items():
                        setattr(profile, field, value)
                    profile.save()

                # Initialize booking and reservation variables
                booking = None
                reservation = None

                # Check for booking or reservation choice
                choice = booking_choice_form.cleaned_data['choice']

                if choice == 'booking':
                    if room_booking_form.is_valid():
                        booking = room_booking_form.save(commit=False)
                        booking.user = user

                        # Handle coupon application
                        if coupon_code:
                            try:
                                coupon = Coupon.objects.get(code=coupon_code)
                                if coupon.is_valid_for_user(user):
                                    booking.coupon = coupon
                                    coupon.redeem_coupon(user)  # Redeem the coupon for the user
                                else:
                                    messages.error(request, 'Coupon is not valid for this user.')
                            except Coupon.DoesNotExist:
                                messages.error(request, 'Coupon code not found.')
                        
                        booking.save()

                        # Recalculate the total after the coupon is applied
                        booking_total_due = booking.get_total_due()
                    else:
                        print('Booking form errors:', room_booking_form.errors)
                elif choice == 'reservation':
                    if room_reservation_form.is_valid():
                        reservation = room_reservation_form.save(commit=False)
                        reservation.user = user
                        reservation.save()

                # Process payment if the form is valid
                if payment_form.is_valid():
                    payment = payment_form.save(commit=False)
                    payment.user = user
                    if booking:
                        payment.booking = booking
                       # payment.amount = booking.get_total_due()  # Ensure coupon is applied in total
                    elif reservation:
                        payment.booking = reservation

                    payment.save()

                # Redirect to the receipt page
                return redirect('dashboard:receipt', booking_id=booking.booking_id if booking else reservation.id)

        else:
            # Initialize forms for GET request
            basic_info_form = BasicUserInfoForm()
            profile_info_form = ProfileInfoForm()
            booking_choice_form = BookingChoiceForm()
            room_booking_form = RoomBookingForm(room_type_id=room_type_id)
            room_reservation_form = RoomReservationForm()
            payment_form = PaymentForm(exclude_completed=hide_completed)

        return render(request, 'front_desk/roombook.html', {
            'basic_info_form': basic_info_form,
            'profile_info_form': profile_info_form,
            'booking_choice_form': booking_choice_form,
            'room_booking_form': room_booking_form,
            'room_reservation_form': room_reservation_form,
            'payment_form': payment_form,
            'active_attendance': active_attendance,
        })


def front_desk_reservation(request):
    if request.method == 'POST':
        basic_info_form = BasicUserInfoForm(request.POST)
        profile_info_form = ProfileInfoForm(request.POST)
        booking_choice_form = BookingChoiceForm(request.POST)
        room_booking_form = RoomBookingForm(request.POST)
        room_reservation_form = RoomReservationForm(request.POST)
        payment_form = PaymentForm(request.POST)

        if basic_info_form.is_valid() and profile_info_form.is_valid() and booking_choice_form.is_valid():
            # Step 1: Check if the user already exists by email or phone number
            email = basic_info_form.cleaned_data['email']
            phone = basic_info_form.cleaned_data['phone']
            
            # Fetch or create user
            user = User.objects.filter(email=email).first()

            if not user:
                # If user doesn't exist, create a new one
                user = basic_info_form.save(commit=False)
                user.set_password(user.phone)  # Set phone number as password
                user.username = user.email  # Set email as the username
                user.save()

                # Create the profile for the user
                profile, created = Profile.objects.get_or_create(user=user)
                profile_form_data = profile_info_form.cleaned_data
                for field, value in profile_form_data.items():
                    setattr(profile, field, value)
                profile.save()

            # Step 2: Handle booking or reservation based on the user's choice
            choice = booking_choice_form.cleaned_data['choice']

            booking = None
            reservation = None

            if choice == 'booking':
                if room_booking_form.is_valid():
                    # Create the booking instance
                    booking = room_booking_form.save(commit=False)
                    booking.user = user
                    booking.save()  # Save the booking instance with ForeignKey to the room (no save_m2m needed)
            elif choice == 'reservation':
                if room_reservation_form.is_valid():
                    # Create the reservation instance
                    reservation = room_reservation_form.save(commit=False)
                    reservation.user = user
                    reservation.save()

            # Step 3: Attach payment to booking or reservation
            if payment_form.is_valid():
                payment = payment_form.save(commit=False)
                payment.user = user
                if booking:
                    payment.booking = booking
                elif reservation:
                    payment.booking = reservation  # Link payment to reservation if applicable
                payment.save()

            # Step 4: Redirect to receipt page with booking or reservation ID
            return redirect('dashboard:receipt', booking_id=booking.booking_id if booking else reservation.id)

    else:
        # Initialize forms if the request method is GET
        basic_info_form = BasicUserInfoForm()
        profile_info_form = ProfileInfoForm()
        booking_choice_form = BookingChoiceForm()
        room_booking_form = RoomBookingForm()
        room_reservation_form = RoomReservationForm()
        payment_form = PaymentForm()

    # Render the room reservation page with all the forms
    return render(request, 'front_desk/roomreserve.html', {
        'basic_info_form': basic_info_form,
        'profile_info_form': profile_info_form,
        'booking_choice_form': booking_choice_form,
        'room_booking_form': room_booking_form,
        'room_reservation_form': room_reservation_form,
        'payment_form': payment_form
    })



def receipt_view(request, booking_id):
    # Get the booking object
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    # Calculate total room charge based on the booking duration and room price

    context = {
        'customer': booking.user,  # Customer who made the booking
        'booking_date': booking.date_created,  # Date the booking was made
        'checkin_date': booking.check_in_date,  # Check-in date of the booking
        'checkout_date': booking.check_out_date,  # Check-out date of the booking
        'total_room_charge': booking.get_room_charges(),  # Total room charge
        'coupon': booking.coupon,  # Coupon if any applied
        'coupon_type': booking.coupon.type if booking.coupon else None,  # Coupon type (if any)
        'coupon_discount_value': booking.get_coupon_discount(),  # Coupon discount
        'total_after_discount': booking.get_total_after_discount(),  # Total after discount
        'initial_amount_paid': booking.get_initial_payment(),  # Amount paid by the customer
        'balance_remaining': booking.get_balance_remaining(),  # Remaining balance
    }
    
    return render(request, 'front_desk/booking/receipt.html', context)


def frontdesk_add_room_service(request, pk):
    booking_instance = Booking.objects.get(pk = pk)
    if request.method == "POST":
        add_room_service_form = RoomServiceForm(request.POST)
        if add_room_service_form.is_valid():
            room_service_form = add_room_service_form.save(commit=False)
            room_service_form.booking = booking_instance
            room_service_form.room = booking_instance.room
            room_service_form.save()
            
            messages.success(request,"Room service sucessfull added to booking")
            return redirect("dashboard:frontdesk_booking_list")
        else:
            messages.error(request,"Something wnt wrong, Unable to add Room service")
            return redirect("dashboard:frontdesk_booking_list")
    else:
        messages.error(request,f"Invalid Form: unable to room service to booking")
        return redirect("dashboard:frontdesk_booking_list")
            
        

def frontdesk_add_additional_charge(request, pk):
    booking_instance = Booking.objects.get(pk = pk)
    if request.method == "POST":
        additional_service_form = AdditionalChargeForm(request.POST)
        if additional_service_form.is_valid():
            room_service_form = additional_service_form.save(commit=False)
            room_service_form.booking = booking_instance
            room_service_form.save()
            
            messages.success(request,"Room service sucessfull added to booking")
            return redirect("dashboard:frontdesk_booking_list")
        else:
            messages.error(request,"Something wnt wrong, Unable to add Room service")
            return redirect("dashboard:frontdesk_booking_list")
    else:
        messages.error(request,f"Invalid Form: unable to room service to booking")
        return redirect("dashboard:frontdesk_booking_list")
    

def frontdesk_apply_coupon_to_booking(request, pk):
    
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        try:
            # get the coupon by its code and check if it's active
            coupon = Coupon.objects.get(
                code=coupon_code, active=True, 
                valid_from__lte=timezone.now(), valid_to__gte=timezone.now()
            )
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code.")
            return redirect('checkout', pk=pk)

        # Check if the coupon has already been used by this user
        if CouponUsers.objects.filter(coupon=coupon, booking=booking).exists():
            messages.error(request, "You have already used this coupon.")
            return redirect('dashboard:checkout', pk=pk)

        # Apply the coupon to the booking
        booking.apply_coupon(coupon)

        # Create a record in the CouponUsers model to track the user who used the coupon
        CouponUsers.objects.create(booking=booking, coupon=coupon)

        messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
        return redirect('dashboard:checkout', pk=pk)

    return redirect('dashboard:checkout', pk=pk)


def checkout_view(request, id):
   
    # Get the user and booking
    booking = get_object_or_404(Booking, id=id)

    # Get the receipt summary
    receipt_summary = booking.get_receipt_summary()

    # Prepare context for the template
    context = {
        'booking':booking,
        'booking_id': receipt_summary['booking_id'],
        'user': receipt_summary['user'],
        'booking_date': receipt_summary['booking_date'],
        'checkin_date': receipt_summary['checkin_date'],
        'checkout_date': receipt_summary['checkout_date'],
        'num_days': receipt_summary['num_days'],
        'room_charges': receipt_summary['room_charges'],
        'additional_charges': receipt_summary['additional_charges'],
        'additional_services':receipt_summary['additional_services'],
        'coupon_applied': receipt_summary['coupon_applied'],
        'sum_of_all_charges':receipt_summary['sum_of_all_charges'],
        'coupon_discount': receipt_summary['coupon_discount'],
        'initial_payment': receipt_summary['initial_payment'],
        'final_charge': receipt_summary['final_charge'],
        'amount_payable': receipt_summary['amount_payable'],
    }

    return render(request, 'front_desk/booking/checkout_details.html', context)


def frontdesk_checkout_payment_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    total_after_discount = booking.amount_payable

    if request.method == 'POST':
        form = PaymentCheckoutForm(request.POST)
        if form.is_valid():
            # Get the existing payment record for the booking
            payment = Payment.objects.filter(booking=booking).first()
            if payment:
                # Only update the payment status
                payment.status = form.cleaned_data['status']
                
                if payment.status == 'completed':
                    payment.save()  # Save only the updated status
                    
                    # Create or update PaymentCompletion record using form data
                    completion, created = PaymentCompletion.objects.get_or_create(
                        payment=payment,
                        defaults={
                            'amount': form.cleaned_data['amount'],  # Use form amount
                            'mode': form.cleaned_data['mode'],      # Use form mode
                            'transaction_id': payment.transaction_id  # Use payment's transaction_id
                        }
                    )
                    if not created:
                        completion.amount = form.cleaned_data['amount']  # Update completion with form data
                        completion.mode = form.cleaned_data['mode']
                        completion.transaction_id = payment.transaction_id
                        completion.save()

                    # Update booking and room statuses
                    booking.is_active = False
                    booking.checked_in = False
                    booking.checked_out = True
                    booking.save()

                    if booking.room:
                        booking.room.is_available = True
                        booking.room.save()

                    return redirect('dashboard:frontdesk_booking_list')
                else:
                    messages.error(request, 'Payment must be marked as completed to  effectively checkout.')
                    return redirect('dashboard:checkout', id=pk)
            else:
                messages.error(request, 'No payment record found for this booking.')
                return redirect('dashboard:checkout', id=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PaymentCheckoutForm(initial={'amount': total_after_discount})

    context = {
        'booking': booking,
        'form': form,
    }
    return render(request, 'front_desk/booking/checkout_payment.html', context)

#Frontdesk views ends here 
# ==========================================================================================================
# ==========================================================================================================



#pos user views
#========================================================================================================
#=======================================================================================================

def pos_user_dashboard(request):
    template = 'pos_officer/dashboard.html'

    # Ensure the current user is a POS user and find the active schedule and attendance
    if request.user.is_pos_officer:
        user = request.user
        employee = user.employee_profile
        pos_user = employee
        
        # Get active attendance and schedule
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
        active_schedule = StaffSchedules.objects.filter(employee=employee, active=True).first()

        if active_attendance and active_schedule:

            # Construct the start and end datetime of the active schedule
            schedule_start = timezone.make_aware(
                datetime.combine(active_schedule.schedule_start_date, active_schedule.start_time)
            )
            schedule_end = timezone.make_aware(
                datetime.combine(active_schedule.schedule_end_date, active_schedule.end_time)
            )
            # Validate schedule start and end times
            start_time = active_schedule.start_time
            end_time = active_schedule.end_time

            if start_time is None or end_time is None:
                return render(request, template, {'error': 'Schedule times are missing.'})

            # Total order quantity from OrderItems during active schedule and attendance
            total_order_quantity = OrderItem.objects.filter(
                order__staff=pos_user,
                date_created__range=(schedule_start, schedule_end)
            ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

            # Count of orders during active schedule and attendance
            order_count = Order.objects.filter(
                staff=pos_user,
                created_at__range=(schedule_start, schedule_end)
            ).count()

            # Total quantity received from StockReceipt during active schedule and attendance
            total_quantity_received = StockReceipt.objects.filter(
                department_user=pos_user,
                updated_at__range=(schedule_start, schedule_end),
                mark_as_received=True  # Ensure mark_as_received is True
            ).aggregate(total_quantity_received=Sum('quantity_received'))['total_quantity_received'] or 0

            # List of products with their quantity received during active schedule and attendance
            products_received = Product.objects.filter(
                stockreceipt__department_user=pos_user,
                department_location =pos_user.department_location,
                date_created__range=(schedule_start, schedule_end),
                stockreceipt__mark_as_received=True  # Ensure mark_as_received is True
            ).annotate(
                quantity_received=Sum('stockreceipt__quantity_received')
            )

            # List of products with their category and quantity left, considering the department location of the pos_user
            products = Product.objects.filter(
                department_location=pos_user.department_location  # Filter by pos_user's department location
            ).annotate(
                total_quantity_left=F('stock_quantity')  # Get the remaining stock quantity for each product
            ).values(
                'category__name',  # Get the product category name
                'name',    # Get the product name
                'price',      # Get the product price    
                'total_quantity_left'  # Get the remaining quantity of the product
            )


            # Total stock remaining for products where department location matches pos_user's department location
            total_stock_remaining = Product.objects.filter(
                department_location=pos_user.department_location
            ).aggregate(
                total_stock=Sum('stock_quantity')
            )['total_stock'] or 0

            # Total amount paid where payment status is PAID during active schedule and attendance
            total_paid = PosPayment.objects.filter(
                order__staff=pos_user,
                payment_status='PAID',
                created_at__range=(schedule_start, schedule_end)
            ).aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0

                    # Retrieve all stock that has not been marked as received, belonging to the user's department
            unreceived_stock = StockReceipt.objects.filter(
                department_location=pos_user.department_location,  # Stock belonging to the same department
                mark_as_received=False  # Stock not marked as received
            ).order_by('-date_received')

            context = {
                'active_attendance': active_attendance,
                'active_schedule': active_schedule,
                'total_order_quantity': total_order_quantity,
                'order_count': order_count,
                'total_quantity_received': total_quantity_received,
                'total_stock_remaining': total_stock_remaining,
                'total_paid': total_paid,
                'products': products,
                'products_received': products_received,
                'unreceived_stock': unreceived_stock,
                'pos_user':pos_user,
            }

            return render(request, template, context)

    return render(request, template, {'error': 'No active attendance or schedule found.'})


def pos_orders(request):
    template = "pos_officer/orders.html"
    
    if request.user.is_pos_officer:
        user = request.user
        employee = get_object_or_404(Employee, user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()

        # Check if there's an active schedule
        active_schedule = StaffSchedules.objects.filter(
            employee=employee,
            active='True',
            schedule_start_date__lte=timezone.now().date(),
            schedule_end_date__gte=timezone.now().date()
        ).first()

        orders = []
        if active_attendance and active_schedule:
            # Retrieve orders for this POSUser during the active attendance period
            pos_user = Employee.objects.filter(user=user).first()
            
            if pos_user:
                orders = Order.objects.filter(
                    staff=pos_user,
                    created_at__gte=active_attendance.check_in,  # Orders made after the check-in time
                    created_at__lte=timezone.now()  # Orders made until now
                )

        context = {
            "active_attendance": active_attendance,
            "orders": orders,
        }

        return render(request, template, context)
    else:
        return redirect('dashboard:pos_orders')



def user_update_received_stock(request):
    template = 'pos_officer/daily_stock_received.html'

    if request.user.is_pos_officer:
        user = request.user
        employee = get_object_or_404(Employee, user=user)
        department_location = employee.department_location


        # Get the active attendance record
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()

        # Get the active staff schedule
        active_schedule = StaffSchedules.objects.filter(
            employee=employee, 
            active="True"  # Make sure we only fetch the active schedule
        ).first()

        if active_schedule:
            # Construct the start and end datetime of the active schedule
            schedule_start = timezone.make_aware(
                datetime.combine(active_schedule.schedule_start_date, active_schedule.start_time)
            )
            schedule_end = timezone.make_aware(
                datetime.combine(active_schedule.schedule_end_date, active_schedule.end_time)
            )

            # Retrieve stock received within the schedule period
            daily_stock = StockReceipt.objects.filter(
                department_user=employee,  # POS officer who received the stock
                mark_as_received=True,  # Stock marked as received
                updated_at__range=(schedule_start, schedule_end)  # Filter by schedule timeframe
            )
        else:
            # If no active schedule is found, set daily_stock to an empty queryset
            daily_stock = StockReceipt.objects.none()


        # Retrieve all stock received by the user for their department, regardless of the schedule
        all_stock = StockReceipt.objects.filter(
            department_user=employee,  # POS officer who received the stock
            mark_as_received=True  # Stock marked as received
        ).order_by('-date_received')  # Order by the latest received items

        
        # Retrieve all stock that has not been marked as received, belonging to the user's department
        unreceived_stock = StockReceipt.objects.filter(
            department_location=department_location,  # Stock belonging to the same department
            mark_as_received=False  # Stock not marked as received
        ).order_by('-date_received')


        if request.method == "POST":
            form = updateReceivedItemForm(request.POST)
            if form.is_valid():
                receipt_form = form.save(commit=False)
                receipt_form.department_user = employee  # Assign the current employee as department_user
                receipt_form.save()

                messages.success(request, 'Product receipt created successfully.')
                return redirect('dashboard:received_stock')  # Redirect to the appropriate URL
            else:
                messages.error(request, 'Unable to create product receipt.')
                return redirect('dashboard:received_stock')  # Redirect to the appropriate URL
        else:
            form = updateReceivedItemForm()

        context = {
            'all_stock':all_stock,
            'daily_stock': daily_stock,
            'unreceived_stock': unreceived_stock,
            'active_attendance': active_attendance,
            'form': form,
        }

        return render(request, template, context)  # Correct render function

    else:
        return redirect('dashboard:received_stock')  # Redirect unauthorized users
 

def mark_product_as_received(request,pk):
    stock = get_object_or_404(StockReceipt, pk=pk)
    if request.method =="POST":
        employee = request.user.employee_profile
  
        form = updateReceivedItemForm(request.POST, instance=stock)

        if form.is_valid():
            stock_instance = form.save(commit=False)
            stock_instance.department_user = employee
            stock_instance.save()
            messages.success(request, 'Product was received successfully!')
            return redirect('dashboard:received_stock')  
        else:
            print(form.errors)
            messages.error(request, 'Error, could not received product.')
            return redirect('dashboard:received_stock')  
            
    else:
        messages.error(request, 'Something Went Wrong, Try Again.')
        return redirect('dashboard:received_stock') 


#oos User views ends
#=====================================================================================================
#======================================================================================================





            # # Total stock remaining across all products during active schedule and attendance
            # total_stock_remaining = Product.objects.annotate(
            #     remaining_stock=F('stock_quantity') - Sum(
            #         Case(
            #             When(
            #                 orderitem__order__staff=pos_user,
            #                 orderitem__order__created_at__date=current_date,
            #                 orderitem__order__created_at__time__gte=start_time,
            #                 orderitem__order__created_at__time__lte=end_time,
            #                 then=F('orderitem__quantity')
            #             ),
            #             default=0,
            #             output_field=IntegerField()
            #         )
            #     )
            # ).aggregate(
            #     total_stock=Sum('remaining_stock')
            # )['total_stock'] or 0