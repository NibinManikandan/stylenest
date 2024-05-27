from django.db import models
from userAuth.models import *

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=50)
    street_address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.IntegerField()
    landmark = models.TextField(blank=True, null=True)
    is_listed = models.BooleanField(default=True)

    def __self__(self):
        return f"Address for {self.user}"