from django.db import models
# Create your models here.

class Location(models.Model):
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    address_line3 = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    def __str__(self):
        add = self.address_line1 + ', ' + self.address_line2 + ', '
        if self.address_line2 is not None:
            add = add + self.address_line2 + ', '
        add = add + self.address_line3 + ' (' + self.postal_code + ') '
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

class Employee(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=13)
    employee_type = models.CharField(max_length=13) 
    location = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name

class ItemPrices(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.CharField(max_length=50)

class Stock(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,default=2)
    quantity_type = models.CharField(max_length=15)
    reorder_level = models.IntegerField(default=10, null=True, blank=True) 


class OrderStatus(models.Model):
    status = models.CharField(max_length=50) #the string is already defined
    abbv = models.CharField(max_length=6)  #can use the abbreviation to set the status : PEND, APPV, PAPPV, DECL, RETRND, DELET, REFERD
                                            # get the object through OrderStatus.objects.get(abbv=PEND) gives Pending object
class RequestOrders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    expected_date = models.CharField(max_length=50,null=True)
    comment = models.CharField(max_length=50, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE,default=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE,null=True,default='pending')
    auto_genarated=models.BooleanField(default=False)
    

class Orders(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    remaining_quantity=models.IntegerField(null=True)
    quantity_type = models.CharField(max_length=15, null=True, blank=True)
    price = models.FloatField(null=True, blank=True) 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    delivery_date = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    request = models.ForeignKey(RequestOrders, on_delete=models.CASCADE)

class DeliveryLog(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE,null=True)
    purchased_orders=models.ForeignKey(Orders,on_delete=models.CASCADE,null=True)
    date = models.CharField(max_length=50)
    quantity = models.IntegerField(blank=True,null=True)
    qnty_type=models.CharField(max_length=50,null=True)
      


