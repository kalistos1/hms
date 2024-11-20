from django.urls import path
from .import views

app_name ="pos"

urlpatterns = [
    
]

htmx_views =[
    path('ordering/',  views.pos_index, name='products'),
    path('products/<slug:slug>/', views.category_products_view, name='category-products'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:item_id>/', views.increase_item_quantity, name='increase_item_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_item_quantity, name='decrease_item_quantity'),
    path('cart/update-total/', views.update_cart_total, name='update_cart_total'),
    path('cart/checkout/', views.checkout_view, name='checkout_view'),
    path('cart/process/', views.process_checkout, name='process_checkout'),
    path('cart/receipt/<int:order_id>/', views.print_receipt, name='print_receipt'),
]

urlpatterns += htmx_views