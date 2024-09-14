from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from accounts.models import User


class EventType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True)
    organizer_name = models.CharField(max_length=255)
    organizer_email = models.EmailField()
    organizer_phone = models.CharField(max_length=20, null=True, blank=True)
    rooms = models.ManyToManyField('Hall', related_name='events')
    services = models.ManyToManyField('Service', related_name='events', blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=50, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], blank=True, null=True)
    end_recurrence = models.DateTimeField(blank=True, null=True)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def calculate_profit(self):
        self.profit = self.total_revenue - self.total_expenses
        self.save()

    def apply_discount(self):
        if self.coupon and self.coupon.is_valid():
            discount = self.total_revenue * (self.coupon.discount_percentage / 100)
            self.total_revenue -= discount
            self.save()

    def __str__(self):
        return self.name


class EventImage(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='event_image/')
    image2 = models.ImageField(upload_to='event_image/')


class EventAgenda(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=120)
    speaker_name = models.CharField(max_length=120)
    start_time = models.TimeField()
    end_time = models.TimeField()
    venue_name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
#Manages rooms that can be booked for events.
class Hall(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seasonal_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, validators=[MinValueValidator(0.1), MaxValueValidator(5.0)])
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"
    

# Manages additional services that the hotel can offer for events (e.g., catering, decoration).
class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


#Handles predefined packages that combine services and rooms for specific event types (e.g., weddings, conferences).
class EventPackage(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    services = models.ManyToManyField(Service, related_name='packages')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
    
class Attendee(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendees')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    rsvp_status = models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')])
    meal_preference = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} for {self.event.name}"
    
  
 #Automates sending notifications to organizers and attendees for important updates or reminders.   
class EventNotification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='notifications')
    notification_time = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def send_notification(self):
        # Logic to send email/SMS notifications
        pass

    def __str__(self):
        return f"Notification for {self.event.name}"
    
    
class StaffAssignment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='staff_assignments')
    staff_member = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you're using Django's User model for staff
    role = models.CharField(max_length=100)
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.staff_member.username} assigned to {self.event.name} as {self.role}"


class EventFeedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='feedback')
    attendee = models.ForeignKey(Attendee, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comments = models.TextField(blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.event.name} by {self.attendee}"
    
    
    
class EventCustomization(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, related_name='customization')
    theme_color = models.CharField(max_length=7, help_text="Hex color code for event theme")
    custom_requests = models.TextField(blank=True, null=True)  # Store special requests or instructions

    def __str__(self):
        return f"Customization for {self.event.name}"
    
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    def is_valid(self):
        return self.valid_from <= timezone.now() <= self.valid_to

    def __str__(self):
        return self.code