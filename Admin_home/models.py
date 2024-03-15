from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    C_name = models.CharField(max_length=100, unique=True, null=True)
    C_description = models.TextField(blank=True)
    C_image = models.ImageField(upload_to='category/', blank=True)
    is_listed = models.BooleanField(default=True) 


    def __str__(self):
        return f'{self.C_name}'

class Product(models.Model):
    Pro_name = models.CharField(max_length = 100, unique=True)
    Pro_description = models.TextField(blank = True)
    Pro_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE)
    is_listed = models.BooleanField(default=True) 
    Pro_offer = models.PositiveIntegerField(default = 0)
    stock = models.PositiveIntegerField(blank = True, null = True)


    def discounted_price(self):
        discount_percentage = self.Pro_offer
        if discount_percentage > 0:
            return self.Pro_price - ((self.Pro_price * discount_percentage) / 100)
        else:
            return self.Pro_price


    def __str__(self):
        return self.Pro_name
        

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'images')
    Pro_image = models.ImageField(upload_to='Product_images/')


    def __str__(self):
        return f'Image of {self.product.Pro_name}'
