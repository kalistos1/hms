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
    


class Equipment(models.Model):
    EQUIPMENT_STATUS = (
        ('active', 'Active'),
        ('in_repair', 'In Repair'),
        ('out_of_service', 'Out of Service'),
    )
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='equipments', db_index=True)
    purchase_receipt = models.ImageField(upload_to="equipment_receipts", blank=True, null=True)
    status = models.CharField(max_length=20, choices=EQUIPMENT_STATUS, db_index=True, default="active")
    warranty_period = models.IntegerField(help_text="Warranty period in months", null=True, blank=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
    next_service_date = models.DateField(null=True, blank=True) 
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


class ConsumableItem(models.Model):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null = True, blank= True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)   
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    purchase_receipt = models.ImageField(upload_to="cunsumable_receipts", blank=True, null=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='consumable', db_index=True)
    reorder_level = models.PositiveIntegerField(default=0)  # Added reorder level field
    purchase_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
   

    def is_reorder_needed(self):
        """Check if reorder is needed based on stock quantity and reorder level."""
        return self.stock_quantity <= self.reorder_level

    def __str__(self):
        return self.name

    @property
    def needs_reorder(self):
        """Property to check if reorder is needed."""
        return self.is_reorder_needed()

    def reorder(self, amount):
        """Implement reorder logic if reorder is needed."""
        if self.needs_reorder:
            # Implement reorder logic, e.g., create a purchase order, notify supplier, etc.
            pass

    def restock(self, amount):
        """Restock the item with a positive amount."""
        if amount <= 0:
            raise ValidationError("Restock amount must be a positive integer.")
        
        self.stock_quantity += amount
        self.update_total_cost()
        self.save()

    def update_total_cost(self):
        """Calculate the total cost based on unit price and stock quantity."""
        self.total_cost = self.unit_price * self.stock_quantity

    def purchase(self, amount):
        """Purchase consumable items and update stock and total cost."""
        if amount <= 0:
            raise ValidationError("Purchase amount must be a positive integer.")

        self.stock_quantity -= amount
        if self.stock_quantity < 0:
            raise ValidationError("Not enough stock available for purchase.")

        self.update_total_cost()
        self.save()

class Amenity(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ItemCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='amenities')
    description = models.TextField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost for using the amenity, if applicable.")
    is_available = models.BooleanField(default=True, help_text="Indicates if the amenity is available for use.")
    is_active = models.BooleanField(default=True, help_text="Controls if the amenity is active and visible.")
    id_code = models.PositiveIntegerField(default=0, help_text="Order for displaying amenities in the system.")

    # Inventory-related fields
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