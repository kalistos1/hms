from django.contrib import admin
from .models import Hotel,RoomAmenity, Room, Booking, RoomServices, HotelGallery, HotelFeatures, HotelFAQs, Payment,RoomType, ActivityLog, StaffOnDuty, Coupon, CouponUsers, Notification, Bookmark, Review

# Register your models here.

admin.site.register(Hotel)
admin.site.register(RoomType)

admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(RoomServices)
admin.site.register(Coupon)
admin.site.register(Notification)
admin.site.register(Bookmark)
admin.site.register(Review)
admin.site.register(RoomAmenity)
admin.site.register(Payment)