from django.urls import path
from . import views

urlpatterns = [ 
    path('my_details/',views.my_details, name = 'my_details'),
    path('change_password/', views.change_password, name= 'change_password'),
    path('manage_address/', views.manage_address, name = 'manage_address'),
    path('edit_details/', views.edit_details, name='edit_details'),
]