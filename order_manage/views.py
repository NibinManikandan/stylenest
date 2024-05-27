import email
from itertools import product
from lib2to3.fixes.fix_operator import invocation
from multiprocessing import context
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.views.decorators.cache import never_cache
import coupon
from coupon.models import Coupons, CouponUsage
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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

        page_number = request.GET.get('page', 1)
    
        paginator = Paginator(order_items, 8)
        
        try:
            order_items = paginator.page(page_number)

        except PageNotAnInteger:
            order_items = paginator.page(1)

        except EmptyPage:
            order_items = paginator.page(paginator.num_pages)
            
    return render(request, 'platform/order_details.html',{"order_items":order_items})



# search function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def search(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            order_items = Order_item.objects.filter(ord_product__Pro_name__icontains=query)
            return render(request, 'platform/order_details.html', {'order_items':order_items})
        else:
            return render(request, 'platform/order_details.html')



# function for order confirmed page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def view_order(request):
    flag=request.session.get('flag')
    order_id = request.session.get('order_id')

    if flag == 0:
        ord_details = Order.objects.get(order_id=order_id)
        current_order = Order_item.objects.filter(order=ord_details)
        current_order = current_order.filter(ord_product__is_listed=True)

        context = {
            "current_order": current_order,
            "ord_details": ord_details,
            'flag':0
        }
    else:
        current_order= Order_item.objects.filter(id = order_id)
        current_order = current_order.filter(ord_product__is_listed=True)
        data= Order_item.objects.filter(id = order_id).first()
        ord_details = data.order
        context = {
            "current_order": current_order,
            "ord_details": ord_details,
            "product":data.price * data.ord_quantity,
            'flag':1
        }
    return render(request, 'platform/conform.html', context)



# function for download invoice
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def invoice(request):
    flag=request.session.get('flag')
    order_id = request.session.get('order_id')
    if flag == 0:
        order_details = Order_item.objects.filter(order_id = order_id).all()
        order_details = order_details.filter(ord_product__is_listed=True)
        invoice_details = Order.objects.get(order_id=order_id)
        context = {
            "order_details":order_details,
            "invoice_details":invoice_details,
            'flag':0
        }
    else:
        data= Order_item.objects.filter(id = order_id).first()
        invoice_details = data.order
        data_obj= Order_item.objects.filter(id = order_id)
        order_details =  data_obj

        context = {
            "order_details":order_details,
            "invoice_details":invoice_details,
            "product":data.price * data.ord_quantity,
            'flag':1
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
        delivery_charge = 50

        if order.order.pyment_mode == 'COD':
            order.ord_product.stock += order.ord_quantity
            order.ord_product.save()
            order.save()
            
        elif order.order.pyment_mode == 'wallet' or order.order.pyment_mode == 'razorepay':
            order.ord_product.stock += order.ord_quantity
            amount = order.ord_product.Pro_price * order.ord_quantity
            if amount < 1000:
                amount = amount + delivery_charge
            else:
                amount
        
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
    



# function for track order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def track_order(request,id):
    Orders = get_object_or_404(Order_item, id=id)
    orders = Orders.order
    coupon_used = CouponUsage.objects.filter(user = orders.user, total_amount=Orders.price * Orders.ord_quantity).first()
    context={
        'Orders': Orders,
        'orders': orders,
        'coupon_used':coupon_used
    }
    
    return render(request, 'platform/track_order.html', context)