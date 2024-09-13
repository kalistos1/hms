from django.db import models
from bookings.models import  Booking, RoomType, Coupon
from accounts.models import User
from django.utils.text import slugify
from django.utils import timezone


class Interaction(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_interactions')
    INTERACTION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('in_person', 'In-Person'),
    ]
    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPE_CHOICES)
    interaction_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    staff = models.ForeignKey(User,on_delete=models.CASCADE, related_name='staff_interactions')

    class Meta:
        indexes = [
            models.Index(fields=['interaction_date']),
        ]

    def __str__(self):
        return f"Interaction with {self.guest.first_name} on {self.interaction_date}"

class LoyaltyProgram(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loyalty_programs')
    points = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    transaction_date = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['transaction_date']),
        ]

    def __str__(self):
        return f"Loyalty points for {self.guest.first_name}: {self.points} points"

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    target_audience = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError("End date must be after start date.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GuestFeedback(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='feedbacks')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True, null=True)
    feedback_date = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [
            models.Index(fields=['feedback_date']),
        ]
        unique_together = ('guest', 'booking')

    def __str__(self):
        return f"Feedback from {self.guest.first_name} - {self.rating} stars"




class ReservationHistory(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation_histories')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='reservation_histories')
    reservation_date = models.DateTimeField(default=timezone.now)
    action_type = models.CharField(max_length=50, choices=[('booking', 'Booking'), ('cancellation', 'Cancellation')])
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['reservation_date']),
        ]

    def __str__(self):
        return f"History for {self.guest.first_name} - {self.action_type}"

class SpecialRequest(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='special_requests')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='special_requests')
    request = models.TextField()
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"Request from {self.guest.first_name} - Fulfilled: {self.fulfilled}"


class GuestSegment(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    description = models.TextField(blank=True, null=True)
    guests = models.ManyToManyField(User, related_name='segments')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Notification(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[('email', 'Email'), ('sms', 'SMS')])
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['sent_at']),
        ]

    def __str__(self):
        return f"Notification for {self.guest.first_name} - {self.notification_type}"


class RoomPricing(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='pricing')
    season = models.CharField(max_length=50, blank=True, null=True)  # e.g., High, Low, Holiday
    demand_factor = models.DecimalField(max_digits=5, decimal_places=2)  # Factor to multiply base price
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.room_type} - {self.season}"
    

class GuestPreference(models.Model):
    guest = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    preferred_bed_type = models.CharField(max_length=50, choices=[('single', 'Single'), ('double', 'Double')], blank=True, null=True)
    preferred_view = models.CharField(max_length=50, choices=[('sea', 'Sea View'), ('city', 'City View')], blank=True, null=True)
    room_floor_preference = models.CharField(max_length=50, choices=[('low', 'Low Floor'), ('high', 'High Floor')], blank=True, null=True)
    other_preferences = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Preferences for {self.guest.first_name}"
    

class Referral(models.Model):
    referrer = models.ForeignKey(User, related_name='referrals', on_delete=models.CASCADE)
    referred_guest = models.ForeignKey(User, related_name='referred_by', on_delete=models.CASCADE)
    reward_earned = models.BooleanField(default=False)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    referral_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Referral by {self.referrer.first_name} for {self.referred_guest.first_name}"


class AbandonedBooking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='abandoned_bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='abandoned_bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    abandonment_date = models.DateTimeField(default=timezone.now)
    reason = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['abandonment_date']),
        ]

    def __str__(self):
        return f"Abandoned Booking by {self.guest.first_name} - {self.room_type.name}"


class ServiceUsage(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.CharField(max_length=255)  # e.g., 'Spa', 'Room Service'
    usage_date = models.DateTimeField(auto_now_add=True)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.guest.first_name} used {self.service}"

class Analytics(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    bookings_count = models.PositiveIntegerField(default=0)
    avg_booking_value = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.guest.first_name}"

class Survey(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    survey_name = models.CharField(max_length=255)
    questions = models.TextField()  # Optionally, use a related Question model for more complex survey structure
    response = models.TextField(blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Survey for {self.guest.first_name} - {self.survey_name}"


class GuestLifetimeValue(models.Model):
    guest = models.OneToOneField(User, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    lifetime_value = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def update_lifetime_value(self):
        # Custom method to update lifetime value based on total_revenue
        self.lifetime_value = self.total_revenue * 1.2  # Example calculation
        self.save()

    def __str__(self):
        return f"Lifetime Value for {self.guest.first_name}: {self.lifetime_value}"