
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import RoomInventory 
from inventory.models import StockLog 

@receiver(post_save, sender=RoomInventory)
def log_room_inventory_save(sender, instance, created, **kwargs):
    if created:
        action = 'Assigned'
    else:
        action = 'Updated'

    # Fetch the unit selling price from the assigned item
    item = instance.get_assigned_item()
    unit_selling_price = item.unit_price if item else 0  # Assuming unit_price is in Item

    StockLog.create_log(
        item=item,
        quantity=instance.quantity,
        unit_selling_price=unit_selling_price,
        movement_type='TRANSFER' if created else 'ADJUST',
        reason=f"{action} to room {instance.room.room_number}"
    )

@receiver(post_delete, sender=RoomInventory)
def log_room_inventory_delete(sender, instance, **kwargs):
    item = instance.get_assigned_item()
    unit_selling_price = item.unit_price if item else 0

    StockLog.create_log(
        item=item,
        quantity=instance.quantity,
        unit_selling_price=unit_selling_price,
        movement_type='RETURN',
        reason=f"Removed from room {instance.room.room_number}"
    )