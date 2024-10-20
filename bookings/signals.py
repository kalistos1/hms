
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
    StockLog.create_log(
        item=instance.get_assigned_item(),
        quantity=instance.quantity,
        movement_type='TRANSFER' if created else 'ADJUST',
        reason=f"{action} to room {instance.room.name}"
    )

@receiver(post_delete, sender=RoomInventory)
def log_room_inventory_delete(sender, instance, **kwargs):
    StockLog.create_log(
        item=instance.get_assigned_item(),
        quantity=instance.quantity,
        movement_type='RETURN',
        reason=f"Removed from room {instance.room.name}"
    )
