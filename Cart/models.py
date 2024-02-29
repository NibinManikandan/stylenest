from django.db import models
from Admin_home.models import Product, Category
from userAuth.models import CustomUser

# Create your models here.


class Cart(models.Model):
    customuser = models.ForeignKey(CustomUser, null = True, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = True, on_delete = models.CASCADE)
    quantity = models.PositiveIntegerField(null = True, blank = False, default = 1)
    cart_price = models.PositiveIntegerField(default = 1)