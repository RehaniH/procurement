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

class Supplier(models.Model):
    company_name = models.CharField(max_length=50)
    company_address = models.ForeignKey(Location, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=13)
    email = models.CharField(max_length=50)

class UserType(models.Model):
    name =  models.CharField(max_length=50)  
    abbv =  models.CharField(max_length=13) 

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, null=True, blank=True)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=13)
    employee_type = models.ForeignKey(UserType, on_delete=models.CASCADE) 
    location = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

class ItemPrices(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.CharField(max_length=50)

class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    quantity_type = models.CharField(max_length=15)
    reorder_level = models.IntegerField(default=10, null=True, blank=True) 

class DeliveryLog(models.Model):
    invoice_id = models.CharField(max_length=50)
    note =  models.CharField(max_length=150)
    date = models.CharField(max_length=50)
    total = models.FloatField
    quantity = models.IntegerField
    price = models.FloatField   

class OrderStatus(models.Model):
    status = models.CharField(max_length=50) #the string is already defined
    abbv = models.CharField(max_length=6)  #can use the abbreviation to set the status : PEND, APPV, PAPPV, DECL, RETRND, DELET, REFERD
                                            # get the object through OrderStatus.objects.get(abbv=PEND) gives Pending object
class RequestOrders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    quantity_type = models.CharField(max_length=15, null=True, blank=True)
    expected_date = models.CharField(max_length=50)
    comment = models.CharField(max_length=50, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

class Orders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    quantity_type = models.CharField(max_length=15, null=True, blank=True)
    price = models.FloatField(null=True, blank=True) 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    delivery_date = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    request = models.ForeignKey(RequestOrders, on_delete=models.CASCADE)
    #do we need a comment here as in RequestOrders

