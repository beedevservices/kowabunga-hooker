import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save

class UserManager(models.Manager):
    def validate(self, form):
        errors = {}

        usernameCheck = self.filter(username=form['username'])
        if usernameCheck:
            errors['username'] ='Sorry that username has been taken please chose a different one'

        if len(form['password']) < 6:
            errors['password'] = 'Password must be at least 5 characters long'
        
        if form['password'] != form['confirm']:
            errors['password'] = 'Password do not match'

        return errors

class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    level = models.IntegerField(default=1)

    objects = UserManager()

    userCreatedAt = models.DateTimeField(auto_now_add=True)
    userUpdatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
    def fullName(self):
        return f'{self.firstName} {self.lastName}'

class Profile(models.Model):
    img = models.ImageField(upload_to='userProfileImgs', default='logo.jpg')
    user = models.OneToOneField(User, unique=True, on_delete=CASCADE)

    def __str__(self):
        return f'{self.user.username} Profile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)
        post_save.connect(create_user_profile, sender=User)

class Category(models.Model):
    name = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)
    info = models.TextField()
    category = models.ForeignKey(Category, related_name='theCategory', on_delete=CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Upload(models.Model):
    img = models.ImageField(upload_to='productImgs', default='logo.jpg')
    mainImg = models.OneToOneField(Product, unique=True, on_delete=CASCADE)
    def __str__(self):
        return f'{self.product.img} Upload'

def create_prod_profile(sender, instance, created, **kwargs):
    if created:
        Product.objects.create(products=instance)
        post_save.connect(create_prod_profile, sender=Product)

class Images(models.Model):
    img = models.ImageField(upload_to='productImgs', default='logo.jpg')
    prod = models.ForeignKey(Product, related_name='prodImg', on_delete=CASCADE)
