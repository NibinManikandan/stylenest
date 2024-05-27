from django.urls import path
from . import views

urlpatterns = [ 
    path('my_details/',views.my_details, name = 'my_details'),
    path('change_password/', views.change_password, name= 'change_password'),
    path('add_address/', views.add_address, name = 'add_address'),
    path('edit_details/', views.edit_details, name='edit_details'),
    path('del_address/<str:id>/', views.del_address, name='del_address'),
    path('edit_address/<str:id>/', views.edit_address, name='edit_address'),
]