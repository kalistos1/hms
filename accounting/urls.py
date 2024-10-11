from django.urls import path
from . import views

app_name = "accounting"


urlpatterns = [
    #accounting
    
    path('dasboard/bookings/payments/',views.booking_payments_list, name="booking_payments"),
    path('dasboard/pos/payments/',views.pos_payments_list, name="pos_payments"),
    path('dasboard/pos_booking/reports/',views.payment_report_view, name="payment_reports"),
    path('dasboard/purchase/reports/',views.purchase_report, name="purchase_reports"),
     
]