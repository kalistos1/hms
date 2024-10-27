

from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.template.defaultfilters import escape
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User
from django.utils import timezone
from django_countries.fields import CountryField
import shortuuid
from taggit.managers import TaggableManager
from django.core.exceptions import ValidationError
from django.db import transaction
from inventory.models import Amenity, Equipment, Item, Warehouse,InventoryMovement
from django.db.models import Sum
from decimal import Decimal
from hrm.models import DepartmentLocation



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

    def __str__(self):
        return f"{self.room_type.type} - Room {self.room_number}"


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


class RoomInventory(models.Model):
    STATUS_CHOICES = [
        ('in_repairs', 'In Repairs'),
        ('in_use', 'In Use'),
        ('decommissioned', 'Decommissioned'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='room_allocations')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, null=True, blank=True)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE, null=True, blank=True)
    consumable = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('room', 'equipment', 'consumable', 'amenity')

    def __str__(self):
        return f"{self.room.room_number} - {self.equipment or self.consumable or self.amenity}"

    def clean(self):
        # Ensure that only one of equipment, amenity, or consumable is set
        if sum(bool(field) for field in [self.equipment, self.amenity, self.consumable]) != 1:
            raise ValidationError("Exactly one of equipment, amenity, or consumable must be set.")


    def save(self, *args, **kwargs):
        self.clean()  # Ensure data integrity

        # Use transaction to ensure atomicity
        with transaction.atomic():
            # Retrieve the DepartmentLocation instance for 'room'
            try:
                room_location = DepartmentLocation.objects.get(name='rooms')
            except ObjectDoesNotExist:
                raise ValidationError("Department location for 'room' does not exist.")

            if self.pk:
                # Existing record; determine if quantity or item has changed
                previous = RoomInventory.objects.get(pk=self.pk)
                quantity_diff = self.quantity - previous.quantity
                item = self.get_assigned_item()

                if quantity_diff > 0:
                    # Allocating more items to the room
                    self.warehouse.remove_stock(item, quantity_diff)
                    InventoryMovement.objects.create(
                        item=item,
                        warehouse=self.warehouse,
                        quantity=quantity_diff,
                       
                        movement_type='TRANSFER',
                        transfer_location=room_location,
                        reason=f"Assigned to room {self.room.room_number}"
                    )
                elif quantity_diff < 0:
                    # Deallocating items from the room
                    self.warehouse.add_stock(item, abs(quantity_diff))
                    InventoryMovement.objects.create(
                        item=item,
                        warehouse=self.warehouse,
                        quantity=abs(quantity_diff),
                      
                        movement_type='RETURN',
                        transfer_location=self.warehouse.department_location,  # Assuming warehouse location here
                        reason=f"Removed from room {self.room.room_number}"
                    )
            else:
                # New record; allocate items to the room
                item = self.get_assigned_item()
                self.warehouse.remove_stock(item, self.quantity)
                InventoryMovement.objects.create(
                    item=item,
                    warehouse=self.warehouse,
                    quantity=self.quantity,
                  
                    movement_type='TRANSFER',
                    transfer_location=room_location,
                    reason=f"Assigned to room {self.room.room_number}"
                )

            super(RoomInventory, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
            # When deleting, return the stock to the warehouse
            with transaction.atomic():
                item = self.get_assigned_item()
                self.warehouse.add_stock(item, self.quantity)
                InventoryMovement.objects.create(
                    item=item,
                    warehouse=self.warehouse,
                    quantity=self.quantity,
                   
                    movement_type='RETURN',
                    transfer_location='warehouse',
                    reason=f"Deleted from room {self.room.room_number}"
                )
                super(RoomInventory, self).delete(*args, **kwargs)

    def get_assigned_item(self):
        item = Item.objects.filter(stock_type='equipment', equipment__isnull=False).first()
        if not item:
            raise ValidationError("No available equipment item for assignment.")
        return item


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
        ('transfer', 'Transfer'),
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
        # Update total room charges and amount when processing payment
        if self.status in ['advance', 'completed']:
            self.booking.calculate_total()  # Ensure the total room charges are updated

            # Update room availability (like before)
            self.booking.update_room_availability(False)

            # Mark as checked in (if advance payment)
            if self.status == 'advance':
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


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey('Hotel', on_delete=models.SET_NULL, null=True)
    room_type = models.ForeignKey('RoomType', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey('Room', on_delete=models.CASCADE,null= True)  # This can be used for both bookings and reservations
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_adults = models.PositiveIntegerField(default=1)
    num_children = models.PositiveIntegerField(default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    # def calculate_total(self):
    #     additional = self.additional_charges.aggregate(total=models.Sum('amount'))['total'] or 0
    #     return self.total_amount + additional

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
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey instead of M2M
    date = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username if self.user else 'Guest'}"
    

    
    def get_total_due(self):
        total = self.calculate_total()  # Ensure this is your method to calculate the regular total
        if self.coupon:
            total -= self.coupon.get_discount_amount(total)  # Adjust total with coupon discount
        return total


    def get_duration(self):
        """Get the duration of the booking in days."""
        duration = self.check_out_date - self.check_in_date
        return max(duration.days, 1)  # Ensure at least 1 day


    def get_room_charges(self):
        """Calculate the total charges for the room based on the duration of the stay."""
        if not self.room:
            return 0  # If no room is assigned, return 0

        duration = self.get_duration()  # Number of days for the booking
        room_price = self.room.price_override if self.room.price_override else self.room.room_type.base_price  # Use price override if available
        total_room_charges = room_price * duration
        
        return total_room_charges
    
    
    def set_checked_in(self):
        """Mark the booking as checked in."""
        self.checked_in = True
        self.save(update_fields=['checked_in'])

    def calculate_total(self):
        """Calculate and update the total booking amount (room charges + additional charges - discounts)."""
        total_room_charges = self.get_room_charges()  # Calculate room charges based on the stay duration
        discount_amount = self.get_discount_amount()  # Calculate discount amount if coupon is applied

        self.total_amount = float(total_room_charges) - discount_amount  # Subtract the discount from the total
        self.save()  # Save the updated total amount

        # Redeem the coupon and create CouponUsers entry if valid
        if self.coupon:
            self.redeem_coupon()

        return self.total_amount  # Explicitly return the total amount


    def get_discount_amount(self):
        """Calculate the discount amount based on the coupon."""
        if self.coupon and self.coupon.is_valid():
            total_payable = self.get_room_charges()  # Get room charges for discount calculation
            discount_value = self.coupon.discount  # Accessing the discount field
            return float(total_payable )* (discount_value / 100)  # Assuming discount is a percentage
        return 0


    def redeem_coupon(self):
        """Redeem the coupon and create a CouponUsers entry."""
        if self.coupon.is_valid_for_user(self.user):  # Ensure the coupon is valid for this user
            # Redeem the coupon and increase its redemption count
            self.coupon.redeem_coupon(self.user)

            # Create an entry in CouponUsers
            CouponUsers.objects.create(
                coupon=self.coupon,
                booking=self,
                email=self.user.email
            )

    def update_room_availability(self, availability):
        """Update the availability of the room in the booking."""
        if self.room:
            self.room.is_available = availability
            self.room.save()

        
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
    
    #receipt methods
    
    # def get_room_charge(self):
    #     """Calculate the total room charge based on the booking duration and room price."""
    #     return self.get_duration() * self.room.price
    
    def get_coupon_discount(self):
        """Return the discount amount based on the associated coupon."""
        if self.coupon:
            return self.coupon.get_discount_amount(self.get_room_charges())
        return 0

    def get_total_after_discount(self):
        """Return the total charge after applying the coupon discount."""
        room_charge = self.get_room_charges()
        coupon_discount = self.get_coupon_discount()
        return float(room_charge) - coupon_discount
    

    def get_initial_payment(self):
        """Get the first advance payment made by the customer."""
        payment = self.payments.filter(status='advance').first()
        return payment.amount if payment else 0


    def get_balance_remaining(self):
        """Calculate the remaining balance after the initial payment."""
        total_after_discount = self.get_total_after_discount()
        initial_payment = self.get_initial_payment()
        return total_after_discount -float(initial_payment)
    
    # receipt methods end


    @property
    def amount_paid(self):
        payment = Payment.objects.filter(booking=self).last()
        return payment.amount if payment else 0

    @property
    def payment_status(self):
        payment = Payment.objects.filter(booking=self).last()
        return payment.status if payment else 'Unpaid'

# receipt summary before chckout

    @property
    def booking_date(self):
        return self.date  # Date booking was made

    @property
    def checkin_date(self):
        return self.check_in_date
    
    @property
    def checkout_date(self):
        return self.check_out_date
    
    @property
    def num_days(self):
        return self.get_duration()  # Use the existing method to get the number of days
    
    @property
    def room_charges(self):
        return self.get_room_charges()  # Use the existing method to calculate room charges
    

    @property
    def additional_charges(self):
        # Use the related_name 'additional_charges' instead of 'additional_charges_set'
        additional_charges = self.additionalcharges.aggregate(total=Sum('amount'))['total'] or 0
      
        return additional_charges

    @property
    def additional_services(self):
        # Use the correct related_name 'roomservice'
        additional_services = self.roomservice.aggregate(total=Sum('price'))['total'] or 0
        
        return additional_services

    @property
    def coupon_discount_value(self):
        if self.coupon:
            return self.coupon.get_discount_amount(self.room_charges)
        return 0
    
    @property
    def sum_of_all_charges(self):
        
        # Ensure all values are treated as Decimal
        room_charges = Decimal(self.get_room_charges() or 0)
        additional_charges = Decimal(self.additional_charges or 0)
        additional_services = Decimal(self.additional_services or 0)

        # Calculate total charge as a Decimal
        sum_of_all_charges = room_charges + additional_charges + additional_services
        return sum_of_all_charges
    
    @property
    def final_charge(self):
        sum_of_all_charges= self.sum_of_all_charges
        # Ensure coupon discount is also Decimal
        coupon_discount = Decimal(self.coupon_discount_value or 0)

        # Calculate final charge by subtracting the coupon discount (if available)
        return sum_of_all_charges - coupon_discount

    
    @property
    def initial_payment(self):
        return self.get_initial_payment()  # Use the method to get initial advance payment
    
    @property
    def amount_payable(self):
        # Calculate amount payable after coupon and initial payment have been applied
        return self.final_charge - self.initial_payment
    
    def get_receipt_summary(self):
        """Returns a summary of all booking details for the checkout."""
        return {
            "booking_id": self.booking_id,
            "user": self.user.username if self.user else "Guest",
            "booking_date": self.booking_date,
            "checkin_date": self.checkin_date,
            "checkout_date": self.checkout_date,
            "num_days": self.num_days,
            "room_charges": self.room_charges,
            "additional_charges": self.additional_charges,
            "additional_services": self.additional_services,
            "sum_of_all_charges": self.sum_of_all_charges,
            "coupon_applied": bool(self.coupon),
            "coupon_discount": self.coupon_discount_value,
            "initial_payment": self.initial_payment,
            "final_charge": self.final_charge,
            "amount_payable": self.amount_payable,
        }

#recceipt summary ends

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Check room availability again in a transaction
            available, conflicting_room = self.are_rooms_available([self.room], self.check_in_date, self.check_out_date)
            if not available:
                raise ValueError(f"Room {self.room.room_number} is not available for the selected dates.")
            
            # Proceed with saving the booking
            super().save(*args, **kwargs)


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
    
    def get_discount_amount(self, total):
        if self.type == 'Percentage':
            return float(total)* (self.discount / 100)
        elif self.type == 'Fixed':
            return min(self.discount, total)  # Don't exceed the total
        return 0
    

class CouponUsers(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)  # Assuming 'Booking' is defined elsewhere
    email = models.CharField(max_length=1000)

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

    booking = models.ForeignKey(Booking, related_name='additionalcharges', on_delete=models.CASCADE)
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
    booking = models.ForeignKey(Booking, null=True,  related_name= "roomservice", on_delete=models.CASCADE)
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
        