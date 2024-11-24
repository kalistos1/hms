
from django.contrib.auth import authenticate, login
from accounts.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Hotel, Room, Booking, RoomServices, HotelGallery, HotelFeatures, RoomType, Reservation, Payment
from datetime import datetime
from decimal import Decimal
from core.decorators import required_roles
from django.contrib import messages
from django.db.models import Q, Exists, OuterRef
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
# from .utils import get_total_selected_items



def check_room_availability(request):
    if request.method == "POST":
        hotel_id = request.POST.get("hotel-id")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        capacity = request.POST.get("capacity")
        room_type_slug = request.POST.get("room-type")

        # Retrieve hotel
        hotel = get_object_or_404(Hotel, status="Live", id=hotel_id)

        try:
            # Attempt to retrieve the room type
            room_type = get_object_or_404(RoomType, hotel=hotel, slug=room_type_slug)
        except Http404:
            messages.error(request, "The selected room type is unavailable. Please choose a different room type.")
            return redirect("booking:booking_data", room_type_slug)

        # Convert check-in and check-out dates to date objects
        checkin_date = parse_date(checkin)
        checkout_date = parse_date(checkout)

        # Subquery to check if rooms are booked within the desired date range
        conflicting_bookings = Booking.objects.filter(
            room=OuterRef('pk'),
            check_in_date__lt=checkout_date,
            check_out_date__gt=checkin_date
        )

        # Filter rooms of the selected type that are not booked in the desired date range
        available_rooms = Room.objects.filter(
            room_type=room_type,
            is_available=True
        ).annotate(
            is_conflicting=Exists(conflicting_bookings)
        ).filter(is_conflicting=False)

        # Check if any rooms are available
        if not available_rooms.exists():
            messages.warning(request, "No rooms available for the selected dates. Please try different dates.")
            return redirect("booking:booking_data", hotel.slug)

        # Store booking data in session
        request.session['booking_data'] = {
            'hotel_id': hotel_id,
            'checkin': checkin,
            'checkout': checkout,
            'capacity': capacity,
            'room_type': room_type_slug,
        }

        # Redirect to the room type detail view with available rooms only
        return HttpResponseRedirect(reverse("core:room_type_detail", args=[hotel.slug, room_type.slug]))

    # Redirect to hotel index if request is not POST
    return redirect("core:index")




def booking_data(request, slug):
    template ='pages/roomlist.html'
    hotel = Hotel.objects.filter(status='Live').first()
    rooms = Room.objects.all()
    room_types =RoomType.objects.all()
    # total_selected_items = get_total_selected_items(request.session)
    context = {
     'hotel':hotel,
     'rooms': rooms,
     'room_types':room_types,
    #  'total_selected_items': total_selected_items, 
     }
    return render(request, template, context)



# # @csrf_exempt
# def add_room_to_cart(request):
#     room_id = request.POST.get('room_id')
#     room = get_object_or_404(Room, id=room_id)

#     # Initialize cart in the session if not present
#     if 'cart' not in request.session:
#         request.session['cart'] = {}
    
#     # Add or increment room count in the cart session data
#     cart = request.session['cart']
#     if room_id in cart:
#         cart[room_id]['quantity'] += 1
#     else:
#         cart[room_id] = {
#             'room_number': room.room_number,
#             'quantity': 1,
#         }

#     # Save updated cart back to the session
#     request.session['cart'] = cart
#     request.session.modified = True
    
#     # Calculate total items and render the cart count HTML snippet
#     total_items = sum(item['quantity'] for item in cart.values())
    
#     html = render_to_string("partials/htmx/cart_count.html", {"total_selected_items": total_items})
#     return HttpResponse(html, content_type="text/html")


def selected_room(request, rid):
    room = get_object_or_404(Room, rid=rid)
    room_type = room.room_type
    hotel = room_type.hotel
    similar_rooms = Room.objects.filter(room_type=room_type)#.exclude(id=room.id)

    if request.method == "POST":
        checkin_str = request.POST.get("checkin")
        checkout_str = request.POST.get("checkout")
        capacity = request.POST.get("capacity")
        selected_room_rid = request.POST.get("room-type")

        # Validate and parse dates
        try:
            checkin = datetime.strptime(checkin_str, "%Y-%m-%d").date()
            checkout = datetime.strptime(checkout_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("booking:selected_room", rid=rid)

        # Ensure valid date range
        num_days = (checkout - checkin).days
        if num_days <= 0:
            messages.error(request, "Check-out date must be after check-in.")
            return redirect("booking:selected_room", rid=rid)

        # Get the selected room
        selected_room = Room.objects.filter(rid=selected_room_rid).first()
        if not selected_room:
            messages.error(request, "Invalid room selection.")
            return redirect("booking:selected_room", rid=rid)

        # Calculate total cost
        room_price = selected_room.price_override or selected_room.room_type.base_price
        total_amount = Decimal(room_price) * Decimal(num_days)

        # Updated context
        context = {
            'hotel': hotel,
            'room': selected_room,
            'checkin': checkin,
            'checkout': checkout,
            'capacity': capacity,
            'num_days': num_days,
            'total_amount': total_amount,
            'similar_rooms': similar_rooms,
        }

        return render(request, "pages/selected_rooms.html", context)

    # Handle initial GET request
    checkin_str = request.GET.get("checkin")
    checkout_str = request.GET.get("checkout")
    capacity = request.GET.get("capacity")

    if not checkin_str or not checkout_str or not capacity:
        messages.error(request, "Room availability information is missing.")
        return redirect("booking:booking_data", slug=room.room_type.slug)

    try:
        checkin = datetime.strptime(checkin_str, "%Y-%m-%d").date()
        checkout = datetime.strptime(checkout_str, "%Y-%m-%d").date()
    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect("booking:booking_data", slug=room.room_type.slug)

    num_days = (checkout - checkin).days
    if num_days <= 0:
        messages.error(request, "Check-out date must be after check-in.")
        return redirect("booking:booking_data", slug=room.room_type.slug)

    room_price = room.price_override or room.room_type.base_price
    total_amount = Decimal(room_price) * Decimal(num_days)

    context = {
        'hotel': hotel,
        'room': room,
        'checkin': checkin,
        'checkout': checkout,
        'capacity': capacity,
        'num_days': num_days,
        'total_amount': total_amount,
        'similar_rooms': similar_rooms,
    }

    return render(request, "pages/selected_rooms.html", context)




def create_reservation(request):
    if request.method == "POST":
        try:
            # Extract submitted data
            room_id = request.POST.get("room_id")
            checkin_str = request.POST.get("checkin")
            checkout_str = request.POST.get("checkout")
            capacity = int(request.POST.get("capacity", 1))  # Default to 1 adult
            full_name = request.POST.get("full_name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")

            # Process full name into first and last name
            name_parts = full_name.strip().split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

            # Retrieve or create the user
            user, created = User.objects.get_or_create(email=email, defaults={
                "username": email,
                "first_name": first_name,
                "last_name": last_name,
                "phone":phone,
            })
            if not created and not user.check_password(phone):
                raise ValueError("Incorrect phone number for existing user.")
            user.set_password(phone)  # Update password if created
            user.t_and_c = True
            user.active_status = True
            user.save()
            login(request, user)

            # Validate room and dates
            room = get_object_or_404(Room, id=room_id)
            checkin = datetime.strptime(checkin_str, "%Y-%m-%d").date()
            checkout = datetime.strptime(checkout_str, "%Y-%m-%d").date()
            num_days = (checkout - checkin).days

            if num_days <= 0:
                raise ValueError("Invalid date range.")

            # Calculate total cost
            total_amount = Decimal(room.price_override or room.room_type.base_price) * Decimal(num_days)


            # Create reservation
            reservation = Reservation.objects.create(
                room=room,
                user=user,
                check_in_date=checkin,
                check_out_date=checkout,
                num_adults=capacity,
                total_amount=total_amount,
            )

            # Create a pending payment
            Payment.objects.create(
                online_reservation=reservation,
                status='pending',
                amount=total_amount,
                mode='cash',  # Default payment mode
            )

            # Redirect to the checkout page
            return redirect("core:checkout", reservation.reservation_id)

        except ValueError as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect("booking:selected_room", rid=request.POST.get("room_id"))
    
    return redirect("/")