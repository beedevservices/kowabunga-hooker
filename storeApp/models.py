from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from customerApp.models import User
import datetime
import string
import random

statusOfOrder = [
    ('New', 'Newly Placed'),
    ('Pending', 'In discussion between Customer and Owner'),
    ('In Progress', 'Item is being created'),
    ('Order Items Created', 'All items in order have been created'),
    ('Shipped', 'Item has been shipped'),
    ('Delivered','Item has been delivered'),
    ('Rejected','Order was Rejected'),
    ('Returned', 'Order was Returned'),
    ('Archived', 'Order was archived')
]
statusOfPay = [
    ('New', 'New Order payment terms not set yet'),
    ('Paid', 'Order is fully Paid for'),
    ('Payment Plan', 'Order is on a payment plan that in still ongoing'),
    ('Billed', 'Final Price determined and sent to customer'),
    ('Unpaid', 'Order remains unpaid'),
    ('On Hold', 'Order is on hold awaiting terms')
]

def genOrderCode():
    N = 4
    res01 = ''.join(random.choices(string.ascii_letters, k=N))
    res02 = ''.join(random.choices(string.ascii_letters, k=N))
    stamp = datetime.date.today()
    orderCode = f'{stamp.year}-{res01}-{stamp.day}-{res02}-{stamp.month}'
    print(orderCode, stamp, res01, res02)
    return orderCode

class Category(models.Model):
    name= models.CharField(max_length=255)
    adultOnly = models.BooleanField(default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @staticmethod
    def getAllCategories():
        return Category.objects.all().values()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0, blank=True, null=True)
    madeToOrder = models.BooleanField(default=0)
    description= models.TextField(max_length=255, default='', blank=True, null= True)
    adultOnly = models.BooleanField(default=1)
    image= models.ImageField(upload_to='products')
    category= models.ForeignKey(Category, related_name='theCategory',on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    @staticmethod
    def getAllProds():
        return Product.objects.all().values()
    
    @staticmethod
    def getAllByCatId(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.getAllProds()
    
    def __str__(self):
        return self.name
    
class ProductImages(models.Model):
    image= models.ImageField(upload_to='products')
    prod = models.ForeignKey(Product, related_name='theProduct', on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


class OrderManager(models.Manager):
    def validate(self):
        orderNum = genOrderCode()
        orderCheck = self.filter(orderNum = orderNum)
        if orderCheck:
            orderNum = genOrderCode()
        return orderNum



class Order(models.Model):
    orderNum = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey(User, related_name='theCustomer', on_delete=CASCADE)
    itemCount = models.IntegerField(blank=True, null=True)
    orderTotal = models.CharField(max_length=255, blank=True, null=True)
    orderStatus = models.CharField(max_length=255, choices=statusOfOrder, default='New')
    paymentStatus = models.CharField(max_length=255, choices=statusOfPay, default='New')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = OrderManager()

    def __str__(self):
        return self.orderNum
        
class OrderItem(models.Model):
    orderNum = models.ForeignKey(Order, related_name='theOrder', on_delete=CASCADE)
    product = models.ForeignKey(Product, related_name='theProd', on_delete=CASCADE)
    quantity = models.IntegerField()
    total = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.orderNum.orderNum} {self.product.name}'
    

class Invoice(models.Model):
    theCustomer = models.ForeignKey(User, related_name='custOrder',on_delete=models.CASCADE)
    cart = models.OneToOneField(Order, on_delete=models.CASCADE)
    orderDate = models.DateField(default=datetime.datetime.today)
    pdf = models.FileField(upload_to='invoices')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.theCustomer.lastName} - {self.cart.orderNum}'