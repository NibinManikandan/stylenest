from django.views.generic import RedirectView
from django.urls import path
from . import views



urlpatterns = [
    path('', views.Home, name='home'),
    path('shop/', views.Shop, name = 'shop'),
    path('prod_details/<str:id>', views.Product_Details, name = 'prod_details'),
    path('search_products/', views.search_products, name = 'search_products'),
    path('filtter/', views.filtter, name = 'filtter'),
 
]