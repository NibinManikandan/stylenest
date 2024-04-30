from unicodedata import category
from django.db import models
from Admin_home.models import *
from Cart.models import Cart
from userAuth.models import *
from Userprofile.models import *
from Admin_home.models import *
import uuid

# Create your models here.

class Order(models.Model):
    order_id = models.CharField(max_length=10, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    pyment_mode = models.CharField(max_length=100, null=False)
    order_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default = 1)
    expected_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, null=False, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)

    def generate_order_id(self):
        return str(uuid.uuid4().hex)[:8]
    

    def __str__(self):
        return f"{self.user.first_name}'s Order | ID : {self.order_id}"
    


class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ord_quantity = models.PositiveBigIntegerField(default=1)
    modified_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Order confirmed')
    ord_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    payment_status = models.CharField(max_length=20, default='Pending')
    status_change_time = models.DateTimeField(auto_now=True)
    

    def total_price(self):
        return self.ord_quantity * self.price
    
    def __str__(self):
        return f"{self.order.user}'s {self.ord_product}"

