from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Employee, Orders, OrderStatus, Item, ItemPrices, Rule1, Rule2, Rule3, Pending_orders, RequestOrders
# Register your models here.

admin.site.register(Permission)
admin.site.register(OrderStatus)
admin.site.register(Orders)
admin.site.register(Item)
admin.site.register(ItemPrices)
admin.site.register(Rule1)
admin.site.register(Rule2)
admin.site.register(Rule3)
admin.site.register(Pending_orders)
admin.site.register(RequestOrders)
