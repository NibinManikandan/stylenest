from django.urls import path
from . import views




urlpatterns = [
    path('admin_login/', views.Admin_Log, name='admin_login'),
    
]