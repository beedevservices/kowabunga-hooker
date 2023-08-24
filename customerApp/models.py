from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from storeApp.models import *
import datetime

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}
        emailCheck = self.filter(email=form['email'])
        if emailCheck:
            errors['email'] = 'Email already in use'
        if form['password'] != form['confirm']:
            errors['password'] = 'Passwords do not match'
        return errors
    
class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    age = models.DateField(blank=True, null=True)
    password = models.CharField(max_length=255)

    objects = UserManager()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def register(self):
        self.save()

    def __str__(self):
        return self.firstName
    def fullName(self):
        return f'{self.firstName} {self.lastName}'
    

class Profile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    address01 = models.CharField(max_length=255, blank=True)
    address02 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f'{self.user.firstName} Profile'
    def address(self):
        return f'{self.address01} {self.address02} {self.city} {self.state} {self.zip}'
    def tel(self):
        return self.phone

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

class LineItem(models.Model):
    product = models.ForeignKey(Product, related_name='theProd', on_delete=CASCADE)
    customer = models.ForeignKey(User, related_name='theUser', on_delete=CASCADE)
    quantity = models.IntegerField(default=1)
    linePriceTotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.product} {self.quantity} {self.linePriceTotal}'


class Order(models.Model):
    customer = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    orderNumber = models.CharField(max_length=255)
    items = models.ManyToManyField(LineItem)
    orderTotal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField (default=datetime.datetime.today)
    notes = models.TextField(null=True, blank=True)
    status = models.BooleanField (default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.customer.firstName} {self.customer.lastName} - {self.orderNumber}'

    def placeOrder(self):
        self.save()

class Invoice(models.Model):
    orderNumber = models.CharField(max_length=255)
    theCustomer = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    cart = models.OneToOneField(Order, unique=True, on_delete=models.CASCADE)
    orderDate = models.DateField (default=datetime.datetime.today)
    pdf = models.FileField(upload_to='invoices')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.lastName} - {self.orderNUmber}'