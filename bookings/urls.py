from django.urls import path 
from .import views 

app_name = "booking"

urlpatterns = [
    path("check_room_availability/", views.check_room_availability, name="check_room_availability"),
    # path("delete_session/", views.delete_session, name="delete_session"),
    path("booking_data/<slug:slug>/", views.booking_data, name="booking_data"),
    path('add-to-booking-cart/', views.add_room_to_cart, name='add_booking_to_cart'),

    # Ajax
    # path("add_to_selection/", views.add_to_selection, name="add_to_selection"),
    # path("delete_selection/", views.delete_selection, name="delete_selection"),
    
]