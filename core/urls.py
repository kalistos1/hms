from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    
    #frontpages
    path ('', views.index, name="index"),
    path ('about/', views.about_us, name="about"),
    path ('contact_us/', views.contact_us, name="contact"),
    path ('gallery/', views.gallery, name="gallery"),
    path ('room_list/', views.all_rooms, name="all_rooms"),
    path('roomtype/room_list/<slug:slug>/', views.room_list, name='room_type_list'),
    path("detail/<slug:slug>/room-type/<slug:rt_slug>/", views.room_type_detail, name="room_type_detail"),
    
    path("checkout/<booking_id>/", views.checkout, name="checkout"),
    path("invoice/<booking_id>/", views.invoice, name="invoice"),
    
    path("selected_rooms/", views.selected_rooms, name="selected_rooms"),
    path("update_room_status/", views.update_room_status, name="update_room_status"),
    
        # Payment API
    path('api/checkout-session/<booking_id>/', views.create_checkout_session, name='api_checkout_session'),
    path('success/<booking_id>/', views.payment_success, name='success'),
    path('failed/<booking_id>/', views.payment_failed, name='failed'),
    
]
