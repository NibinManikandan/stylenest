from django.urls import path
from . import views
from django.conf.urls import handler404
from django.shortcuts import render

def custom_page_not_found_view(request, exception):
    return render(request, "404.html", {})

handler404 = custom_page_not_found_view

urlpatterns = [
    path('wallet/',views.wallet,name='wallet'),
    path('add_amount/',views.add_amount, name="add_amount"),
    path('update_wallet/', views.update_wallet, name='update_wallet'),
]
