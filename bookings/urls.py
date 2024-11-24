from django.urls import path 
from .import views 

app_name = "booking"

urlpatterns = [
    path("check_room_availability/", views.check_room_availability, name="check_room_availability"),

    path("room/<str:rid>/", views.selected_room, name="selected_room"),
    path("booking_data/<slug:slug>/", views.booking_data, name="booking_data"),
    path("create-reservation/", views.create_reservation, name="create_reservation"),

    
    #htmx
    # path('update-booking-summary/<str:rid>/', views.update_booking_summary, name='update_booking_summary'),
    
]