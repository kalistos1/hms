from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django_countries.fields import CountryField
from accounts.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum



# ProductCategory 
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

def pre_save_category_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_category_slug, sender=ProductCategory)



# Product 
class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.price}'

    @property
    def is_in_stock(self):
        """Check if product is in stock."""
        return self.stock_quantity > 0

def pre_save_product_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_product_slug, sender=Product)



# Customer 
class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10, blank=True)  # If room is assigned
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    nationality = CountryField()
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

def pre_save_customer_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(f"{instance.first_name} {instance.last_name}")

pre_save.connect(pre_save_customer_slug, sender=Customer)


# POSUser
class POSUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username



# Discount

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.code} - {self.discount_percentage}%'

    def clean(self):
        if self.discount_percentage > 100:
            raise ValidationError("Discount percentage cannot exceed 100%.")



# Order 
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(POSUser, on_delete=models.CASCADE)  # User handling the transaction
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    order_status = models.CharField(
        max_length=20,
        choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')],
        default='PENDING'
    )
    room_charge = models.BooleanField(default=False)  # If the order is charged to the room
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} - {self.get_order_status_display()}'

    @property
    def final_total(self):
        """
        Calculate final total after applying discount.
        """
        if self.discount:
            discount_amount = (self.total_amount * self.discount.discount_percentage) / 100
            return self.total_amount - discount_amount
        return self.total_amount



# OrderItem 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} (x{self.quantity})'

    @property
    def get_total_price(self):
        return self.price * self.quantity

# Payment

class Payment(models.Model):
    
    
    PAYMENT_METHODS = (
    ('CASH', 'Cash'),
    ('CARD', 'Card'),
    ('ROOM_CHARGE', 'Room Charge'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[('PAID', 'Paid'), ('PARTIALLY_PAID', 'Partially Paid'), ('UNPAID', 'Unpaid')],
        default='PAID'
    )
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Order {self.order.id} - {self.amount_paid}'
    
    

# Refund 
class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Refund for Order {self.order.id} - {self.refund_amount}'

    def clean(self):
        total_paid = self.order.payment_set.aggregate(Sum('amount_paid'))['amount_paid__sum']
        if self.refund_amount > total_paid:
            raise ValidationError('Refund amount cannot exceed total payment.')
        

# Shift 
class Shift(models.Model):
    staff = models.ForeignKey(POSUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)  # Active until manually closed
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Shift {self.id} by {self.staff}'

    @property
    def shift_duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return 'Shift still ongoing'
