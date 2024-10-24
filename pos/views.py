
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from uuid import uuid4
from django.db import transaction
from accounts.models import User  
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from hrm .models import *
from .forms import  updateReceivedItemForm, WaiterCheckoutForm
from django.contrib import messages
from django.urls import reverse
from django.utils.html import escape



def pos_index(request, slug=None):
    
    categories = ProductCategory.objects.all()
    cart = get_user_cart(request)
    total_items = cart.total_items
    
    try: 
        pos_user_location = request.user.employee_profile.department_location
        if slug:
            category = get_object_or_404(ProductCategory, slug=slug)
            products = Product.objects.filter(category=category, department_location=pos_user_location)
        else:
            products = Product.objects.filter(department_location=pos_user_location)

    except:
    # Load all products 
        if slug:
            category = get_object_or_404(ProductCategory, slug=slug)
            products = Product.objects.filter(category=category)
        else:
            products = Product.objects.all() 
   
    context = {
        'categories': categories,
        'products': products,
        'current_slug': slug,
        'cart': cart,
        'total_items': total_items,
    }
    return render(request, 'pages/pos_index.html', context)


# HTMX view to load products based on category
def category_products_view(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'partials/htmx/product_list.html', {'products': products})


# views.py
def get_user_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart



def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_user_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, price=product.price)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    html = render_to_string('partials/htmx/_cart_sidebar.html', {'cart': cart})
    return HttpResponse(html)



def increase_item_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()

    html = render_to_string('partials/htmx/_cart_sidebar.html', {'cart': item.cart})
    return HttpResponse(html)




def decrease_item_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity -= 1
    if item.quantity < 1:
        item.delete()
        html = render_to_string('partials/htmx/_cart_sidebar.html', {'cart': item.cart})
        return HttpResponse(html)

    item.save()
    html = render_to_string('partials/htmx/_cart_sidebar.html', {'cart': item.cart})
    return HttpResponse(html)



def checkout_view(request):
    cart = get_user_cart(request)
    current_user = request.user
    department_location = None
    waiter_form = None

    # Determine if the user is a customer or privileged user
    if not current_user.is_admin and not current_user.is_supervisor and \
       not current_user.is_account_officer and not current_user.is_frontdesk_officer and \
       not current_user.is_pos_officer and not current_user.is_worker:
        is_customer = True
    else:
        is_customer = False
        # Check if they are employee/users with valid schedules and attendance
        if hasattr(current_user, 'employee_profile'):
            try:
                pos_user = current_user.employee_profile
            except AttributeError:
                return HttpResponse('<div style="padding:20px;"><p style="color:red; font-weight:bold; font-size:14px;" class="alert alert-danger alert-dismissible fade show" role="alert"> You have not been given permission to work as a POS Officer </p></div>')

            department_location = current_user.employee_profile.department_location
            now = timezone.now()

            # Check if the employee has a valid schedule for either 'Pos_shift' or 'Waiter_shift'
            pos_schedule = StaffSchedules.objects.filter(
                employee=pos_user,
                schedule_type__in=['Pos_shift', 'Waiter_shift'],  # Include both 'Pos_shift' and 'Waiter_shift'
                schedule_start_date__lte=now.date(),
                schedule_end_date__gte=now.date(),
                active=True
            ).first()
         

            if pos_schedule and pos_schedule.start_time <= now.time() <= pos_schedule.end_time:

                # Check if the POS user has checked in for attendance
                attendance = Attendance.objects.filter(
                    employee=pos_user,
                    active=True,
                    check_in__date=now.date()
                ).first()
               
 
                if attendance:
                    # The POS user has a valid schedule and is checked in, display the waiter form
                    if request.method == 'POST':
                        waiter_form = WaiterCheckoutForm(request.POST, department_location=department_location)
                        if waiter_form.is_valid():
                            waiter = waiter_form.cleaned_data['waiter']
                            # Handle waiter selection for the checkout process
                    else:
                        waiter_form = WaiterCheckoutForm(department_location=department_location)
            else:
                print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')

    # Render the cart checkout page along with the waiter form (if applicable)
    html = render_to_string('partials/htmx/_cart_checkout.html', {
        'cart': cart,
        'waiter_form': waiter_form if not is_customer else None  # Display the form only if not a customer
    })
    
    return HttpResponse(html)
   

@transaction.atomic
def process_checkout(request):
   

    if request.method == 'POST':
        # Extract form data
        payment_method = request.POST.get('payment_method')
        cart_id = request.POST.get('cart_id')
        waiter_id = request.POST.get('waiter')
        # waiter = None
        
        # Validate POSUser's schedule and check-in status
        pos_user = request.user.employee_profile
        now = timezone.now()

        # Check if the POS user is within their scheduled shift
        pos_schedule = StaffSchedules.objects.filter(
            employee=pos_user,
            schedule_type='Pos_shift',
            schedule_start_date__lte=now.date(),
            schedule_end_date__gte=now.date(),
            active=True
        ).first()

        if not pos_schedule:
            return JsonResponse({'status': 'error', 'message': 'You are not scheduled for a shift currently.'}, status=403)

        # Check if the current time is within their scheduled shift hours
        if not (pos_schedule.start_time <= now.time() <= pos_schedule.end_time):
            return JsonResponse({'status': 'error', 'message': 'You are not within your scheduled hours.'}, status=403)

        # Check if the POS user has checked in
        attendance = Attendance.objects.filter(
            employee=pos_user,
            active=True,
            check_in__date=now.date()
        ).first()

        if not attendance:
            return JsonResponse({'status': 'error', 'message': 'You must check in to start processing orders.'}, status=403)

        waiter = None
        if waiter_id:
            waiter = Employee.objects.filter(id=waiter_id).first()  # Get the POSUser instance

        # Handle the Waiter form
        if 'waiter' in request.POST:
            waiter_form = WaiterCheckoutForm(request.POST)
            if waiter_form.is_valid():
                waiter = waiter_form.cleaned_data['waiter']

        # Create an anonymous customer
        try:
            anonymous_customer_count = PosCustomer.objects.filter(name__startswith="Customer").count()
            customer_name = f"Customer{anonymous_customer_count + 1}"
        except:
            customer_name = f"Customer"

        customer = PosCustomer.objects.create(customer_name= customer_name, pos_customer=True,customer_room_number=0)

        # Fetch the cart and items
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = cart.total_amount


        # Create the Order with both POSUser and Waiter
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount,
            order_status='PENDING',
            room_charge=(payment_method == 'ROOM_CHARGE'),
            staff=pos_user,
            waiter=waiter  # Add waiter if applicable
        )

        # Create OrderItems and adjust product stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
            item.product.stock_quantity -= item.quantity
            item.product.save()

        # Process payment
        payment_status = 'PAID' if payment_method in ['CASH', 'CARD'] else 'UNPAID'
        PosPayment.objects.create(
            order=order,
            payment_method=payment_method,
            amount_paid=total_amount,
            payment_status=payment_status
        )

        # Update order status if payment is completed
        if payment_status == 'PAID':
            order.order_status = 'COMPLETED'
            order.save()

        # Clear the cart after processing
        cart_items.delete()
        
        messages.success(request, 'Checkout completed successfully!')

        # Create an HttpResponse to tell HTMX to redirect to the pos:products page
        response = HttpResponse()
        response['HX-Redirect'] = reverse('pos:products')

        return response

    return HttpResponse('Invalid request method', status=400)



def cart_view(request):
    cart = get_user_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})



def update_cart_total(request):
    cart = get_user_cart(request)
    html = render_to_string('partials/htmx/_cart_total.html', {'cart': cart})
    return HttpResponse(html)
