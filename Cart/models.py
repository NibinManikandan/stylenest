from django.db import models
from Admin_home.models import Product, Category
from userAuth.models import CustomUser

# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, null = True, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, null = True, on_delete = models.CASCADE)
    categorye = models.ForeignKey(Category, null = True, on_delete = models.CASCADE)
    cart_quantity = models.PositiveIntegerField(null = True, blank = False, default = 1)
    cart_price = models.PositiveIntegerField(default = 1)
    created_at = models.DateTimeField(auto_now_add = True, null = True)


    def __str__(self):
        return f"{self.user}'s {self.product} in Cart"