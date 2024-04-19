from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.



class CustomUser(AbstractUser):
    phone = models.CharField(max_length = 12, unique=True, null = False)
    otp = models.CharField(max_length = 6)
    date_of_join = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.username


