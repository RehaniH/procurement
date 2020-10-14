from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Employee, Orders, OrderStatus, Item, ItemPrices
# Register your models here.

admin.site.register(Permission)
admin.site.register(OrderStatus)
admin.site.register(Orders)
admin.site.register(Item)
admin.site.register(ItemPrices)
