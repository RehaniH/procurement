from django.db import models
from django.contrib.auth.models import User as user
# Create your models here.


class Location(models.Model):
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    address_line3 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    def __str__(self):
        add = self.address_line1 + ', ' + self.address_line2 + ', '
        if self.address_line3 is not None:
            add = add + self.address_line3 + ', '
        add = add + self.city + ' (' + self.postal_code + ') '
        return add

    def get_address(self):
        """"Return the address as a string"""
        add = self.address_line1 + ', ' + self.address_line2 + ', '
        if self.address_line3 is not None:
            add = add + self.address_line3 + ', '
        add = add + self.city + ' (' + self.postal_code + ') '
        return add


class Site(models.Model):
    name = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    budget = models.FloatField

    def __str__(self):
        return self.name


class Supplier(models.Model):
    company_name = models.CharField(max_length=50)
    company_address = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=13)
    email = models.CharField(max_length=50)


class UserType(models.Model):
    name =  models.CharField(max_length=50)  
    abbv =  models.CharField(max_length=13) #MANG #SUPV #SMANG #ACCST

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(#One to one ? 
        user, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=13)
    employee_type = models.ForeignKey(UserType, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Site, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname



class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemPrices(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['item', 'supplier', 'price'], name='item_suppliers')
        ]


class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField(default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    quantity_type = models.CharField(max_length=15)
    reorder_level = models.IntegerField(default=10, null=True, blank=True)


class OrderStatus(models.Model):
    status = models.CharField(max_length=50)  # the string is already defined
    # can use the abbreviation to set the status : PEND, APPV, PAPPV, DECL, RETRND, DELET, REFERD
    abbv = models.CharField(max_length=6)
    # get the object through OrderStatus.objects.get(abbv=PEND) gives Pending object


class RequestOrders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    expected_date = models.CharField(max_length=50, null=True)
    comment = models.CharField(max_length=50, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE,null=True)
    auto_genarated=models.BooleanField(default=False)
    quantity_type=models.CharField(max_length=50,null=True)
    
    def __str__(self):
        return self.item.name


class Orders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    remaining_quantity = models.IntegerField(null=True)
    quantity_type = models.CharField(max_length=15, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(
        UserType, on_delete=models.CASCADE, null=True, blank=True)
    delivery_date = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    request = models.OneToOneField(RequestOrders, on_delete=models.CASCADE)#make this a one to one feild
    # do we need a comment here as in RequestOrders


class Rule1(models.Model):
    rule_code = models.CharField(max_length=15)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    active_status = models.BooleanField(default=True)


class Rule2(models.Model):
    rule_code = models.CharField(max_length=15)
    price_limit = models.FloatField(null=True, blank=True)
    active_status = models.BooleanField(default=True)


class Rule3(models.Model):
    rule_code = models.CharField(max_length=15)
    level = models.IntegerField(default=1, null=True, blank=True)
    active_status = models.BooleanField(default=True)


class DeliveryLog(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    purchased_orders = models.ForeignKey(
        Orders, on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=50)
    quantity = models.IntegerField(blank=True, null=True)


class Pending_orders(models.Model):
    orderno = models.ForeignKey(Orders, on_delete=models.CASCADE)
    Ruletype1 = models.IntegerField(default=0,null=False, blank=False)
    Ruletype2 = models.IntegerField(default=0,null=False, blank=False)
    Ruletype3 = models.IntegerField(default=0,null=False, blank=False)
    DeleteRequest = models.IntegerField(default=0,null=False, blank=False)
    EditRequest = models.IntegerField(default=0,null=False, blank=False)
    approved = models.IntegerField(default=0,null=False,blank=False)

