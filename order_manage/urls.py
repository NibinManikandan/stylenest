from django.urls import path
from . import views



urlpatterns = [
    path('order_success/', views.order_success, name='order_success'),
    path('place_order/', views.place_order, name='place_order'),
    path('confirm/', views.confirm, name='confirm')
]