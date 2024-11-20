from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse,Http404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Hotel, Room, Booking, RoomServices, HotelGallery, HotelFeatures, RoomType
from datetime import datetime
from decimal import Decimal
from core.decorators import required_roles
from django.contrib import messages
from django.db.models import Q, Exists, OuterRef
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt




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
    
    context = {
     'hotel':hotel,
     'rooms': rooms,
     'room_types':room_types,
     }
    return render(request, template, context)




# @csrf_exempt
def add_room_to_cart(request):
    room_id = request.POST.get('room_id')
    room = get_object_or_404(Room, id=room_id)

    # Initialize cart in the session if not present
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    # Add or increment room count in the cart session data
    cart = request.session['cart']
    if room_id in cart:
        cart[room_id]['quantity'] += 1
    else:
        cart[room_id] = {
            'room_number': room.room_number,
            'quantity': 1,
        }

    # Save updated cart back to the session
    request.session['cart'] = cart
    request.session.modified = True
    
    # Calculate total items and render the cart count HTML snippet
    total_items = sum(item['quantity'] for item in cart.values())
    
    html = render_to_string("partials/htmx/cart_count.html", {"total_selected_items": total_items})
    return HttpResponse(html, content_type="text/html")





# def selected_rooms(request):
#     # Get the selected rooms from the cart in session
#     cart = request.session.get('cart', [])
#     rooms = Room.objects.filter(id__in=cart)
    
#     context = {
#         'rooms': rooms,
#     }
    
#     return render(request, 'pages/selected_rooms.html', context)

# def add_to_selection(request):
#     room_selection = {}

#     room_selection[str(request.GET['id'])] = {
#         'hotel_id': request.GET['hotel_id'],
#         'hotel_name': request.GET['hotel_name'],
#         'room_name': request.GET['room_name'],
#         'room_price': request.GET['room_price'],
#         'number_of_beds': request.GET['number_of_beds'],
#         'room_number': request.GET['room_number'],
#         'room_type': request.GET['room_type'],
#         'room_id': request.GET['room_id'],
#         'checkin': request.GET['checkin'],
#         'checkout': request.GET['checkout'],
#         'adult': request.GET['adult'],
#         'children': request.GET['children'],
#     }

#     if 'selection_data_obj' in request.session:
#         if str(request.GET['id']) in request.session['selection_data_obj']:

#             selection_data = request.session['selection_data_obj']
#             selection_data[str(request.GET['id'])]['adult'] = int(room_selection[str(request.GET['id'])]['adult'])
#             selection_data[str(request.GET['id'])]['children'] = int(room_selection[str(request.GET['id'])]['children'])
#             request.session['selection_data_obj'] = selection_data
#         else:
#             selection_data = request.session['selection_data_obj']
#             selection_data.update(room_selection)
#             request.session['selection_data_obj'] = selection_data
#     else:
#         request.session['selection_data_obj'] = room_selection
#     data = {
#         "data":request.session['selection_data_obj'], 
#         'total_selected_items': len(request.session['selection_data_obj'])
#         }
#     return JsonResponse(data)


# def delete_session(request):
#     request.session.pop('selection_data_obj', None)
#     return redirect(request.META.get("HTTP_REFERER"))


# def delete_selection(request):
#     hotel_id = str(request.GET['id'])
#     if 'selection_data_obj' in request.session:
#         if hotel_id in request.session['selection_data_obj']:
#             selection_data = request.session['selection_data_obj']
#             del request.session['selection_data_obj'][hotel_id]
#             request.session['selection_data_obj'] = selection_data


#     total = 0
#     total_days = 0
#     room_count = 0
#     adult = 0 
#     children = 0 
#     checkin = "" 
#     checkout = "" 
#     children = 0 
#     hotel = None

#     if 'selection_data_obj' in request.session:
#         for h_id, item in request.session['selection_data_obj'].items():
                
#             id = int(item['hotel_id'])

#             checkin = item["checkin"]
#             checkout = item["checkout"]
#             adult += int(item["adult"])
#             children += int(item["children"])
#             room_type_ = item["room_type"]
            
#             hotel = Hotel.objects.get(id=id)
#             room_type = RoomType.objects.get(id=room_type_)

#             date_format = "%Y-%m-%d"
#             checkin_date = datetime.strptime(checkin, date_format)
#             checout_date = datetime.strptime(checkout, date_format)
#             time_difference = checout_date - checkin_date
#             total_days = time_difference.days

#             room_count += 1
#             days = total_days
#             price = room_type.price

#             room_price = price * room_count
#             total = room_price * days
        
    
#     context = render_to_string("pages/async/selected_rooms.html", { "data":request.session['selection_data_obj'],  "total_selected_items": len(request.session['selection_data_obj']), "total":total, "total_days":total_days, "adult":adult, "children":children,    "checkin":checkin,    "checkout":checkout,    "hotel":hotel})

#     print("data ======", context)
    
#     return JsonResponse({"data": context, 'total_selected_items': len(request.session['selection_data_obj'])})

