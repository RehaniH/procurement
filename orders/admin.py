from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Employee, Location, Orders, OrderStatus, Item, ItemPrices, RequestOrders, Site, Stock,DeliveryLog, Supplier
# Register your models here.

admin.site.register(Permission)
admin.site.register(OrderStatus)
admin.site.register(Orders)
admin.site.register(Item)
admin.site.register(ItemPrices)
admin.site.register(Stock)
admin.site.register(DeliveryLog)
admin.site.register(Site)
admin.site.register(RequestOrders)
admin.site.register(Location)
admin.site.register(Supplier)
admin.site.register(Employee)



