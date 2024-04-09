from django.urls import path
from . import views



urlpatterns = [
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_wish/<str:id>/', views.remove_wish, name='remove_wish')
]
