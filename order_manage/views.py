import email
from itertools import product
from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
import requests
from django.db import transaction

from coupon.models import Coupons
from wallet.models import Wallet
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
    if request.user:
        email = request.user
        user = CustomUser.objects.get(email=email)
        orders = Order.objects.filter(user=user)
        order_items = Order_item.objects.filter(order__in = orders).order_by('-id')
        order_items = order_items.filter(ord_product__is_listed=True)
        
    return render(request, 'platform/order_details.html',{"order_items":order_items})



# function for order confirmed page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_order(request):
    order_id = request.session.get('order_id')
    ord_details = Order.objects.get(order_id=order_id)
    current_order = Order_item.objects.filter(order=ord_details)
    current_order = current_order.filter(ord_product__is_listed=True)

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
    order_details = order_details.filter(ord_product__is_listed=True)
    invoice_details = Order.objects.get(order_id=order_id)
    context = {
        "order_details":order_details,
        "invoice_details":invoice_details
    }
    return render(request, 'platform/invoice.html', context)



# function for cancel the order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cancel_order(request, id):
    if request.user:
        email = request.user
        user=CustomUser.objects.get(email=email)
        order = Order_item.objects.get(id=id)
        order.status = "Cancelled"

        if order.order.pyment_mode == 'COD':
            order.ord_product.stock += order.ord_quantity
            order.ord_product.save()
            order.save()
            
        elif order.order.pyment_mode == 'wallet':
            order.ord_product.stock += order.ord_quantity
            print('quantity is the',order.ord_quantity)
            amount = order.ord_product.Pro_price * order.ord_quantity
            print('the product price',order.ord_product.Pro_price)
            print(amount)

            user_wallet = Wallet.objects.filter(user=user).order_by('-id').first()

            if user_wallet:
                balance=user_wallet.balance
            else:
                balance=0

            used_coupon = request.session.get('used_coupon')
            coupon = Coupons.objects.filter(code=used_coupon).first()
            
            if coupon:
                amount = amount - coupon.discount_value
                new_balance = (balance + amount)

            else:
                new_balance = balance + amount

            print(new_balance)

            Wallet.objects.create(
                user=user,
                amount=amount,
                balance=new_balance,
                transaction_type="Credit",
                transaction_details=f"Received Money through Order Cancel",
            )
            order.save()
            order.ord_product.save()

            return JsonResponse({'success': False, 'message': 'This order cannot be cancelled as it was not paid via Cash on Delivery.'}, status=400)

    return JsonResponse({'success': False, 'message': 'Order not found.'}, status=400)
   



# function for return product
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def return_order(request, id):
    if request.user:
        email = request.user
        user = CustomUser.objects.get(email=email)

        order = Order_item.objects.get(id=id)
        order.status = "Returned"
        order.ord_product.stock += order.ord_quantity
        
        amount = order.price * order.ord_quantity

        user_wallet = Wallet.objects.filter(user=user).order_by('id').first()

        if not user_wallet:
            balance = 0
        else:
            balance = user_wallet.balance

        new_balance = balance + amount
        Wallet.objects.create(
            user = user,
            amount = amount,
            balance = new_balance,
            transaction_type = 'Credit',
            transaction_details = f"Refund amount received"
        )

        order.save()
        order.ord_product.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Order not found.'}, status=400)