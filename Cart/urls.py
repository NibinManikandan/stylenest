from django.urls import path
from . import views

urlpatterns = [ 
    path('cart_page/', views.cart_page, name = 'cart_page'),
    path('add_to_cart/', views.add_to_cart, name = 'add_to_cart'),
    path('remove_item_cart/',views.remove_item_cart, name = 'remove_item_cart'),
    path('update_cart/', views.update_cart, name = 'update_cart'),

    path('checkout/', views.checkout, name = 'checkout'),
    path('ship_to_another/', views.ship_to_another, name='ship_to_another'),
    path('place_order/', views.place_order, name='place_order'),
    path('place_order_wallet/', views.place_order_wallet, name='place_order_wallet'),
    path('order_razorpay/', views.order_razorpay, name='order_razorpay'),
    path('order_place/', views.order_place, name='order_place'),

    path('apply_coupons/', views.apply_coupons, name='apply_coupons'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    
]