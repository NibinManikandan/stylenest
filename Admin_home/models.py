from email.policy import default
from django.db import models
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    C_name = models.CharField(max_length=100, unique=True)
    C_description = models.TextField(blank=True)
    C_image = models.ImageField(upload_to='category/', blank=True)
    is_listed = models.BooleanField(default=True) 
    Cate_offer = models.IntegerField(null=True)
    


    def __str__(self):
        return f'{self.C_name}'

class Product(models.Model):
    Pro_name = models.CharField(max_length = 100, unique=True)
    Pro_description = models.TextField(blank = True)
    Pro_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    category = models.ForeignKey(Category, null = True, on_delete = models.CASCADE)
    is_listed = models.BooleanField(default=True) 
    stock = models.PositiveIntegerField(blank = True, null = True)
    Pro_offer = models.IntegerField(default=0)
    
    


    def discount(self):
        discount_percentage = 0

        if self.Pro_offer > self.category.Cate_offer:
            discount_percentage = self.Pro_offer
        else:
            discount_percentage = self.category.Cate_offer
        return discount_percentage
    

    def discounted_price(self):
        if self.discount() > 0:
            return  ((self.Pro_price/100 )* self.discount())
        else:
            return self.Pro_price


    def __str__(self):
        return self.Pro_name
        

class Product_Image(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'images')
    Pro_image = models.ImageField(upload_to='Product_images/')


    def __str__(self):
        return f'Image of {self.product.Pro_name}'
