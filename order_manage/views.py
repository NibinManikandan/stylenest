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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_success(request):
    if request.user.is_authenticated:
        order_id = request.user.email
        
        if order_id:
            order=get_object_or_404(Order, order_id=order_id)
            order_item = Order_item.objects.filter(order=order)

            context = {
                'order':order,
                'order_item':order_item
            }

            return render(request, 'platform/conform.htmls', context)
        
        else:
            messages.error(request, 'Invalid or missing order ID in session.')
            return redirect('home')
        

# fucntion for place order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    if request.user.is_authenticated:
        email = request.user.email
        user = get_object_or_404(CustomUser, email=email)
        cart_items = Cart.objects.filter(user=user)
        out_of_stock = [item for item in cart_items if item.quantity > item.product.stock]
        if out_of_stock:
            return JsonResponse({'empty':True ,'message':'Item out of Stock'})
        
        if request.method == 'POST':
            address_id = request.POST.get('address_select')
            payment_mode = request.POST.get('pyment_mode')
            cart_items = Cart.objects.filter(user=user)
            delivery_address = get_object_or_404(Address, user=user, id=address_id)
            coupon_code = request.POST.get('coupon_code')


            if payment_mode == 'cod':
                if cart_items.exists():
                    try:
                        with transaction.atomic():
                            total_price = 0
                            if 'final_amount' in request.session:
                                final_amount = int(request.session['final_amount'])
                            else:
                                total_price = sum(cart_items.values_list('cart_price', flat=True))

                            order = Order.objects.create(
                                user = user,
                                address = delivery_address,
                                payment_mode = payment_mode,
                                ord_quantity = 0,
                                total_price = final_amount if 'final_amount' in request.session else total_price
                            )

                            for cart_item in cart_items:
                                order_item = Order_item.objects.create(
                                    order = order,
                                    price = cart_item.cart_price,
                                    ord_quantity = cart_item.quantity,
                                    status = "Order Confirmed"
                                )

                                products = cart_item.product
                                products.stock -= cart_item.quantity 
                                products.save()


                                order.quantity += order_item.ord_quantity
                                cart_item.delete()

                            order.expected_date = (order.order_date + timedelta(days=7))
                            order.save()
                            request.session['order_id'] = str(order.order_id)

                            response_data = {
                                'success':True,
                                'message':'Your order hasbeen placed Successfully',
                                'order_id':order.order_id
                            }

                            return JsonResponse(response_data)
                    except Exception as e:
                        response_data={
                            'success':False,
                            'message':'An error occured while placing your order'
                        }

                        return JsonResponse(response_data)
                    
                else:
                    response_data = {
                        'success':False,
                        'message':'Your Cart is empty'
                    }

                    return JsonResponse(response_data)
                
        else:
            response_data = {
                'success':False,
                'message':'Please login to Place an order!'
            }

            return JsonResponse(response_data)
        




def confirm(request):
    return render(request, 'platform/conform.html')