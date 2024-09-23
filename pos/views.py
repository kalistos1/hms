
from .models import *
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from uuid import uuid4
from django.db import transaction
from accounts.models import User  
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist



def pos_index(request, slug=None):
    categories = ProductCategory.objects.all()
    cart = get_user_cart(request)
    total_items = cart.total_items

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
    
    # Render the cart checkout page
    html = render_to_string('partials/htmx/_cart_checkout.html', {'cart': cart})
    return HttpResponse(html)



# @transaction.atomic
# def process_checkout(request):
    
#     customer = None
#     if request.method == 'POST':
#         # Extract form data from the request
#         email = request.POST.get('email')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         phone_number = request.POST.get('phone_number')
#         payment_method = request.POST.get('payment_method')
#         cart_id = request.POST.get('cart_id')
      
#         try:
            
#             # user = User.objects.get(email=email)
#             user = User.objects.filter(email=email).first() 
#         except ObjectDoesNotExist:
#             password = make_password(phone_number) 
#             user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=password)
#             # Create a new customer associated with the new user
#             customer = Customer.objects.create(user=user)
        
#         # Fetch the cart using cart_id
#         cart = Cart.objects.get(id=cart_id)
#         cart_items = CartItem.objects.filter(cart=cart)
        
#         # Create the order for the customer
      
#         order = Order.objects.create(
#             customer=customer,
#             total_amount=cart.total_amount,  # Based on cart total
#             order_status='PENDING',  # Default status
#             room_charge=True if payment_method == 'ROOM_CHARGE' else False
#         )

#         # Create the order items for each item in the cart
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.price
#             )
#             # Update stock quantity of the product
#             item.product.stock_quantity -= item.quantity
#             item.product.save()

#         # Handle payment based on the payment method
#         payment_status = 'PAID' if payment_method in ['CASH', 'CARD'] else 'UNPAID'
#         Payment.objects.create(
#             order=order,
#             payment_method=payment_method,
#             amount_paid=order.total_amount,
#             payment_status=payment_status
#         )

#         # Clear the cart after checkout
#         cart_items.delete()

#         # Send a success response using HTMX
#         return JsonResponse({
#             'status': 'success',
#             'message': 'Checkout completed successfully!',
#             'order_id': order.id
#         })

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.http import JsonResponse

@transaction.atomic
def process_checkout(request):
    customer = None
    
    if request.method == 'POST':
        # Extract form data from the request
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        payment_method = request.POST.get('payment_method')
        cart_id = request.POST.get('cart_id')

        # Fetch or create the user
        user = User.objects.filter(email=email).first()

        if user:
            # If user exists, create a new Customer linked to this User
            customer = Customer.objects.create(user=user)
        else:
            # Create a new User if it doesn't exist
            password = make_password(phone_number)  # Use phone number as the password
            user = User.objects.create(
                email=email,
                username=email,  # Set email as the username
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            # Create a new Customer associated with the new User
            customer = Customer.objects.create(user=user)

        # Fetch the cart using cart_id
        cart = Cart.objects.get(id=cart_id)
        cart_items = CartItem.objects.filter(cart=cart)

        # Create the order for the customer
        order = Order.objects.create(
            customer=customer,
            total_amount=cart.total_amount,  # Based on cart total
            order_status='PENDING',  # Default status
            room_charge=True if payment_method == 'ROOM_CHARGE' else False
        )

        # Create the order items for each item in the cart
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
            # Update stock quantity of the product
            item.product.stock_quantity -= item.quantity
            item.product.save()

        # Handle payment based on the payment method
        payment_status = 'PAID' if payment_method in ['CASH', 'CARD'] else 'UNPAID'
        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount_paid=order.total_amount,
            payment_status=payment_status
        )

       
        cart_items.delete()

        # Send a success response using HTMX
        return JsonResponse({
            'status': 'success',
            'message': 'Checkout completed successfully!',
            'order_id': order.id
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


def cart_view(request):
    cart = get_user_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})



def update_cart_total(request):
    cart = get_user_cart(request)
    html = render_to_string('partials/htmx/_cart_total.html', {'cart': cart})
    return HttpResponse(html)
