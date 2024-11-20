
from bookings.models import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from bookings.models import Coupon, CouponUsers, Hotel, Room, Booking, RoomServices, HotelGallery, HotelFeatures, RoomType, Notification, Bookmark, Review
from datetime import datetime
from decimal import Decimal
import stripe
import json
from .decorators import required_roles

# Create your views here.


#index view
def index(request):
    template ='pages/index.html'
    
    hotel = Hotel.objects.filter(status='Live').first()
    
    room_types = RoomType.objects.all()
    context = {
        'hotel':hotel,
        'room_types':room_types,
    }
    
    return render(request, template, context)



#about view
def about_us(request):
    template ='pages/about.html'
    
    return render(request, template)

#contac view
def contact_us(request):
    template ='pages/contact_us.html'
    
    return render(request, template)

#gallery view
def gallery(request):
    template ='pages/gallery.html'
    
    roomtypes = RoomType.objects.all()
    room_gallery = Room.objects.all()
    
    return render(request, template, {"room":roomtypes, "room_gallery":room_gallery})

def gallery_filter(request, foo):
    template ='pages/gallery.html'
    
    roomtypes = RoomType.objects.all()
    
    foo = foo.replace('-', '')
    rooms = RoomType.objects.get(type=foo)
    room_gallery = Room.objects.filter(room_type=rooms)
    context = {
    "rooms":rooms,
    "room":roomtypes,
    "room_gallery":room_gallery
}

    return render(request, template, context)
    
    
    
    

def all_rooms(request):
    
    template ='pages/roomlist.html'
    hotel = Hotel.objects.filter(status='Live').first()
    
    rooms = Room.objects.all()
    context = {
    'hotel':hotel,
    'rooms': rooms,
     }
    
    return render(request, template, context)


#rooms by category view
def room_list(request,slug):
    
    template ='pages/roomlist.html'
     
    hotel = Hotel.objects.filter(status='Live').first()
   
    room_type = get_object_or_404(RoomType, slug=slug)
    rooms = Room.objects.filter(room_type=room_type)
    amenities = room_type.amenities.all()
  
    
    context = {
     'hotel':hotel,
     'room_type': room_type,
     'rooms': rooms,
     'amenities': amenities
     }
    
    return render(request, template, context)


def room_type_detail(request, slug, rt_slug):
    hotel = get_object_or_404(Hotel, status="Live", slug=slug)
    room_type = get_object_or_404(RoomType, hotel=hotel, slug=rt_slug)
    rooms = Room.objects.filter(room_type=room_type, is_available=True)

    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.warning(request, "Please enter your booking data to check availability.")
        return redirect("booking:booking_data", hotel.slug)

    request.session.pop('booking_data', None)

    room_amenities = [
        {
            'room': room,
            'amenities': RoomInventory.objects.filter(room=room, amenity__isnull=False).select_related('amenity')
        }
        for room in rooms
    ]

    # Calculate total items in the cart
    cart = request.session.get('cart', {})
    total_selected_items = sum(item['quantity'] for item in cart.values())

    context = {
        "hotel": hotel,
        "room_type": room_type,
        "rooms": rooms,
        "room_amenities": room_amenities,
        "checkin": booking_data['checkin'],
        "checkout": booking_data['checkout'],
        "capacity": booking_data['capacity'],
        "id": booking_data['hotel_id'],
        "total_selected_items": total_selected_items,
    }
    return render(request, "pages/room_detail.html", context)





# def selected_rooms(request):
#     #request.session.pop('selection_data_obj', None)
#     total = 0
#     room_count = 0
#     total_days = 0
#     adult = 0 
#     children = 0 
#     checkin = "0" 
#     checkout = "" 
#     children = 0 
  
    
#     if 'selection_data_obj' in request.session:

#         selection_data = request.session['selection_data_obj']
#         print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjSelection Data:", selection_data)  # Print the contents

#         if request.method == "POST":
#             for h_id, item in request.session['selection_data_obj'].items():
                
#                 id = int(item['hotel_id'])
#                 hotel_id = int(item['hotel_id'])

#                 checkin = item["checkin"]
#                 checkout = item["checkout"]
#                 adult = int(item["adult"])
#                 children = int(item["children"])
#                 room_type_ = item["room_type"]
#                 room_id = int(item["room_id"])
                
#                 user = request.user
#                 hotel = Hotel.objects.get(id=id)
#                 room = Room.objects.get(id=room_id)
#                 room_type = RoomType.objects.get(id=room_type_)

                
#             date_format = "%Y-%m-%d"
#             checkin_date = datetime.strptime(checkin, date_format)
#             checout_date = datetime.strptime(checkout, date_format)
#             time_difference = checout_date - checkin_date
#             total_days = time_difference.days

#             # Get and parse full name
#             full_name = request.POST.get("full_name")
#             email = request.POST.get("email")
#             phone = request.POST.get("phone")

#             # Split the full name to first and last names
#             name_parts = full_name.split()
#             first_name = name_parts[0] if name_parts else ""
#             last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

#             # Create the booking
#             booking = Booking.objects.create(
#                 hotel=hotel,
#                 room_type=room_type,
#                 check_in_date=checkin,
#                 check_out_date=checkout,
#                 num_adults=adult,
#                 num_children=children,
#             )

#             if request.user.is_authenticated:
#                 booking.user = request.user
#                 booking.save()
#             else:
#                 user = User.objects.filter(email=email).first() 
                
#                 if not user:
#                     # If user doesn't exist, create a new one
#                     user = User(email=email, username=email)
#                     user.set_password(phone)  # Set phone number as password
#                     user.first_name = first_name
#                     user.last_name = last_name
#                     user.save()
                    
#                     booking.user = user
#                     booking.save()           

#             for h_id, item in request.session['selection_data_obj'].items():
#                 room_id = int(item["room_id"])
#                 room = Room.objects.get(id=room_id)
                
#                 booking = Booking.objects.create(
#                     hotel=hotel,
#                     room_type=room_type,
#                     room=room,  # Assign a single room per booking
#                     check_in_date=checkin,
#                     check_out_date=checkout,
#                     num_adults=adult,
#                     num_children=children,
#                     user=request.user if request.user.is_authenticated else user
#                 )
                
#                 # Add total amount calculations if needed
#                 days = total_days
#                 print('ccccccccccccccccccccccccccccccccccccccccccccccccc', days)
#                 price = room_type.base_price if not room.price_override else room.price_override
#                 total_amount = price * days
#                 print('yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',total_amount)
#                 booking.total_amount = total_amount
#                 booking.save()
                
#                 room_count += 1
#                 total += total_amount
#                 print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd',total)


#             messages.success(request, "Checkout Now!")
#             return redirect("core:checkout", booking.booking_id)

#         hotel = None

#         for h_id, item in request.session['selection_data_obj'].items():
                
#             id = int(item['hotel_id'])
#             hotel_id = int(item['hotel_id'])

#             checkin = item["checkin"]
#             checkout = item["checkout"]
#             adult = int(item["adult"])
#             children = int(item["children"])
#             room_type_ = item["room_type"]
           
#             room_id = int(item["room_id"])
           
#             room_type = RoomType.objects.get(id=room_type_)

#             date_format = "%Y-%m-%d"
#             checkin_date = datetime.strptime(checkin, date_format)
#             checout_date = datetime.strptime(checkout, date_format)
#             time_difference = checout_date - checkin_date
#             total_days = time_difference.days

#             room_count += 1
#             days = total_days
#             price = room_type.base_price

#             room_price = price * room_count
#             total = room_price * days
            
#             hotel = Hotel.objects.get(id=id)

#         print("hotel ===", hotel)
#         context = {
#             "data":request.session['selection_data_obj'], 
#             "total_selected_items": len(request.session['selection_data_obj']),
#             "total":total,
#             "total_days":total_days,
#             "adult":adult,
#             "children":children,   
#             "checkin":checkin,   
#             "checkout":checkout,   
#             "hotel":hotel,   
#             'room_type':room_type,
#         }

#         return render(request, "pages/selected_rooms.html", context)
#     else:
#         messages.warning(request, "You don't have any room selections yet!")
#         return redirect("/")



def checkout(request, booking_id):
    try:
        # Retrieve the booking and the latest payment attempt
        booking = Booking.objects.get(booking_id=booking_id)
        latest_payment = booking.payments.order_by('-date').first()

        # Check if the latest payment was completed
        if latest_payment and latest_payment.status == "completed":
            messages.success(request, "This order has already been paid for!")
            return redirect("/")
        elif latest_payment:
            latest_payment.status = "processing"
            latest_payment.save()

        # Handle coupon application if form is submitted
        now = timezone.now()
        if request.method == "POST":
            code = request.POST.get('code')
            try:
                # Validate and retrieve the coupon
                coupon = Coupon.objects.get(
                    code__iexact=code,
                    valid_from__lte=now,
                    valid_to__gte=now,
                    active=True
                )
                # Check if coupon is already applied to this booking
                if coupon in booking.coupons.all():
                    messages.warning(request, "Coupon already activated for this booking.")
                    return redirect("hotel:checkout", booking_id=booking.id)
                
                # Apply the coupon and create a record in CouponUsers
                CouponUsers.objects.create(
                    booking=booking,
                    coupon=coupon,
                    full_name=booking.full_name,
                    email=booking.email,
                    mobile=booking.phone,
                )
                
                # Calculate and apply the discount based on coupon type
                discount = (booking.total * coupon.discount / 100) if coupon.type == "Percentage" else coupon.discount
                booking.coupons.add(coupon)
                booking.total -= discount
                booking.saved += discount
                booking.save()

                messages.success(request, "Coupon found and activated!")
                return redirect("hotel:checkout", booking_id=booking.id)

            except Coupon.DoesNotExist:
                messages.error(request, "Coupon not found or expired.")
                return redirect("hotel:checkout", booking_id=booking.id)

        # Context for rendering the checkout page
        context = {
            "booking": booking,
            "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
            "flutterwave_public_key": settings.FLUTTERWAVE_PUBLIC,
            "website_address": settings.WEBSITE_ADDRESS,
        }
        return render(request, "pages/checkout.html", context)

    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect("/")


@csrf_exempt
def create_checkout_session(request, booking_id):
    request_data = json.loads(request.body)
    booking = get_object_or_404(Booking, booking_id=booking_id)

    stripe.api_key = settings.STRIPE_PRIVATE_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = booking.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': booking.full_name,
                    },
                    'unit_amount': int(booking.total * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('hotel:success', args=[booking.booking_id])) + "?session_id={CHECKOUT_SESSION_ID}&success_id="+booking.success_id+'&booking_total='+str(booking.total),
        cancel_url=request.build_absolute_uri(reverse('hotel:failed', args=[booking.booking_id]))+ "?session_id={CHECKOUT_SESSION_ID}",
    )

    booking.payment_status = "processing"
    booking.stripe_payment_intent = checkout_session['id']
    booking.save()

    print("checkout_session ==============", checkout_session)
    return JsonResponse({'sessionId': checkout_session.id})


def payment_success(request, booking_id):
    success_id = request.GET.get('success_id')
    booking_total = request.GET.get('booking_total')

    if success_id and booking_total: 
        success_id = success_id.rstrip('/')
        booking_total = booking_total.rstrip('/')
        
        booking = Booking.objects.get(booking_id=booking_id, success_id=success_id)
        
        # Payment Verification
        if booking.total == Decimal(booking_total):
            if booking.payment_status == "processing": #processing #paid
                booking.payment_status = "paid"
                booking.save()

                noti = Notification.objects.create(booking=booking,type="Booking Confirmed",)
                if request.user.is_authenticated:
                    noti.user = request.user
                    noti.save()
                else:
                    noti = None
                    noti.save()

                # Delete the Room Sessions
                if 'selection_data_obj' in request.session:
                    del request.session['selection_data_obj']
                
                # Send Email To Customer
                merge_data = {
                    'booking': booking, 
                    'booking_rooms': booking.room.all(), 
                    'full_name': booking.full_name, 
                    'subject': f"Booking Completed - Invoice & Summary - ID: #{booking.booking_id}", 
                }
                subject = f"Booking Completed - Invoice & Summary - ID: #{booking.booking_id}"
                text_body = render_to_string("email/booking_completed.txt", merge_data)
                html_body = render_to_string("email/booking_completed.html", merge_data)
                
                msg = EmailMultiAlternatives(
                    subject=subject, 
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[booking.email], 
                    body=text_body
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()
                    
            elif booking.payment_status == "paid":
                messages.success(request, f'Your booking has been completed.')
                return redirect("/")
            else:
                messages.success(request, 'Opps... Internal Server Error; please try again later')
                return redirect("/")
                
        else:
            messages.error(request, "Error: Payment Manipulation Detected, This payment have been cancelled")
            booking.payment_status = "failed"
            booking.save()
            return redirect("/")
    else:
        messages.error(request, "Error: Payment Manipulation Detected, This payment have been cancelled")
        booking = Booking.objects.get(booking_id=booking_id, success_id=success_id)
        booking.payment_status = "failed"
        booking.save()
        return redirect("/")
    
    context = {
        "booking": booking, 
        'rooms':booking.room.all(), 
    }
    return render(request, "hotel/payment_success.html", context) 


def payment_failed(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)
    booking.payment_status = "failed"
    booking.save()
                
    context = {
        "booking": booking, 
    }
    return render(request, "hotel/payment_failed.html", context) 


def invoice(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id)

    context = {
        "booking":booking,  
        "room":booking.room.all(),  
    }
    return render(request, "hotel/invoice.html", context)


@csrf_exempt
def update_room_status(request):
    today = timezone.now().date()

    booking = Booking.objects.filter(is_active=True)   
    for b in booking:
        if b.is_active != True:
            if b.check_in_date > today:
                b.is_active = False
                b.save()

                for r in b.room:
                    r.is_available = True
                    r.save()
                

            else:
                b.is_active = True
                b.save()

                for r in b.room:
                    r.is_available = False
                    r.save()
        else:
            if b.check_out_date > today:
                b.is_active = False
                b.save()

                for r in b.room:
                    r.is_available = False
                    r.save()

            else:
                b.is_active = True
                b.save()

                for r in b.room:
                    r.is_available = True
                    r.save()

            

    return HttpResponse(today)