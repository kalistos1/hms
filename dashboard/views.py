from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib import messages
from dashboard . models import *
from accounts.models import *
from bookings.models import *
import string
from .forms import *
from django.db.models import Count
from accounts.forms import *
from formtools.wizard.views import SessionWizardView
from django.db.models import Sum
from datetime import timedelta

from django.contrib.auth import login
from bookings.forms import (
    BasicUserInfoForm, ProfileInfoForm, 
    BookingChoiceForm, RoomBookingForm, RoomReservationForm, 
    RoomServiceForm, PaymentForm,AdditionalChargeForm
)
from django.utils import timezone



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
# ================================================================================================================

def admin_users_list(request):
    template ="admin_user/admin_user.html"
  
    admin_form = AddAdminForm()
    supervisor_form = AddSupervisorForm()
    frontdesk_form = AddFrontdeskForm()
    pos_officer_form = AddPosOfficerForm()
    account_officer_form = AddAccountOfficerForm()
    
    privilage_users = User.objects.filter(
                            is_admin=True
                        ) | User.objects.filter(
                            is_supervisor=True
                        ) | User.objects.filter(
                            is_account_officer=True
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
        'account_officer_form':account_officer_form       
    }
    return render(request, template, context)



def add_admin_privilaged_user(request):
    
    admin_form = AddAdminForm()
    supervisor_form = AddSupervisorForm()
    frontdesk_form = AddFrontdeskForm()
    pos_officer_form = AddPosOfficerForm()
    account_officer_form = AddAccountOfficerForm()

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

    messages.error(request, f"Something Went Wrong, Account Officer was not created!")
    return redirect('dashboard:admin_users_list')





def admin_delete_privilaged_user(request, pk):
    
    room_type = get_object_or_404(User, pk=pk)
    if request.method == 'GET':
        room_type.delete()
        messages.success(request, 'user deleted successfully!')
        return redirect('dashboard:admin_users_list')
    
    return redirect('dashboard:admin_users_list')



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



def frontdesk_dashboard(request):
    template = "front_desk/dashboard.html"
    
    if request.user.is_frontdesk_officer:
    
     return render (request,template)


#room status 
def frontdesk_room_status(request):
    template = "front_desk/roomstatus.html"
    
    if request.user.is_frontdesk_officer:
        
        room_status = Room.objects.all()
        context = {
            'room_status':room_status
        }
        
        return render (request,template, context)



# bookings
def frontdesk_booking_list(request):
    template = "front_desk/bookinglist.html"
  
    if request.user.is_frontdesk_officer:
        bookin_list = Booking.objects.all()
        room_service_form =  RoomServiceForm()
        additional_charge_form =  AdditionalChargeForm()
        context = {
            'bookings':bookin_list,
            'room_service_form': room_service_form,
            "additional_charge_form":additional_charge_form,
        }
        
        return render (request,template, context)




def generate_unique_username(base_username):
    username = base_username
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{get_random_string(4, allowed_chars=string.ascii_lowercase)}"
    return username


def front_desk_booking(request):
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
                    payment.booking = reservation  # Assuming reservation can be treated as a booking in the payment
                payment.save()

            # Redirect to receipt view with the booking ID
            return redirect('dashboard:receipt', booking_id=booking.booking_id if booking else reservation.id)
    else:
        # Initialize empty forms for GET request
        basic_info_form = BasicUserInfoForm()
        profile_info_form = ProfileInfoForm()
        booking_choice_form = BookingChoiceForm()
        room_booking_form = RoomBookingForm()
        room_reservation_form = RoomReservationForm()
        payment_form = PaymentForm()

    return render(request, 'front_desk/roombook.html', {
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
    



def frontdesk_room_checkout(request):
        template = "front_desk/roomcheckout_detail.html"
        
        if request.user.is_frontdesk_officer:
            
            booked_rooms = Room.objects.filter(is_available = False)
            context = {
                'rooms':booked_rooms,
            }
            
            return render (request,template,context)
        
        
        
        

def frontdesk_apply_coupon_to_booking(request, booking_id):

    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        try:
            # Fetch the coupon by its code and check if it's active
            coupon = Coupon.objects.get(code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid or expired coupon code.")
            return redirect('booking_detail', booking_id=booking_id)

        # Check if the coupon has already been used by this user
        if CouponUsers.objects.filter(coupon=coupon, user=booking.user).exists():
            messages.error(request, "You have already used this coupon.")
            return redirect('booking_detail', booking_id=booking_id)

        # Apply the coupon to the booking
        booking.apply_coupon(coupon)

        # Create a record in the CouponUsers model to track the user who used the coupon
        CouponUsers.objects.create(user=booking.user, coupon=coupon)

        messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
        return redirect('booking_detail', booking_id=booking_id)

    return render(request, 'apply_coupon.html', {'booking': booking})

        
#Frontdesk views ends here 
# ==========================================================================================================
# ==========================================================================================================


# from django.http import JsonResponse
# from .models import Booking, Coupon

def apply_coupon_to_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    coupon_code = request.POST.get('coupon_code')

    try:
        coupon = Coupon.objects.get(code=coupon_code, active=True)
        if coupon.valid_from <= timezone.now().date() <= coupon.valid_to:
            # Apply the coupon to the booking
            booking.apply_coupon(coupon)
            return JsonResponse({'success': True, 'new_total': booking.total_amount})
        else:
            return JsonResponse({'success': False, 'message': 'Coupon is not valid for current date.'})
    except Coupon.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid coupon code.'})
    
    
    # process additional charge

# from .models import Booking, AdditionalCharge
# from .forms import AdditionalChargeForm
# from django.db import transaction

def add_additional_charge(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if not booking.is_active:
        messages.error(request, 'Cannot add charges to an inactive booking.')
        return redirect('booking_detail', booking_id=booking.booking_id)
    
    if request.method == 'POST':
        form = AdditionalChargeForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                additional_charge = form.save(commit=False)
                additional_charge.booking = booking
                additional_charge.save()
                # Potentially update booking.total_amount or other related fields
            messages.success(request, 'Additional charge added successfully.')
            return redirect('booking_detail', booking_id=booking.booking_id)
    else:
        form = AdditionalChargeForm()
    return render(request, 'add_additional_charge.html', {'form': form, 'booking': booking})


def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    total_due = booking.get_total_with_additional_charges() - booking.payments.filter(status='completed').aggregate(total=models.Sum('amount'))['total'] or 0
    
    if request.method == 'POST':
        # Assume you have a form for payment details
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = total_due
            payment.save()
            # Update payment status based on actual payment processing
            payment.status = 'completed'  # or 'failed' based on real outcome
            payment.save()
            messages.success(request, 'Payment processed successfully.')
            return redirect('booking_detail', booking_id=booking.booking_id)
    else:
        form = PaymentForm()
    
    return render(request, 'process_payment.html', {'form': form, 'booking': booking, 'total_due': total_due})


def available_rooms(request, room_type_id, check_in_date, check_out_date):
    room_type = RoomType.objects.get(id=room_type_id)
    available_rooms = []

    for room in room_type.room_set.all():
        overlapping_bookings = Booking.objects.filter(
            room=room,
            is_active=True,
            check_in_date__lt=check_out_date,
            check_out_date__gt=check_in_date
        )
        if not overlapping_bookings.exists():
            available_rooms.append(room)

    return render(request, 'available_rooms.html', {'available_rooms': available_rooms})