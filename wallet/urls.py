from django.urls import path
from . import views





urlpatterns = [
    path('wallet/',views.wallet,name='wallet'),
    path('add_amount',views.add_amount, name="add_amount"),
]
