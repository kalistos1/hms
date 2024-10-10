from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from bookings.models import Payment as BookingPayment
from pos.models import PosPayment

# Create your models here.

    
class PaymentRecord(models.Model):
    PAYMENT_STATUS_CHOICES = [
       ('pending', 'Pending'),
        ('advance', 'Advance'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    PAYMENT_SOURCE_CHOICES = [
        ('booking', 'Booking'),
        ('event', 'Event'),
        ('pos', 'POS'),
    ]
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='uncompleted')
    source = models.CharField(max_length=50, choices=PAYMENT_SOURCE_CHOICES)
    booking_payment = models.ForeignKey('bookings.Payment', null=True, blank=True, on_delete=models.SET_NULL)
    pos_payment = models.ForeignKey('pos.PosPayment', null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.get_source_display()} Payment - {self.amount}"
