from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from accounts.models import User
from bookings.models import Hotel



class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    purchase_date = models.DateField()
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    warranty_period = models.IntegerField(help_text="Warranty period in months", null=True, blank=True)
    warranty_expiry_date = models.DateField(null=True, blank=True)
  

    def is_warranty_active(self):
        return self.warranty_expiry_date and self.warranty_expiry_date >= timezone.now().date()

    def __str__(self):
        return self.name
    

    @property
    def warranty_status(self):
        return "Active" if self.is_warranty_active() else "Expired"

    @property
    def age(self):
        return (timezone.now().date() - self.purchase_date).days // 365

    def is_in_use(self):
        return EquipmentUsageLog.objects.filter(equipment=self, usage_end_time__isnull=True).exists()

    def get_usage_logs(self):
        return self.equipmentusagelog_set.all()

    def get_next_service_date(self):
        
        if self.warranty_expiry_date:
            return self.warranty_expiry_date
        return self.purchase_date + timezone.timedelta(days=365)



class ConsumableItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    stock_quantity = models.PositiveIntegerField()  # Current stock level
    reorder_level = models.PositiveIntegerField()  # Minimum stock level before reordering
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def is_reorder_needed(self):
        return self.stock_quantity <= self.reorder_level

    def __str__(self):
        return self.name
    

    @property
    def needs_reorder(self):
        return self.stock_quantity <= self.reorder_level

    def reorder(self, amount):
        # Logic to reorder items from supplier
        if self.needs_reorder:
            # Trigger an alert or order process
            pass

    def restock(self, amount):
        self.stock_quantity += amount
        self.save()



class EquipmentUsageLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Staff using the equipment
    usage_start_time = models.DateTimeField()
    usage_end_time = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    def usage_duration(self):
        if self.usage_end_time:
            return self.usage_end_time - self.usage_start_time
        return None

    def __str__(self):
        return f"Usage Log for {self.equipment.name} by {self.user.username}"


    def end_usage(self):
        self.usage_end_time = timezone.now()
        self.save()

    def get_usage_duration(self):
        if self.usage_end_time:
            duration = self.usage_end_time - self.usage_start_time
            return duration.total_seconds() // 3600  # Returns in hours
        return None



class InsurancePolicy(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100, unique=True)
    provider = models.CharField(max_length=255)
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    expiry_date = models.DateField()

    def is_insurance_active(self):
        return self.expiry_date >= timezone.now().date()

    def __str__(self):
        return f"Insurance for {self.equipment.name}"


    def renew_policy(self, months):
        if self.expiry_date:
            self.expiry_date += timezone.timedelta(days=30 * months)
            self.save()



class EquipmentAuditLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    change_date = models.DateTimeField(auto_now_add=True)
    change_description = models.TextField()  # Details about what was changed

    def __str__(self):
        return f"Change made to {self.equipment.name} by {self.changed_by.username} on {self.change_date}"
    
    @staticmethod
    def create_log(equipment, user, description):
        log = EquipmentAuditLog(
            equipment=equipment,
            changed_by=user,
            change_description=description
        )
        log.save()



class InspectionChecklist(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    checklist_item = models.CharField(max_length=255)
    is_passed = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    inspection_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.checklist_item} for {self.equipment.name}"


    def pass_inspection(self):
        self.is_passed = True
        self.save()

    def fail_inspection(self, remarks):
        self.is_passed = False
        self.remarks = remarks
        self.save()

