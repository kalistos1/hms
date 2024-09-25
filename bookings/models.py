

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import escape
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
from django.utils import timezone
from django_countries.fields import CountryField
import shortuuid
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.db import transaction




ICON_TPYE = (
    ('Bootstap Icons', 'Bootstap Icons'),
    ('Fontawesome Icons', 'Fontawesome Icons'),
)


RATING = (
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
)

class Hotel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = CKEditor5Field(config_name='extends', null=True, blank=True)
    image = models.FileField(upload_to="hotel_gallery")
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    status = models.CharField( max_length=10, default="Live", null=True, blank=True)
    tags = TaggableManager(blank=True)
    views = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False)
    hid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    slug = models.SlugField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.name) + "-" + str(uniqueid.lower())
            
        super(Hotel, self).save(*args, **kwargs) 

    def thumbnail(self):
        return mark_safe('<img src="%s" width="50" height="50" style="object-fit:cover; border-radius: 6px;" />' % (self.image.url))

    def hotel_gallery(self):
        return HotelGallery.objects.filter(hotel=self)
    
    def hotel_features(self):
        return HotelFeatures.objects.filter(hotel=self)

    def hotel_faqs(self):
        return HotelFAQs.objects.filter(hotel=self)

    def hotel_room_types(self):
        return RoomType.objects.filter(hotel=self)
    
    def average_rating(self):
        average_rating = Review.objects.filter(hotel=self, active=True).aggregate(avg_rating=models.Avg("rating"))
        return average_rating['avg_rating']
    
    def rating_count(self):
        rating_count = Review.objects.filter(hotel=self, active=True).count()
        return rating_count
 
 
    
class HotelGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image = models.FileField(upload_to="hotel_gallery")
    hgid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return str(self.hotel)

    class Meta:
        verbose_name_plural = "Hotel Gallery"
    


class HotelFeatures(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    icon_type = models.CharField(max_length=100, null=True, blank=True, choices=ICON_TPYE)
    icon = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    hfid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return str(self.hotel)
    
    class Meta:
        verbose_name_plural = "Hotel Features"
  
  
    
class HotelFAQs(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    hfid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return str(self.hotel)
    
    class Meta:
        verbose_name_plural = "Hotel FAQs"
     
        
class RoomAmenity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
       
       
        
class RoomType(models.Model):
    
    ROOM_TYPES = (
        ('Delux', 'Delux'),
        ('Executive', 'Executive'),
        ('Presidential', 'Presidential'),
        
    )

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    banner_img = models.ImageField(upload_to="room_type", null=True, blank=True)
    type = models.CharField(max_length=20, choices = ROOM_TYPES, null=True, blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    number_of_beds = models.PositiveIntegerField(default=0)
    room_capacity = models.PositiveIntegerField(default=0)
    rtid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    slug = models.SlugField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type}"

    def rooms_count(self):
        return Room.objects.filter(room_type=self).count()

    def save(self, *args, **kwargs):
        if not self.slug:
            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]
            self.slug = slugify(self.type) + "-" + str(uniqueid.lower())
        super(RoomType, self).save(*args, **kwargs)
        
               
        
class Room(models.Model):
    FLOOR = (
        ('ground_floor', 'Ground Floor'),
        ('first_floor', 'First Floor'),
        ('second_floor', 'Second Floor'),
    )
    
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    banner_img = models.ImageField(upload_to="rooms", null=True, blank=True)
    room_number = models.CharField(max_length=10)
    floor = models.CharField(max_length=20, choices=FLOOR, default='ground_floor')
    price_override = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    rid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)
    amenities = models.ManyToManyField(RoomAmenity, blank=True)  # Added field

    def __str__(self):
        return f"{self.room_type.type} - Room {self.room_number}"

    def price(self):
        return self.price_override if self.price_override is not None else self.room_type.base_price

    def number_of_beds(self):
        return self.room_type.number_of_beds

    def save(self, *args, **kwargs):
        # Validation to ensure price_override is not negative
        if self.price_override is not None and self.price_override < 0:
            raise ValidationError("Price override cannot be negative.")
        
        super(Room, self).save(*args, **kwargs)



class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'pending'),
        ('advance', 'advance'),
        ('completed', 'completed'),
        ('failed', 'Failed'),
        ('refunded', 'refunded'),
    ]
    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    ]
    
    booking = models.ForeignKey('Booking', related_name='payments', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='cash')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    date = models.DateTimeField(auto_now_add=True)
    transaction_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"

    def get_total_due(self):
        total_booking = self.booking.calculate_total()
        total_paid = self.booking.payments.filter(status='advance').aggregate(total=models.Sum('amount'))['total'] or 0
        return total_booking - total_paid
        
    def are_rooms_available(self, rooms, check_in_date, check_out_date):
        """
        Check if all the specified rooms are available for the selected date range
        in an atomic way using select_for_update to prevent race conditions.
        Returns True if all rooms are available, otherwise False.
        """
        with transaction.atomic():
            for room in rooms:
                # Lock the room rows to avoid race conditions
                locked_room = Room.objects.select_for_update().get(id=room.id)
                
                # Check if the room has any overlapping active bookings
                overlapping_bookings = Booking.objects.filter(
                    room=locked_room,
                    is_active=True,
                    check_in_date__lt=check_out_date,
                    check_out_date__gt=check_in_date
                ).exists()
                
                if overlapping_bookings:
                    return False, locked_room  # Return the specific room that's not available
                
        return True, None
    
    def save(self, *args, **kwargs):
        # Check if payment is marked as advance
        if self.status == 'advance':
            # Update room availability to false (unavailable)
            self.booking.update_room_availability(False)
            self.booking.set_checked_in()

        super(Payment, self).save(*args, **kwargs)


class PaymentCompletion(models.Model):

    PAYMENT_MODE_CHOICES = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
    ]
    
    payment = models.OneToOneField(Payment, related_name='completion', on_delete=models.CASCADE)
    completion_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='cash')
    transaction_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Completion for Payment {self.payment.transaction_id} - {self.transaction_id}"



class Refund(models.Model):
    REFUND_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    
    payment = models.ForeignKey(Payment, related_name='refunds', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=REFUND_STATUS_CHOICES, default='pending')
    transaction_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund {self.transaction_id} - {self.status} - ${self.amount}"

    def clean(self):
        # Ensure that the refund amount does not exceed the payment amount
        total_refunded = self.payment.refunds.aggregate(total=models.Sum('amount'))['total'] or 0
        if self.amount > (self.payment.amount - total_refunded):
            raise ValidationError("Refund amount exceeds the remaining payment balance.")

    def save(self, *args, **kwargs):
        # Call the clean method to validate before saving
        self.clean()
        super(Refund, self).save(*args, **kwargs)



class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True)
    room = models.ManyToManyField('Room')  # This can be used for both bookings and reservations
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def calculate_total(self):
        additional = self.additional_charges.aggregate(total=models.Sum('amount'))['total'] or 0
        return self.total_amount + additional

    def __str__(self):
        return f" {self.room_type.type} Transaction"
    
    

class Reservation(Transaction):
    reservation_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    expiration_date = models.DateTimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    cancel_date = models.DateTimeField(null=True, blank=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Reservation {self.reservation_id} by {self.user.username if self.user else 'Guest'}"
    
    def cancel_reservation(self):
        if not self.expiration_date:
            raise ValueError("Expiration date is not set.")
        
        # Check if the current time is past the expiration date and payment status is pending
        if not self.is_cancelled and self.payment and self.payment.status == "pending" and timezone.now() > self.expiration_date:
            self.is_cancelled = True
            self.cancel_date = timezone.now()
            self.save()

    def save(self, *args, **kwargs):
        # Set a default expiration date if it's not provided
        if not self.expiration_date:
            self.expiration_date = self.date_created + timezone.timedelta(days=3)
        super(Reservation, self).save(*args, **kwargs)



class Booking(Transaction):
    booking_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    is_active = models.BooleanField(default=True)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    reservation = models.OneToOneField('Reservation', on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username if self.user else 'Guest'}"

  
    def apply_coupon(self, coupon):
        """Apply a valid coupon and calculate the final amount."""
        if coupon and coupon.active and coupon.valid_from <= timezone.now().date() <= coupon.valid_to:
            print(f"Applying coupon: {coupon.code} with discount type: {coupon.type} and discount: {coupon.discount}")
            if coupon.type == 'Percentage':
                discount_amount = (self.total_amount * coupon.discount) / 100
               
            else:  # Fixed amount discount
                discount_amount = coupon.discount

            self.total_amount -= min(discount_amount, self.total_amount)  # Ensure discount doesn't exceed total
            self.coupon = coupon
            self.save()


    def get_discount_amount(self):
        """Calculate the discount amount based on the coupon."""
        if self.coupon:
            total_payable = self.get_total_payable()
            discount_value = self.coupon.discount  # Accessing the discount field
            return float(total_payable) * (discount_value / 100)  # Assuming discount is a percentage
        return 0

    def get_total_payable_after_discount(self):
        """Get the total payable after applying the coupon discount."""
        total_payable = self.get_total_payable()
        discount_amount = self.get_discount_amount()
        print(f"Total Payable: {total_payable}, Discount Amount: {discount_amount}")
        return float(total_payable) - float(discount_amount)

    def convert_reservation_to_booking(self, reservation):
        """Convert a reservation into a booking and optionally apply a coupon if one exists."""
        self.user = reservation.user
        self.hotel = reservation.hotel
        self.room_type = reservation.room_type
        self.room.set(reservation.room.all())  # Copy the rooms from the reservation
        self.check_in_date = reservation.check_in_date
        self.check_out_date = reservation.check_out_date
        self.num_adults = reservation.num_adults
        self.num_children = reservation.num_children
        self.reservation = reservation
        self.total_amount = reservation.total_amount

        # Apply coupon if any exists in the reservation
        if reservation.payment and reservation.payment.booking.coupon:
            self.coupon = reservation.payment.booking.coupon  # Copy the coupon from the reservation if it exists
        
        self.save()
        
        
    def are_rooms_available(self, rooms, check_in_date, check_out_date):
        """
        Check if all the specified rooms are available for the selected date range.
        Returns True if all rooms are available, otherwise False.
        """
        for room in rooms:
            overlapping_bookings = Booking.objects.filter(
                room=room,
                is_active=True,
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).exclude(id=self.id)  # Exclude the current booking to avoid checking itself
            if overlapping_bookings.exists():
                return False, room  # Return the specific room that's not available
        return True, None

        
    def save(self, *args, **kwargs):
        # If it's a new booking (i.e., no primary key assigned yet)
        if not self.pk:
            # Save the booking to generate the primary key (id)
            super(Booking, self).save(*args, **kwargs)

        # Now that the booking has an id, check room availability
        available, unavailable_room = self.are_rooms_available(self.room.all(), self.check_in_date, self.check_out_date)
        if not available:
            raise ValueError(f"Room {unavailable_room.room_number} is not available for the selected dates.")

        # Ensure that the booking's total amount is calculated
        self.total_amount = self.get_total_payable_after_discount()

        # Save again to update the fields after all checks
        super(Booking, self).save(*args, **kwargs)
        
        
    # def save(self, *args, **kwargs):
    #     if self.pk:  # Existing booking, so check room availability
    #         available, unavailable_room = self.are_rooms_available(self.room.all(), self.check_in_date, self.check_out_date)
    #         if not available:
    #             raise ValueError(f"Room {unavailable_room.room_number} is not available for the selected dates.")
        
    #     # Ensure that the booking's total amount is calculated before saving
    #     self.total_amount = self.get_total_payable_after_discount()


        super(Booking, self).save(*args, **kwargs)

    def get_duration(self):
        # Subtract check_in_date from check_out_date
        duration = self.check_out_date - self.check_in_date
        return duration.days if duration.days > 0 else 0


    def get_room_charges(self):
        """Calculate the total charges for all rooms based on the duration of the stay."""
        total_room_charges = 0
        for room in self.room.all():
            duration = self.get_duration()  # Number of days for the booking
            room_price = room.price() * duration
            total_room_charges += room_price
        return total_room_charges

    def get_service_charges(self):
        """Sum the charges for all room services, if any."""
        room_services = self.roomservice_set.all()  # Assuming a related name for room services
        total_service_charges = sum(service.price for service in room_services)
        return total_service_charges

    def get_additional_charges(self):
        """Calculate the total of all additional charges."""
        additional_charges = AdditionalCharge.objects.filter(booking=self)
        return sum(charge.amount for charge in additional_charges)

    def get_total_payable(self):
        """Calculate the total amount payable (rooms + services + additional charges)."""
        total_room_charges = self.get_room_charges()
        total_service_charges = self.get_service_charges()
        total_additional_charges = self.get_additional_charges()
        return total_room_charges + total_service_charges + total_additional_charges

    def update_room_availability(self, availability):
        """Update the availability of rooms in the booking."""
        for room in self.room.all():
            room.is_available = availability
            room.save()

    def set_checked_in(self):
        """Mark the booking as checked in."""
        self.checked_in = True
        self.save(update_fields=['checked_in'])

    @property
    def amount_paid(self):
        payment = Payment.objects.filter(booking=self).last()
        return payment.amount if payment else 0

    @property
    def payment_status(self):
        payment = Payment.objects.filter(booking=self).last()
        return payment.status if payment else 'Unpaid'


class Coupon(models.Model):
    DISCOUNT_TYPE = [
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed'),
    ]
    
    code = models.CharField(max_length=1000)
    type = models.CharField(max_length=100, choices=DISCOUNT_TYPE, default="Percentage")
    discount = models.IntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(100)])
    redemption = models.IntegerField(default=0)  # Track how many times this coupon has been used
    max_redemptions = models.IntegerField(default=1)  # Limit the number of redemptions
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    cid = ShortUUIDField(length=10, max_length=25, alphabet="abcdefghijklmnopqrstuvxyz")
    
    # Optional: Limit coupon to single use per user
    single_use = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    
    class Meta:
        ordering = ['-id']

    def is_valid(self):
        """
        Check if the coupon is valid globally (active, within date range, and not over-redeemed).
        """
        current_date = timezone.now().date()
        if not self.active:
            return False
        if self.valid_from > current_date or self.valid_to < current_date:
            return False
        if self.redemption >= self.max_redemptions:
            return False
        return True

    def is_valid_for_user(self, user):
        """
        Check if the coupon is valid for a specific user.
        If it's a single-use coupon, verify that the user hasn't already used it.
        """
        if self.single_use and CouponUsers.objects.filter(coupon=self, email=user.email).exists():
            return False
        return self.is_valid()

    def redeem_coupon(self, user):
        """
        Redeem the coupon if valid.
        Increase redemption count and ensure it's valid for the user.
        """
        if self.is_valid_for_user(user):
            self.redemption += 1
            self.save()
            return True
        return False


class CouponUsers(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)  # Assuming 'Booking' is defined elsewhere
    full_name = models.CharField(max_length=1000)
    email = models.CharField(max_length=1000)
    mobile = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.coupon.code)
    
    class Meta:
        ordering = ['-id']


class AdditionalCharge(models.Model):
    CHARGE_CATEGORY_CHOICES = [
        ('minibar', 'Minibar'),
        ('room_service', 'Room Service'),
        ('damage', 'Damage'),
        ('laundry', 'Laundry'),
        ('other', 'Other'),
    ]

    booking = models.ForeignKey(Booking, related_name='additional_charges', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CHARGE_CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - ${self.amount} for Booking {self.booking.booking_id}"
    
    
    
 
class ActivityLog(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    guest_out = models.DateTimeField()
    guest_in = models.DateTimeField()
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.booking)
    
    
 
class StaffOnDuty(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    staff_id = models.CharField(null=True, blank=True, max_length=100)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.staff_id)
    

 
class RoomServices(models.Model):
    
    SERVICES_TYPES = (
        ('Food', 'Food'),
        ('Cleaning', 'Cleaning'),
        ('Technical', 'Technical'),
    )
    booking = models.ForeignKey(Booking, null=True,  related_name= "roomservice_set", on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    service_type = models.CharField(max_length=20, choices = SERVICES_TYPES, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    def __str__(self):
        return f"{self.booking} {self.room} {self.service_type}"

    def save(self, *args, **kwargs):
        super(RoomServices, self).save(*args, **kwargs)
        # Create an AdditionalCharge entry
        AdditionalCharge.objects.create(
            booking=self.booking,
            category='room_service',
            description=f"Room service: {self.service_type}",
            amount=self.price
        )
    
    
         

class Notification(models.Model):
    
    NOTIFICATION_TYPE = (
        ("Booking Confirmed", "Booking Confirmed"),
        ("Booking Cancelled", "Booking Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=100, default="new_order", choices=NOTIFICATION_TYPE)
    seen = models.BooleanField(default=False)
    nid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['-date']

    
#  ================================================================================================================================================================   
#  =========================================================================================================================================================== 
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, null=True, blank=True)
    bid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    date= models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ['-date']



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, blank=True, null=True, related_name="reviews")
    review = models.TextField(null=True, blank=True)
    reply = models.CharField(null=True, blank=True, max_length=1000)
    rating = models.IntegerField(choices=RATING, default=None)
    active = models.BooleanField(default=False)
    helpful = models.ManyToManyField(User, blank=True, related_name="helpful")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Reviews & Rating"
        ordering = ["-date"]
        
    def __str__(self):
        return f"{self.user.username} - {self.rating}"
        