from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(ProductCategory)
admin.site.register(Product)
admin.site.register(PosCustomer)
admin.site.register(POSUser)
admin.site.register(Discount)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PosPayment)
admin.site.register(Refund)

