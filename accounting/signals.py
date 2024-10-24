from accounting.models import PaymentRecord
from bookings.models import Payment, PaymentCompletion
from pos.models import PosPayment
from django.db.models.signals import post_save
from django.dispatch import receiver

# Handle Payment creation (for pending and advance payments)

@receiver(post_save, sender=Payment)
def create_or_update_payment_record(sender, instance, created, **kwargs):
    """
    Create or update a PaymentRecord when a payment is made or updated (advance or pending).
    """
    if instance.status in ['pending', 'advance']:
        payment_record, created = PaymentRecord.objects.get_or_create(
            booking_payment=instance,
            defaults={
                'amount': instance.amount,
                'payment_date': instance.date,
                'status': 'uncompleted',
                'source': 'booking',
                'description': f" Booking Payment ID: {instance.transaction_id}",
            }
        )

        if not created:
            # Update the existing payment record if it's not a new one
            payment_record.amount += instance.amount  # Increment the amount for subsequent advances
            payment_record.save()
            

# Handle PaymentCompletion (for completed payments)
@receiver(post_save, sender=PaymentCompletion)
def mark_payment_as_completed(sender, instance, **kwargs):
    """
    Update the PaymentRecord when a payment is fully completed.
    """
    # Find the corresponding PaymentRecord for the booking payment
    payment_record = PaymentRecord.objects.filter(booking_payment=instance.payment).first()

    if payment_record:
        # Update the status to 'completed' and add the completed amount
        payment_record.amount += instance.amount  # Add the completed amount to the total
        payment_record.status = 'completed'
      
        payment_record.save()
    else:
        # If no record exists, create a new one for completed payment
        PaymentRecord.objects.create(
            amount=instance.amount,
            payment_date=instance.completion_date,
            status='completed',
            source='booking',
            booking_payment=instance.payment,
            description=f"Booking Payment ID: {instance.payment.transaction_id}"
        )

# Handle POS Payment creation
@receiver(post_save, sender=PosPayment)
def create_pos_payment_record(sender, instance, created, **kwargs):
    """
    Create a PaymentRecord for POS payments.
    """
    if created:
        PaymentRecord.objects.create(
            amount=instance.amount_paid,
            payment_date=instance.payment_date,
            status='completed',
            source='pos',
            pos_payment=instance,
            description=f"POS Transaction ID: {instance.transaction_id}"
        )
