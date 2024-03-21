from unicodedata import category
from django.db import models
from userAuth.models import CustomUser
from Admin_home.models import Product

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.user.first_name}'s wishlist item - {self.product.Pro_name} - {self.product.Pro_price}"
    