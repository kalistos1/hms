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
from django.db.models import Sum, Case, When, F, IntegerField,Q
from django.contrib.auth import login
from bookings.forms import (
    BasicUserInfoForm, ProfileInfoForm, 
    BookingChoiceForm, RoomBookingForm, RoomReservationForm, 
    RoomServiceForm, PaymentForm,AdditionalChargeForm, PaymentCheckoutForm,UpdateCheckOutDateForm
)
from django.utils import timezone
from django.http import JsonResponse,HttpResponse
import datetime
from pos.models import *
from pos.forms import updateReceivedItemForm
from django.utils.timezone import make_aware,is_aware
today = datetime.date.today()



# admin view s start
# =========================================================================================
# ==========================================================================================

def admin_dashboard(request):
    template = "admin_user/dashboard.html"
    return render (request,template)


# Amenities
def admin_create_room_amenity(request):
    if request.method == 'POST':
        form = RoomAmenityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Amenity created successfully!')
            return redirect('dashboard:admin_list_room_amenities')  
        else:
            messages.error(request, 'Error creating Room Amenity. Please correct the errors below.')
            return redirect('dashboard:admin_list_room_amenities')  
            
    else:
        messages.error(request, 'Something Went Wrong. Try Again.')
        return redirect('dashboard:admin_list_room_amenities') 
    


def admin_list_room_amenities(request):
    amenities = RoomAmenity.objects.all()
    form = RoomAmenityForm()   
    context = {
        'amenities': amenities,
        'form':form,
        }
    return render(request, 'admin_user/amenities_list.html',context)



def admin_update_room_amenity(request, pk):
    amenity = get_object_or_404(RoomAmenity, pk=pk)
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
    
    amenity = get_object_or_404(RoomAmenity, pk=pk)
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
    amenity = get_object_or_404(RoomAmenity, pk=pk)
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
    return render (request,template)



#supervisor views ends here 
# ==========================================================================================================
# ==========================================================================================================




# Accountant views starts here 
# ===========================================================================================================
# ==========================================================================================================




def account_dashboard(request):
    template = "account_officer/dashboard.html"    
    return render (request,template)




#Accountant views ends here 
# ==========================================================================================================
# ==========================================================================================================



#Frontdesk  views starts here 
# ==========================================================================================================
# ==========================================================================================================



# def frontdesk_dashboard(request):
#     template = "front_desk/dashboard.html"
    
#     if request.user.is_frontdesk_officer:
       
#         today = timezone.now().date()

#         all_bookings = Booking.objects.filter( check_in_date =today)
#         user = request.user

#         employee = Employee.objects.get(user=user)
    
#         # Get the active attendance records
#         active_attendance = Attendance.objects.filter(employee=employee, check_in__date=today, active=True).first()


#         # Bookings created today
#         todays_bookings = Booking.objects.filter(date_created__date=today)

#         # Payments with status 'advance' or 'completed'
#         todays_payments = Payment.objects.filter(
#             Q(booking__in=todays_bookings) & (Q(status='advance') | Q(status='completed'))
#         )

#         # Sum of advance payments
#         advance_payments_total = todays_payments.filter(status='advance').aggregate(total=Sum('amount'))['total'] or 0

#         # Sum of completed payments
#         completed_payments_total = todays_payments.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0

#         # Sum of payment completions
#         payment_completion_total = PaymentCompletion.objects.filter(payment__booking__in=todays_bookings).aggregate(
#             total=Sum('amount')
#         )['total'] or 0

#         # Calculate the total money realized for today
#         todays_total_money = advance_payments_total + completed_payments_total + payment_completion_total

#         # Get all customers excluding specific user roles
#         customers = User.objects.filter(
#             is_admin=False,
#             is_supervisor=False,
#             is_account_officer=False,
#             is_frontdesk_officer=False,
#             is_pos_officer=False
#         )

#         context = {
#             'all_bookings': all_bookings.count(),
#             'todays_bookings': todays_bookings,
#             'total_todays_booking':todays_bookings.count(),
#             'todays_total_money': todays_total_money,
#             'customers': customers.count(),
#             'active_attendance':active_attendance,
#         }

#         return render(request, template, context)


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
                date_created__date=today,  # Adjust according to your model structure
                date_created__range=(check_in_time, check_out_time)
            )

            # Payments made for these bookings within the same time range
            todays_payments = Payment.objects.filter(
                booking__in=todays_bookings,
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


# bookings
def frontdesk_booking_list(request):
    template = "front_desk/bookinglist.html"
  
    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()

        bookin_list = Booking.objects.all()
        room_service_form =  RoomServiceForm()
        additional_charge_form =  AdditionalChargeForm()
        context = {
            'bookings':bookin_list,
            'room_service_form': room_service_form,
            "additional_charge_form":additional_charge_form,
            'active_attendance':active_attendance,
        }
        
        return render (request,template, context)
    


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

# htmx for room price
def get_room_price_view(request):
    room_type_id = request.GET.get('room_type')
    room_id = request.GET.get('room')

    base_price = 0
   
    if room_id:
        # Fetch price from Room model (priority if selected)
        room = Room.objects.filter(id=room_id, is_available=True).first()
        if room and room.price_override:
            base_price = room.price_override
        else:
            base_price = room.room_type.base_price if room else 0
    elif room_type_id:
        # Fetch price from RoomType model
        room_type = RoomType.objects.filter(id=room_type_id).first()
        base_price = room_type.base_price if room_type else 0
    # Return the updated input field HTML with the base price
    html = render_to_string('partials/htmx/payment_amount_input.html', {'base_price': base_price})
    return HttpResponse(html)

#htmx view for room price

def front_desk_booking(request):

    if request.user.is_frontdesk_officer:
        today = timezone.now().date()
        user = request.user
        employee = Employee.objects.get(user=user)

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()    
        room_type_id = request.POST.get('room_type') if request.method == 'POST' else None

        if request.method == 'POST':
            basic_info_form = BasicUserInfoForm(request.POST)
            profile_info_form = ProfileInfoForm(request.POST)
            booking_choice_form = BookingChoiceForm(request.POST)
            room_booking_form = RoomBookingForm(request.POST, room_type_id=room_type_id)  # Pass room_type_id
            room_reservation_form = RoomReservationForm(request.POST)
            payment_form = PaymentForm(request.POST)

            if basic_info_form.is_valid() and profile_info_form.is_valid() and booking_choice_form.is_valid():
    
                # Step 1: Check if the user already exists by email or phone number
                email = basic_info_form.cleaned_data['email']
                phone = basic_info_form.cleaned_data['phone']
                
                user = User.objects.filter(email=email).first() 

                if not user:
                    # If user doesn't exist, create a new one
                    user = basic_info_form.save(commit=False)
                    user.set_password(user.phone)  # Set phone number as password
                    user.username = user.email  # Set email as the username
                    user.save()

                    profile, created = Profile.objects.get_or_create(user=user)
                    profile_form_data = profile_info_form.cleaned_data
                    for field, value in profile_form_data.items():
                        setattr(profile, field, value)
                    profile.save()

                choice = booking_choice_form.cleaned_data['choice']

                booking = None
                reservation = None

                # Step 2: Save booking or reservation once
                if choice == 'booking':
                
                    if room_booking_form.is_valid():
                        booking = room_booking_form.save(commit=False)
                        booking.user = user
                        booking.save()
                    
                        room_booking_form.instance = booking 
                        room_booking_form.save_m2m()  # Save ManyToMany fields
                    else:
                        print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy', room_booking_form.errors)
                elif choice == 'reservation':
                    if room_reservation_form.is_valid():
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
                        payment.booking = reservation 
                    payment.save()

                return redirect('dashboard:receipt', booking_id=booking.booking_id if booking else reservation.id)

        else:
            basic_info_form = BasicUserInfoForm()
            profile_info_form = ProfileInfoForm()
            booking_choice_form = BookingChoiceForm()
            room_booking_form = RoomBookingForm(room_type_id=room_type_id)  # Pass room_type_id
            room_reservation_form = RoomReservationForm()
            payment_form = PaymentForm()

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
            
            user = User.objects.filter(email=email).first() 

            if not user:
                # If user doesn't exist, create a new one
                user = basic_info_form.save(commit=False)
                user.set_password(user.phone)  # Set phone number as password
                user.username = user.email  # Set email as the username
                user.save()

                profile, created = Profile.objects.get_or_create(user=user)
                profile_form_data = profile_info_form.cleaned_data
                for field, value in profile_form_data.items():
                    setattr(profile, field, value)
                profile.save()

            choice = booking_choice_form.cleaned_data['choice']

            booking = None
            reservation = None

            # Step 2: Save booking or reservation once
            if choice == 'booking':
                if room_booking_form.is_valid():
                    booking = room_booking_form.save(commit=False)
                    booking.user = user
                    booking.save()
                    room_booking_form.save_m2m()  # Save ManyToMany fields
            elif choice == 'reservation':
                if room_reservation_form.is_valid():
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
                    payment.booking = reservation 
                payment.save()

            return redirect('dashboard:receipt', booking_id=booking.booking_id if booking else reservation.id)
    else:
       
        basic_info_form = BasicUserInfoForm()
        profile_info_form = ProfileInfoForm()
        booking_choice_form = BookingChoiceForm()
        room_booking_form = RoomBookingForm()
        room_reservation_form = RoomReservationForm()
        payment_form = PaymentForm()

    return render(request, 'front_desk/roomreserve.html', {
        'basic_info_form': basic_info_form,
        'profile_info_form': profile_info_form,
        'booking_choice_form': booking_choice_form,
        'room_booking_form': room_booking_form,
        'room_reservation_form': room_reservation_form,
        'payment_form': payment_form
    })


def receipt_view(request, booking_id):
    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        return redirect('dashboard:frontdesk_booking_list') 

    # Calculate room charges
    total_room_charges = booking.get_room_charges()

    # Calculate room service charges
    total_service_charges = booking.get_service_charges()

    # Calculate additional charges
    total_additional_charges = booking.get_additional_charges()

    # Total amount payable
    total_amount_payable = booking.get_total_payable()

    # Get latest payment details
    payment = Payment.objects.filter(booking=booking).last()
    amount_paid = payment.amount if payment else 0
    payment_status = payment.status if payment else 'Unpaid'

    # Remaining balance
    remaining_balance = total_amount_payable - amount_paid

    # Pass context to template
    context = {
        'booking': booking,
        'total_room_charges': total_room_charges,
        'total_service_charges': total_service_charges,
        'total_additional_charges': total_additional_charges,
        'total_amount_payable': total_amount_payable,
        'amount_paid': amount_paid,
        'payment_status': payment_status,
        'remaining_balance': remaining_balance,
    }

    return render(request, 'front_desk/booking/receipt.html', context)



def re_issue_receipt_view(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return redirect('error_page')  # Handle case where booking does not exist

    # Calculate room charges
    total_room_charges = booking.get_room_charges()

    # Calculate room service charges
    total_service_charges = booking.get_service_charges()

    # Calculate additional charges
    total_additional_charges = booking.get_additional_charges()

    # Total amount payable
    total_amount_payable = booking.get_total_payable()

    # Get latest payment details
    payment = Payment.objects.filter(booking=booking).last()
    amount_paid = payment.amount if payment else 0
    payment_status = payment.status if payment else 'Unpaid'

    # Remaining balance
    remaining_balance = total_amount_payable - amount_paid

    context = {
        'booking': booking,
        'total_room_charges': total_room_charges,
        'total_service_charges': total_service_charges,
        'total_additional_charges': total_additional_charges,
        'total_amount_payable': total_amount_payable,
        'amount_paid': amount_paid,
        'payment_status': payment_status,
        'remaining_balance': remaining_balance,
    }

    return render(request, 'front_desk/booking/receipt.html', context)



def frontdesk_add_room_service(request, pk):
    booking_instance = Booking.objects.get(pk = pk)
    
    if request.method == "POST":
        add_room_service_form = RoomServiceForm(request.POST)
        if add_room_service_form.is_valid():
            room_service_form = add_room_service_form.save(commit=False)
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


def checkout_view(request, pk):
    try:
        booking = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return redirect('error_page')  # Handle case where booking does not exist

    # Calculate room charges, service charges, etc.
    total_room_charges = booking.get_room_charges()
    total_service_charges = booking.get_service_charges()
    total_additional_charges = booking.get_additional_charges()
    total_amount_payable = booking.get_total_payable()

    # Apply coupon discount if available
    discount_amount = booking.get_discount_amount()
    total_after_discount = booking.get_total_payable_after_discount()

    # Get latest payment details
    payment = Payment.objects.filter(booking=booking).last()
    amount_paid = payment.amount if payment else 0
    payment_status = payment.status if payment else 'Unpaid'

    # Remaining balance
    remaining_balance = total_after_discount -float( amount_paid)

    context = {
        'booking': booking,
        'total_room_charges': total_room_charges,
        'total_service_charges': total_service_charges,
        'total_additional_charges': total_additional_charges,
        'total_amount_payable': total_amount_payable,
        'discount_amount': discount_amount,
        'total_after_discount': total_after_discount,
        'amount_paid': amount_paid,
        'payment_status': payment_status,
        'remaining_balance': remaining_balance,
    }

    return render(request, 'front_desk/booking/checkout_details.html', context)


def frontdesk_checkout_payment_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    total_after_discount = booking.get_total_payable_after_discount()

    if request.method == 'POST':
        form = PaymentCheckoutForm(request.POST)
        if form.is_valid():
            # Get the existing payment record for the booking
            payment = Payment.objects.filter(booking=booking).first()
            if payment:
                payment.amount = form.cleaned_data['amount']
                payment.mode = form.cleaned_data['mode']
              
                payment.status = form.cleaned_data['status']
                
                if payment.status == 'completed':
                    payment.save()

                    # Create or update PaymentCompletion record
                    completion, created = PaymentCompletion.objects.get_or_create(
                        payment=payment,
                        defaults={
                            'amount': payment.amount,
                            'mode': payment.mode,
                            'transaction_id': payment.transaction_id
                        }
                    )
                    if not created:
                        completion.amount = payment.amount
                        completion.mode = payment.mode
                        completion.transaction_id = payment.transaction_id
                        completion.save()

                    # Update booking and room statuses
                    booking.is_active = False
                    booking.checked_in = False
                    booking.checked_out = True
                    booking.save()

                    for room in booking.room.all():
                        room.is_available = True
                        room.save()

                    return redirect('dashboard:frontdesk_booking_list')
                else:
                    messages.error(request, 'Payment must be completed to proceed.')
                    return redirect('dashboard:checkout', pk=pk)
            else:
                messages.error(request, 'No payment record found for this booking.')
                return redirect('dashboard:checkout', pk=pk)
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
        pos_user = employee.pos_user
        
        # Get active attendance and schedule
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()
        active_schedule = StaffSchedules.objects.filter(employee=employee, active=True).first()

        if active_attendance and active_schedule:
            # Get the current date and time
            current_date =timezone.now().date()
            current_time = timezone.now().time()

            # Validate schedule start and end times, compare only times without date conversion
            start_time = active_schedule.start_time
            end_time = active_schedule.end_time

            if start_time is None or end_time is None:
                return render(request, template, {'error': 'Schedule times are missing.'})

            # Assume the schedule is for the current day
            # Total order quantity from OrderItems during active schedule and attendance
            total_order_quantity = OrderItem.objects.filter(
                order__staff=pos_user,
                order__created_at__date=current_date,
                order__created_at__time__gte=start_time,
                order__created_at__time__lte=end_time
            ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

            # Count of orders during active schedule and attendance
            order_count = Order.objects.filter(
                staff=pos_user,
                created_at__date=current_date,
                created_at__time__gte=start_time,
                created_at__time__lte=end_time
            ).count()

            # Total quantity received from PosStockReceipt during active schedule and attendance
            total_quantity_received = PosStockReceipt.objects.filter(
                pos_user=pos_user,
                date_received__date=current_date,
                date_received__time__gte=start_time,
                date_received__time__lte=end_time
            ).aggregate(total_quantity_received=Sum('quantity_received'))['total_quantity_received'] or 0

            # List of products with their quantity received and remaining stock during the active schedule and attendance
            products = Product.objects.annotate(
                quantity_received=Sum(
                    Case(
                        When(
                            posstockreceipt__pos_user=pos_user,
                            posstockreceipt__date_received__date=current_date,
                            posstockreceipt__date_received__time__gte=start_time,
                            posstockreceipt__date_received__time__lte=end_time,
                            then=F('posstockreceipt__quantity_received')
                        ),
                        default=0,
                        output_field=IntegerField()
                    )
                ),
                remaining_stock=F('stock_quantity') - Sum(
                    Case(
                        When(
                            orderitem__order__staff=pos_user,
                            orderitem__order__created_at__date=current_date,
                            orderitem__order__created_at__time__gte=start_time,
                            orderitem__order__created_at__time__lte=end_time,
                            then=F('orderitem__quantity')
                        ),
                        default=0,
                        output_field=IntegerField()
                    )
                )
            )

            # Total stock remaining across all products during active schedule and attendance
            total_stock_remaining = products.aggregate(
                total_stock=Sum('remaining_stock')
            )['total_stock'] or 0

            # Total amount paid where payment status is PAID during active schedule and attendance
            total_paid = PosPayment.objects.filter(
                order__staff=pos_user,
                payment_status='PAID',
                order__created_at__date=current_date,
                order__created_at__time__gte=start_time,
                order__created_at__time__lte=end_time
            ).aggregate(total_paid=Sum('amount_paid'))['total_paid'] or 0

            context = {
                'active_attendance': active_attendance,
                'active_schedule': active_schedule,
                'total_order_quantity': total_order_quantity,
                'order_count': order_count,
                'total_quantity_received': total_quantity_received,
                'total_stock_remaining': total_stock_remaining,
                'total_paid': total_paid,
                'products': products
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
            pos_user = POSUser.objects.filter(employee=employee).first()
            
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

        # Get the active attendance record for today
        active_attendance = Attendance.objects.filter(employee=employee, active=True).first()

        # Get the POSUser linked to the employee
        pos_user = user.employee_profile.pos_user

        # Retrieve daily stock received today
        daily_stock = PosStockReceipt.objects.filter(pos_user=pos_user, date_received__date=timezone.now().date())

        if request.method == "POST":
            form = updateReceivedItemForm(request.POST)
            if form.is_valid():
                receipt_form = form.save(commit=False)
                receipt_form.pos_user = pos_user  # Assign the POSUser
                receipt_form.save()

                messages.success(request, 'Product receipt created successfully.')
                return redirect('dashboard:received_stock')  # Redirect to a valid URL or named view
            else:
                messages.error(request, 'Unable to create product receipt.')
                return redirect('dashboard:received_stock')  # Redirect to a valid URL or named view

        else:
            form = updateReceivedItemForm()

        context = {
            'daily_stock': daily_stock,
            'active_attendance': active_attendance,
            'form': form,
        }

        return render(request, template, context)  # Correct render function

    else:
        return redirect('dashboard:received_stock')  # Redirect unauthorized users

#oos User views ends
#=====================================================================================================
#======================================================================================================