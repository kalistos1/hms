from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.contrib import messages
from dashboard . models import *
from accounts.models import *
from bookings.models import *
import string
from .forms import BookingForm, CustomerForm

# Create your views here.

def admin_dashboard(request):
    template = "admin_user/dashboard.html"
    
    return render (request,template)


def supervisor_dashboard(request):
    template = "supervisor/dashboard.html"
    
    return render (request,template)


def account_dashboard(request):
    template = "account_officer/dashboard.html"
    
    return render (request,template)



def frontdesk_dashboard(request):
    template = "front_desk/dashboard.html"
    
    return render (request,template)


#room status 
def frontdesk_room_status(request):
    template = "front_desk/roomstatus.html"
    room_status = Room.objects.all()
    context = {
        'room_status':room_status
    }
    
    return render (request,template, context)



# bookings
def frontdesk_booking_list(request):
    template = "front_desk/bookinglist.html"
    
    bookin_list = Booking.objects.all()
    context = {
        'bookings':bookin_list,
    }
    
    return render (request,template, context)




def generate_unique_username(base_username):
    username = base_username
    while User.objects.filter(username=username).exists():
        username = f"{base_username}_{get_random_string(4, allowed_chars=string.ascii_lowercase)}"
    return username
    

def frontdesk_room_book(request):
    template = "front_desk/roombook.html"

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST, request.FILES)
        booking_form = BookingForm(request.POST)

        # Extract the email or unique identifier to check for an existing user
        email = request.POST.get('email')
        existing_user = User.objects.filter(email=email).first()

        if existing_user:
            user = existing_user
            profile = user.profile  # Access the existing profile
            profile.title = customer_form.cleaned_data['title']
            profile.phone = customer_form.cleaned_data['phone']
            profile.date_of_birth = customer_form.cleaned_data['date_of_birth']
            profile.gender = customer_form.cleaned_data['gender']
            profile.country = customer_form.cleaned_data['country']
            profile.nationality = customer_form.cleaned_data['nationality']
            profile.city = customer_form.cleaned_data['city']
            profile.state = customer_form.cleaned_data['state']
            profile.address = customer_form.cleaned_data['address']
            profile.occupation = customer_form.cleaned_data['occupation']
            profile.id_no = customer_form.cleaned_data['id_no']
            profile.identity_type = customer_form.cleaned_data['identity_type']
            profile.identity_image_front = customer_form.cleaned_data['identity_image_front']
            profile.identity_image_back = customer_form.cleaned_data['identity_image_back']
            profile.save()

            messages.info(request, "Using existing user and profile.")
        else:
            if customer_form.is_valid():
                base_username = customer_form.cleaned_data['email'].split('@')[0]
                unique_username = generate_unique_username(base_username)

                user = customer_form.save(commit=False)
                random_password = get_random_string(length=8)
                user.username = unique_username
                user.set_password(random_password)
                user.save()

                # The profile is created automatically by the post_save signal.
                profile = user.profile  # Access the automatically created profile
                profile.title = customer_form.cleaned_data['title']
                profile.phone = customer_form.cleaned_data['phone']
                profile.date_of_birth = customer_form.cleaned_data['date_of_birth']
                profile.gender = customer_form.cleaned_data['gender']
                profile.country = customer_form.cleaned_data['country']
                profile.nationality = customer_form.cleaned_data['nationality']
                profile.city = customer_form.cleaned_data['city']
                profile.state = customer_form.cleaned_data['state']
                profile.address = customer_form.cleaned_data['address']
                profile.occupation = customer_form.cleaned_data['occupation']
                profile.id_no = customer_form.cleaned_data['id_no']
                profile.identity_type = customer_form.cleaned_data['identity_type']
                profile.identity_image_front = customer_form.cleaned_data['identity_image_front']
                profile.identity_image_back = customer_form.cleaned_data['identity_image_back']
                profile.save()

                messages.success(request, f"Customer {user.username} booked successfully! Password: {random_password}")
            else:
                for error in customer_form.errors.as_data():
                    print(f"Customer form error: {error} - {customer_form.errors[error]}")
                messages.error(request, "There were errors in the customer form submission. Please correct them and try again.")
                return render(request, template, {'customer_form': customer_form, 'booking_form': booking_form})

        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = user
            booking.created_by = request.user
            booking.save()
            booking.room.set(booking_form.cleaned_data['room'])

            for room in booking.room.all():
                room.is_available = False
                room.save()

            messages.success(request, f"Booking successfully created for {user.username}!")
            return redirect('dasboard:frontdesk_booking_list')
        else:
            for error in booking_form.errors.as_data():
                print(f"Booking form error: {error} - {booking_form.errors[error]}")
            messages.error(request, "There were errors in the booking form submission. Please correct them and try again.")

    else:
        customer_form = CustomerForm()
        booking_form = BookingForm()

    context = {
        'customer_form': customer_form,
        'booking_form': booking_form
    }
    return render(request, template, context)



def frontdesk_room_checkout(request):
    template = "front_desk/roomcheckout.html"
    booked_rooms = Room.objects.filter(is_available = False)
    context = {
        'rooms':booked_rooms,
    }
    
    return render (request,template,context)