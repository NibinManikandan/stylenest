from django.urls import path
from . import views



urlpatterns =[
    path('coupons/', views.coupons, name='coupons'),
    path('add_coupons/', views.add_coupons, name='add_coupons'),
    path('coupons/edit_coupons/<str:id>/', views.edit_coupons, name='edit_coupons'),
    path('coupon_status/', views.coupon_status, name='coupon_status'),
]