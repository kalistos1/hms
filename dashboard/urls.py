from django.urls import path
from . import views


app_name = "dashboard"

urlpatterns = [
    #dshboards
    
    path('admin_dash/',views.admin_dashboard, name="admin_dashboard"),
    path('supervisor_dash/',views.supervisor_dashboard, name ="supervisor_dashboard"),
    path('account_dash/',views.account_dashboard, name ="account_dashboard"),
    path('front_desk_dash/',views.frontdesk_dashboard, name ="frontdesk_dashboard"),
    
    #frontdesk
    path('front_desk/room_status/',views.frontdesk_room_status, name ="frontdesk_room_status"),
    path('front_desk/booking_list/',views.frontdesk_booking_list, name ="frontdesk_booking_list"),
    path('front_desk/check_in_out/',views.frontdesk_room_checkout, name ="frontdesk_room_checkout"),
    path('front_desk/book_room/',views.frontdesk_room_book, name ="book_room"),
    
    
    
]
