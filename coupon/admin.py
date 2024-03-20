from django.contrib import admin

from coupon.models import *

# Register your models here.
admin.site.register(Coupons)
admin.site.register(CouponUsage)