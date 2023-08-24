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
        return f'{self.user.username} Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)


class Order(models.Model):
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    product = models.ForeignKey(Product, related_name='theProd', on_delete=CASCADE)
    customer = models.ForeignKey(User, related_name='theUser', on_delete=CASCADE)
    date = models.DateField (default=datetime.datetime.today)
    status = models.BooleanField (default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def placeOrder(self):
        self.save()