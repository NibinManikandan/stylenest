from django.urls import path
from . import views

urlpatterns = [ 
    path('cart_page/', views.cart_page, name = 'cart_page'),
    path('add_to_cart/', views.add_to_cart, name = 'add_to_cart'),
    path('remove_item_cart/',views.remove_item_cart, name = 'remove_item_cart'),
    path('update_cart/', views.update_cart, name = 'update_cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('add_address/', views.add_address, name='add_address'),
    path('place_order/', views.place_order, name='place_order'),
    path('apply_coupons/', views.apply_coupons, name='apply_coupons'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    
]

