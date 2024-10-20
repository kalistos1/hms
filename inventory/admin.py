from django.contrib import admin
from .models import (
     Equipment,  StockReceipt, Item, EquipmentUsageLog, ItemCategory,
    InsurancePolicy, EquipmentAuditLog, InspectionChecklist, Alert, Warehouse,PriceHistory,PurchaseOrder,InventoryMovement,WarehouseStock,StockLog
)
admin.site.register(Warehouse)
admin.site.register(ItemCategory)
admin.site.register(Equipment)
admin.site.register(Item)
admin.site.register( StockReceipt )
admin.site.register(PriceHistory)
admin.site.register(PurchaseOrder)
admin.site.register(InventoryMovement)
admin.site.register(WarehouseStock)
admin.site.register(StockLog)
admin.site.register(EquipmentUsageLog)
admin.site.register(InsurancePolicy)
admin.site.register(EquipmentAuditLog)
admin.site.register(InspectionChecklist)
admin.site.register(Alert)