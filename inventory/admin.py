from django.contrib import admin
from .models import (
     Equipment, ConsumableItem, EquipmentUsageLog, ItemCategory,
    InsurancePolicy, EquipmentAuditLog, InspectionChecklist, Alert
)

admin.site.register(ItemCategory)
admin.site.register(Equipment)
admin.site.register(ConsumableItem)
admin.site.register(EquipmentUsageLog)
admin.site.register(InsurancePolicy)
admin.site.register(EquipmentAuditLog)
admin.site.register(InspectionChecklist)
admin.site.register(Alert)