from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null = True, blank = True)
    name = models.CharField(max_length = 80, null = True)
    email = models.CharField(max_length = 50, null = True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 80, null = True)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    digital = models.BooleanField(default = False, null = True, blank = False)
    image = models.ImageField(null = True, blank = True)

    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null = True)
    dateOrdered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    transactionId = models.CharField(max_length = 80, null = True)

    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def getCartTotal(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderItems])
        return total

    @property
    def getCartItems(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank = True, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    dateAdded = models.DateTimeField(auto_now_add = True)

    @property 
    def getTotal(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True)
    address = models.CharField(max_length = 100, null = False)
    city = models.CharField(max_length = 100, null = False)
    state = models.CharField(max_length = 100, null = False)
    zipCode = models.CharField(max_length = 100, null = False)
    dateAdded = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.address