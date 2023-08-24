from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save

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

