import email
from itertools import product
from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
import requests
from django.db import transaction
from .models import *
from Cart.models import *
from userAuth.models import *
from Admin_home.models import *
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime
from Userprofile.models import *
from order_manage.models import *
from django.views.decorators.cache import cache_control
from django_countries import countries as django_countries


# Create your views here.

# function for list orders
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def orders(request):
    if 'email' in request.session:
        email = request.session['email']
        user = CustomUser.objects.get(email=email)
        orders = Order.objects.filter(user=user)
        order_items = Order_item.objects.filter(order__in = orders).order_by('-id')
    return render(request, 'platform/order_details.html',{"order_items":order_items})



# function for order confirmed page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_order(request):
    order_id = request.session.get('order_id')
    ord_details = Order.objects.get(order_id=order_id)
    current_order = Order_item.objects.filter(order=ord_details)
    
    # Debugging prints
    print("Order ID:", order_id)
    print("Order Details:", ord_details)
    print("Current Order Items:", current_order)

    context = {
        "current_order": current_order,
        "ord_details": ord_details
    }
    return render(request, 'platform/conform.html', context)



# function for download invoice
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def invoice(request):
    order_id = request.session['order_id']
    order_details = Order_item.objects.filter(order_id = order_id).all()
    invoice_details = Order.objects.get(order_id=order_id)
    context = {
        "order_details":order_details,
        "invoice_details":invoice_details
    }
    return render(request, 'platform/invoice.html', context)



# function for cancel the order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cancel_order(request, id):
    email = request.session['email']
    user = CustomUser.objects.get(email = email)
    order = Order_item.objects.get(id=id)
    order_status = "Cancelled"

    if order.order.payment_method == 'COD':
        order.ord_product.stock += order.ord_quantity
        order.save()
        order.ord_product.save()

    return redirect('orders')


# function for return product
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def return_order(request, id):
    email = request.session['email']
    user = CustomUser.objects.get(email=email)

    order = Order_item.objects.get(id=id)
    order_status = "Returned"
    order.ord_product.stock += order.ord_quantity
    
    amount = order.price * order.ord_quantity

    balance = 0

    order.save()
    order.ord_product.save()
    return redirect('orders')