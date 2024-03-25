from django.urls import path
from . import views



urlpatterns = [
    path('orders/', views.orders, name='orders'),
    path('view_order/', views.view_order, name='view_order'),
    path('cancel_order/<str:id>', views.cancel_order, name='cancel_order'),
    path('return_order/<str:id>', views.return_order, name='return_order'),
    path('invoice/', views.invoice, name='invoice')
]