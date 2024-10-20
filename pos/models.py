from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django_countries.fields import CountryField
from accounts.models import User
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from hrm.models import Employee,DepartmentLocation
from shortuuid.django_fields import ShortUUIDField



# ProductCategory 
class ProductCategory(models.Model):
    ICONS = (
    ('fa-bowl-rice','fa-bowl-rice'),
    ('fa-cocktail','fa-cocktail'),
    ('fa-ice-cream','fa-ice-cream'),
    ('fa-drumstick-bite','fa-drumstick-bite'),
    ('fa-hamburger','fa-hamburger'),
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    icon_class = models.CharField(max_length=100, default='fa-utensils',choices =ICONS)
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
    
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank = True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="pos", default = "pos.jpg", null=True, blank =True)
    stock_quantity = models.PositiveIntegerField()
    department_location = models.ForeignKey(DepartmentLocation, on_delete=models.CASCADE, null=True, blank = True)
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
class PosCustomer(models.Model):
    customer_name = models.CharField(max_length=50, null=True, blank=True)
    customer_room_number = models.CharField(max_length=10, null=True, blank=True)  # If room is assigned
    pos_customer = models.BooleanField(default=True, blank = True, null = True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


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
    customer = models.ForeignKey(PosCustomer, on_delete=models.CASCADE, null=True, blank=True)
    staff = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)  # POS staff handling the transaction
    waiter = models.ForeignKey(Employee, related_name="orders", on_delete=models.CASCADE, null=True, blank=True)  # Waiter attending the order

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

class PosPayment(models.Model):
    
    
    PAYMENT_METHODS = (
    ('CASH', 'CASH'),
    ('CARD', 'CARD'),
    ('ROOM_CHARGE', 'ROOM_CHARGE'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS)  
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20,
        choices=[('PAID', 'PAID'), ('PARTIALLY_PAID', 'PARTIALLY_PAID'), ('UNPAID', 'UNPAID')],
        default='PAID'
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    transaction_id = ShortUUIDField(unique=True, length=10, max_length=20, alphabet="abcdefghijklmnopqrstuvxyz")
    created_at = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

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
        

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return f"Cart - {self.user or self.session_key}"
    
    
    @property
    def subtotal(self):
        return sum(float(item.total_price)for item in self.items.all())

    @property
    def taxes(self):
        return self.subtotal * 0.06  # Assuming a 6% tax rate

    @property
    def total(self):
        return self.subtotal + self.taxes
    
    @property
    def total_items(self):
        # This sums up the quantity of each item in the cart
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
