from django.db import models
from django.utils import timezone
from accounts.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from dateutil.relativedelta import relativedelta  # Import relativedelta
from django.utils.text import slugify
from hrm .models import DepartmentLocation,Employee
from pos .models import Product, ProductCategory
from django.db import transaction

class Warehouse(models.Model):
    name = models.CharField(max_length=255 )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_item_quantity(self, item):
        """Get the quantity of a specific item in this warehouse."""
        try:
            warehouse_stock = WarehouseStock.objects.get(warehouse=self, item=item)
            return warehouse_stock.quantity
        except WarehouseStock.DoesNotExist:
            return 0  # If the item is not found in this warehouse, return 0
        
    def get_all_items_and_quantities(self):
        """Get all items and their quantities in this warehouse."""
        items_and_quantities = self.stocks.select_related('item').values('item__name', 'quantity')
        return items_and_quantities

    def add_stock(self, item, quantity):
        """Add stock for a specific item."""
        warehouse_stock, created = WarehouseStock.objects.get_or_create(warehouse=self, item=item)
        warehouse_stock.add_stock(quantity)

    def remove_stock(self, item, quantity):
        """Remove stock for a specific item."""
        try:
            warehouse_stock = WarehouseStock.objects.get(warehouse=self, item=item)
            warehouse_stock.remove_stock(quantity)
        except WarehouseStock.DoesNotExist:
            raise ValidationError(f"No stock available for {item.name} in {self.name}.")
        

class ItemCategory(models.Model):
    name = models.CharField(max_length = 250)
    slug = models.SlugField ()
    parent = models.ForeignKey('self',blank=True, null=True ,related_name='children', on_delete = models.CASCADE)

    class Meta:
       unique_together = ('slug', 'parent',)    
       verbose_name_plural = 'inventory_categories'
       db_table = 'inventory_categories'

    def save(self, *args, **kwargs):        
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super( ItemCategory, self).save(*args, **kwargs)
    
        
    def __str__(self):                           
        full_path = [self.name]                  
        parent_cat = self.parent
        while parent_cat is not None:
            full_path.append(parent_cat.name)
            parent_cat = parent_cat.parent
        return ' -> '.join(full_path[::-1])


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField(validators=[EmailValidator()], unique=True) 
    notes = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.name
    

class Item(models.Model):
    STOCK_TYPES = (
        ('utility', 'Utility'),
        ('consumable_item', 'Consumable Item'),
        ('equipment', 'Equipment'),
        ('amenity', 'Amenity'),
    )
    
    stock_type = models.CharField(max_length=20, choices=STOCK_TYPES) 
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    purchase_receipt = models.ImageField(upload_to="consumable_receipts", blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='consumable', db_index=True)
    purchase_date = models.DateField()
    equipment = models.OneToOneField('Equipment', on_delete=models.CASCADE, null=True, blank=True, related_name='equimentitem')  # Link to Equipment model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_cost(self):
        return self.unit_price * self.stock_quantity
 

    def purchase(self, amount):
        """Purchase consumable items and update stock."""
        if amount <= 0:
            raise ValidationError("Purchase amount must be a positive integer.")

        if self.stock_quantity < amount:
            raise ValidationError("Not enough stock available for purchase.")

        self.stock_quantity -= amount
        self.save()


class PurchaseOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('ordered', 'Ordered'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ])

    def __str__(self):
        return f"Order of {self.quantity} {self.item.name} from {self.supplier.name}"
    

class InventoryMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('IN', 'Incoming'),
        ('OUT', 'Outgoing'),
        ('TRANSFER', 'Transfer'),
        ('RETURN', 'Return'),
        ('ADJUST', 'Adjustment'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_movements')
    quantity = models.IntegerField()
    unit_selling_price = models.DecimalField(help_text="For items being sold at POS", max_digits=12, decimal_places=2, default=0, null= True, blank = True)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    transfer_location = models.ForeignKey(DepartmentLocation, on_delete=models.SET_NULL, null=True, blank=True)  # Destination for transfers
    date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    performed_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)  # Employee carrying out the movement

    def __str__(self):
        return f"{self.item.name} - {self.movement_type}"

    def save(self, *args, **kwargs):
        from inventory.models import StockReceipt

        # Retrieve or create warehouse stock record
        warehouse_stock, created = WarehouseStock.objects.get_or_create(
            warehouse=self.warehouse, 
            item=self.item
        )

        # Handle different movement types
        if self.movement_type == 'IN':
            self.item.stock_quantity -= self.quantity
            warehouse_stock.add_stock(self.quantity)  # Add to warehouse stock
            destination = "Warehouse"

            # Track price change if the item price differs from the previous pricev
            self.track_price_change(warehouse_stock)

        elif self.movement_type == 'OUT':
            if warehouse_stock.quantity < self.quantity:
                raise ValidationError("Insufficient stock in warehouse for this operation.")
            self.item.stock_quantity -= self.quantity
            warehouse_stock.remove_stock(self.quantity)
            destination = "Warehouse"

        elif self.movement_type == 'TRANSFER':
            if warehouse_stock.quantity < self.quantity:
                raise ValidationError("Insufficient stock in warehouse for this operation.")
            self.item.stock_quantity -= self.quantity
            warehouse_stock.remove_stock(self.quantity)

            if self.transfer_location:
                destination = self.transfer_location.name
                StockReceipt.objects.create(
                    department_location=self.transfer_location,
                    product_received=self.item,
                    price_per_item=warehouse_stock.unit_purchase_price,  # Ensure price matches warehouse unit price
                    selling_price_per_item=self.unit_selling_price,
                    quantity_received=self.quantity,
                    mark_as_received=False  # Adjust based on business logic
                )
            else:
                destination = "Unknown"

        elif self.movement_type == 'RETURN':
            self.item.stock_quantity += self.quantity
            warehouse_stock.add_stock(self.quantity)
            destination = "Warehouse"

            # Track price change on returns
            self.track_price_change(warehouse_stock)

        elif self.movement_type == 'ADJUST':
            destination = "Warehouse"

        # Save the item and warehouse stock changes
        self.item.save()
        warehouse_stock.save()

        # Log the stock movement
        StockLog.create_log(
            item=self.item,
            quantity=self.quantity,
            unit_selling_price=self.unit_selling_price,
            movement_type=self.movement_type,
            reason=self.reason,
            destination=destination,
            performed_by=self.performed_by.user.get_full_name() if self.performed_by else "Unknown"
        )

        super().save(*args, **kwargs)

    def track_price_change(self, warehouse_stock):
        """ Track price changes for incoming or return movements """
        # Compare the item's current price with the last recorded price
        if self.item.unit_price != warehouse_stock.unit_purchase_price:
            PriceHistory.objects.create(
                item=self.item,
                old_price=warehouse_stock.unit_purchase_price,
                new_price=self.item.unit_price
            )
            # Update the warehouse stock price
            warehouse_stock.unit_purchase_price = self.item.unit_price


class PriceHistory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='price_history')
    old_price = models.DecimalField(max_digits=12, decimal_places=2)
    new_price = models.DecimalField(max_digits=12, decimal_places=2)
    change_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price change for {self.item.name} from {self.old_price} to {self.new_price} on {self.change_date}"


class WarehouseStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    unit_purchase_price  =  models.DecimalField( max_digits=12, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity} in {self.warehouse.name}"
    
    def add_stock(self, quantity):
        """Increase stock by the given quantity."""
        if quantity <= 0:
            raise ValueError("Quantity to add must be positive.")
        self.quantity += quantity
        self.save()

    def remove_stock(self, quantity):
        """Decrease stock by the given quantity."""
        if quantity <= 0:
            raise ValueError("Quantity to remove must be positive.")
        if quantity > self.quantity:
            raise ValidationError(f"Not enough stock for {self.item.name} in {self.warehouse.name}.")
        self.quantity -= quantity
        self.save()


class StockLog(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('IN', 'Incoming'),
        ('OUT', 'Outgoing'),
        ('TRANSFER', 'Transfer'),
        ('RETURN', 'Return'),
        ('ADJUST', 'Adjustment'),
    ]
    
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='stock_logs')
    quantity = models.IntegerField()
    unit_selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, null = True, blank = True)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    destination = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(blank=True, null=True)
    performed_by = models.CharField(max_length=255, null=True, blank=True)  # Employee who performed the movement
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.item.name} - {self.movement_type} - {self.quantity} units"

    @staticmethod
    def create_log(item, quantity, unit_selling_price, movement_type, reason="", destination=None, performed_by=None):
        """Helper method to create a stock log with destination and employee responsible."""
        StockLog.objects.create(
            item=item,
            quantity=quantity,
            unit_selling_price = unit_selling_price,
            movement_type=movement_type,
            reason=reason,
            destination=destination,
            performed_by=performed_by
        )


class StockReceipt(models.Model):
    department_location = models.ForeignKey(DepartmentLocation, on_delete=models.CASCADE, null=True, blank=True)
    department_user = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)  # User receiving the stock
    product_received = models.ForeignKey('inventory.Item', on_delete=models.CASCADE)  # Linking to the inventory item model
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)  # Link to Product model
    product_sales_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    price_per_item = models.FloatField(default=0)
    selling_price_per_item = models.FloatField(default=0)
    quantity_received = models.PositiveIntegerField()
    mark_as_received = models.BooleanField(default=False)
    date_received = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        department_user = self.department_user.user.get_full_name() if self.department_user else "Unknown User"
        return f'{self.department_location.name} received {self.quantity_received} of {self.product_received.name} by {department_user} on {self.date_received}'

    def update_or_create_product(self):
        """Update or create the Product model with the received stock and other details, including product_sales_category."""
        try:
            # If there's no linked product, create one
            if not self.product:
                product, created = Product.objects.get_or_create(
                    name=self.product_received.name,
                    department_location=self.department_location,
                    defaults={
                        'price': self.selling_price_per_item,
                        'stock_quantity': self.quantity_received,
                        'description': self.product_received.description,
                        'category': self.product_sales_category, 
                    }
                )
                self.product = product  # Link the product to the StockReceipt

            else:
                # If product exists, update its stock, price, and category
                self.product.stock_quantity += self.quantity_received
                self.product.price = self.selling_price_per_item
                self.product.category = self.product_sales_category  # Update the category if needed
                self.product.save()

        except Exception as e:
            raise ValueError(f"Error updating or creating product: {str(e)}")

    def save(self, *args, **kwargs):
        # Save the stock receipt first
        with transaction.atomic():  # Ensure we are in a transaction block
            super().save(*args, **kwargs)

            # Only update the product if mark_as_received is True
            if self.mark_as_received:
                try:
                    self.update_or_create_product()  # Update the Product model with the new stock and details
                    # Save the updated StockReceipt with the product linked after updating or creating the product
                    super().save(update_fields=['product'])  # No recursion as it's only updating a specific field
                except ValueError as e:
                    print(str(e))

          

class Equipment(models.Model):
    EQUIPMENT_STATUS = (
        ('active', 'Active'),
        ('in_repair', 'In Repair'),
        ('out_of_service', 'Out of Service'),
    )
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS, db_index=True, default="active")
    warranty_period = models.IntegerField(help_text="Warranty period in months", null=True, blank=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True)
    purchase_date = models.DateField(null=True, blank=True)  # Add purchase date
    item = models.OneToOneField('Item', on_delete=models.CASCADE, related_name='equipment_item', null=True, blank=True)  # Link back to Item
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_warranty_active(self):
        """Check if the warranty is still active."""
        return self.warranty_expiry_date and self.warranty_expiry_date >= timezone.now().date()

    def __str__(self):
        return self.name

    @property
    def warranty_status(self):
        """Return the current warranty status as 'Active' or 'Expired'."""
        return "Active" if self.is_warranty_active() else "Expired"

    @property
    def age(self):
        """Return the age of the equipment in a human-readable format (years and months)."""
        delta = timezone.now().date() - self.purchase_date
        years = delta.days // 365
        months = (delta.days % 365) // 30
        return f"{years} years and {months} months"

    def schedule_service(self, date):
        """Schedule the next service date for the equipment."""
        self.next_service_date = date
        self.save()


class Amenity(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='amenities')
    items = models.ManyToManyField(Item, related_name='amenities')
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost for using the amenity, if applicable.")
    is_available = models.BooleanField(default=True, help_text="Indicates if the amenity is available for use.")
    is_active = models.BooleanField(default=True, help_text="Controls if the amenity is active and visible.")
    id_code = models.PositiveIntegerField(default=0, help_text="Order for displaying amenities in the system.")
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Quantity available for tangible items.")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, help_text="Supplier of this amenity.")
    
    class Meta:
        ordering = ['id_code', 'name']

    def __str__(self):
        return self.name

    # Availability management
    def mark_unavailable(self):
        """Mark the amenity as unavailable."""
        self.is_available = False
        self.save()

    def mark_available(self):
        """Mark the amenity as available."""
        self.is_available = True
        self.save()
    
    def total_value(self):
        """Calculate the total value of the items associated with this amenity."""
        return sum(item.total_cost for item in self.items.all())

    def add_item(self, item):
        """Add an item to this amenity."""
        self.items.add(item)

    def remove_item(self, item):
        """Remove an item from this amenity."""
        self.items.remove(item)

    @classmethod
    def get_active_amenities(cls, hotel):
        """Retrieve all active amenities for a given hotel."""
        return cls.objects.filter(hotel=hotel, is_active=True, is_available=True).order_by('display_order')



class EquipmentUsageLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='usage_logs', db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment_usage_logs', db_index=True)
    usage_start_time = models.DateTimeField()
    usage_end_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def usage_duration(self):
        """Return a descriptive usage duration string."""
        if self.usage_end_time:
            duration = self.usage_end_time - self.usage_start_time
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{int(hours)} hours, {int(minutes)} minutes"
        return None

    def __str__(self):
        return f"Usage Log for {self.equipment.name} by {self.user.username}"

    def end_usage(self):
        """End the usage session by setting the end time to now."""
        self.usage_end_time = timezone.now()
        self.save()

    @classmethod
    def is_equipment_in_use(cls, equipment):
        """Check if the equipment is currently in use."""
        return cls.objects.filter(equipment=equipment, usage_end_time__isnull=True).exists()

    @classmethod
    def start_usage(cls, equipment, user):
        """Start a new usage session for the equipment."""
        if cls.is_equipment_in_use(equipment):
            raise ValidationError(f"{equipment.name} is currently in use. Cannot start a new session.")
        
        return cls.objects.create(equipment=equipment, user=user, usage_start_time=timezone.now())

    @classmethod
    def get_recent_logs(cls, limit=10):
        """Retrieve recent equipment usage logs with optimized queries."""
        return cls.objects.select_related('equipment', 'user').order_by('-usage_start_time')[:limit]
    

class InsurancePolicy(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='insurance_policies', db_index=True)
    policy_number = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=255)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    expiry_date = models.DateField()

    def is_insurance_active(self):
        """Check if the insurance policy is currently active."""
        return self.expiry_date >= timezone.now().date()

    def __str__(self):
        return f"Insurance for {self.equipment.name}"

    def renew_policy(self, months):
        """Renew the insurance policy for a specified number of months, 
        ensuring the current date is before the expiry date."""
        if self.expiry_date:
            if timezone.now().date() >= self.expiry_date:
                raise ValidationError("Cannot renew the policy as it is already expired.")
            # Use relativedelta for precise month handling
            self.expiry_date += relativedelta(months=months)
            self.save()

    def notify_expiry(self):
        """Notify the user if the policy is nearing its expiry (e.g., within 30 days)."""
        if self.expiry_date and (self.expiry_date - timezone.now().date()).days <= 30:
            # Here, you can implement notification logic (e.g., sending an email or a message)
            return f"Policy {self.policy_number} for {self.equipment.name} is nearing expiry on {self.expiry_date}."
        return None

  
class EquipmentAuditLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='audit_logs', db_index=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipment_audit_logs', db_index=True)
    change_date = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()

    def __str__(self):
        return f"Change made to {self.equipment.name} by {self.changed_by.username} on {self.change_date}"

    @staticmethod
    def create_log(equipment, user, description):
        """Create a new audit log entry for a change made to equipment."""
        log = EquipmentAuditLog(
            equipment=equipment,
            changed_by=user,
            change_description=description
        )
        log.save()
        return log

    @classmethod
    def get_recent_logs(cls, equipment, limit=5):
        """Retrieve the most recent logs for a specific equipment item."""
        return cls.objects.filter(equipment=equipment).order_by('-change_date')[:limit]

    @classmethod
    def log_sensitive_change(cls, equipment, user, change_description):
        """Log sensitive changes to equipment with appropriate details."""
        cls.create_log(equipment, user, change_description)
        # Additional logic to handle sensitive changes can be added here


class InspectionChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='inspection_checklists', db_index=True)
    checklist_item = models.CharField(max_length=255)
    is_passed = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    inspection_date = models.DateField(auto_now_add=True)
    inspector = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='inspection_checklists')

    def __str__(self):
        return f"{self.checklist_item} for {self.equipment.name}"

    def pass_inspection(self):
        self.is_passed = True
        self.save()

    def fail_inspection(self, remarks):
        self.is_passed = False
        self.remarks = remarks
        self.save()

    @classmethod
    def all_items_passed(cls, equipment):
        """Check if all items in the checklist for the specified equipment have passed."""
        return all(item.is_passed for item in cls.objects.filter(equipment=equipment))



class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts', db_index=True)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField(null=True, blank=True)  # Expiration field for alerts

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"

    @property
    def is_expired(self):
        """Check if the alert has expired based on the current timestamp."""
        return self.expiration and timezone.now() > self.expiration

    def mark_as_read(self):
        """Mark the alert as read."""
        self.is_read = True
        self.save()







 # def is_reorder_needed(self):
    #     """Check if reorder is needed based on stock quantity and reorder level."""
    #     return self.stock_quantity <= self.reorder_level

    # def reorder(self, amount):
    #     """Implement reorder logic if reorder is needed."""
    #     if self.is_reorder_needed:
    #         # Implement reorder logic, e.g., create a purchase order, notify supplier, etc.
    #         pass

    # def restock(self, amount):
    #     """Restock the item with a positive amount."""
    #     if amount <= 0:
    #         raise ValidationError("Restock amount must be a positive integer.")
        
    #     self.stock_quantity += amount
    #     self.save()