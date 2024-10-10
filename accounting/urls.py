from django.urls import path
from . import views

app_name = "accounting"


urlpatterns = [
    #accounting
    
    path('dasboard/bookings/payments/',views.booking_payments_list, name="booking_payments"),
    path('dasboard/pos/payments/',views.pos_payments_list, name="pos_payments"),
]