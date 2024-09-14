from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(EventType)
admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(EventAgenda)
admin.site.register(Hall)
admin.site.register(Service)
admin.site.register(EventPackage)
admin.site.register(Attendee)
admin.site.register(EventNotification)
admin.site.register(EventFeedback)
admin.site.register(StaffAssignment)
admin.site.register(EventCustomization)
admin.site.register(Coupon)