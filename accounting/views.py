from django.shortcuts import render
from .models import PaymentRecord


def booking_payments_list(request):
    booking_payments = PaymentRecord.objects.filter(source='booking').order_by('-payment_date')
    context = {
        'booking_payments': booking_payments,
    }

    return render(request, 'account_officer/booking_payment_list.html', context)



def pos_payments_list(request):
    pos_payments = PaymentRecord.objects.filter(source='pos').order_by('-payment_date')
    context = {
        'pos_payments': pos_payments,
    }

    return render(request, 'account_officer/pos_payment_list.html', context)