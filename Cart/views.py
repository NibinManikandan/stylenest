from datetime import timedelta
from urllib import response
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
import requests

import coupon
from coupon.models import CouponUsage, Coupons
from .models import Cart
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



# rendering cart page with cart details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_page(request):
    email = request.session.get('user')
    if email:
        user = get_object_or_404(CustomUser, email = email)
        cart_items = Cart.objects.filter(user=user).order_by('id')
        subPrice = sum(cart_items.values_list('cart_price', flat=True))
        return render(request, 'platform/cart.html', {'cart_items':cart_items, 'subPrice':subPrice})
    else:
        return redirect('Userlogin')



# function for add items into cart 
def add_to_cart(request):
    if request.method == 'POST':
        if 'user' in request.session:
            email = request.session['user']
            user = CustomUser.objects.get(email = email)
            product_id = request.POST.get('id')
            products = Product.objects.get(id = product_id)
            
            if (Cart.objects.filter(user=user, product = products).first()):
                return JsonResponse({'success':False,'status' : "Product already in cart"})
            else:
                Cart.objects.create(user=user, product=products, created_at =timezone.now(), cart_price = products.Pro_price)
                cart_count_ajax = Cart.objects.filter(user = user).count()
                return JsonResponse({'status' : "Product added successfully",'success':True ,'cart_count_ajax' : cart_count_ajax})
        
        else:
            return redirect('Userlogin')
        
    else:
        return render(request, 'platform/home.html')



# fucntion for remove item from the cart
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_item_cart(request):
    if 'user' in request.session:
        if request.method == 'POST':
            user_email = request.session['user']
            user = CustomUser.objects.filter(email = user_email).first()
            item_id = request.POST.get('item_id')
            
            try:
                cart_item = Cart.objects.get(id=item_id)
                cart_item.delete()
                cart_count = Cart.objects.filter(user = user).count()
                return JsonResponse({'success':True,'cartCount': cart_count, 'message': 'Item removed successfully'})
            except Cart.DoesNotExist:
                return JsonResponse({'success':False,'message': 'Item not found'}, status=400)
            
        else:
            return JsonResponse({'success':False,'message': 'Invalid request method'}, status=405)
        
    else:
        return redirect('Userlogin')



# update cart function
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_cart(request):
    if request.method == 'POST':
        if 'user' in request.session:
            user_email = request.session['user']
            user = CustomUser.objects.filter(email=user_email).first()
            if user:
                change = request.POST.get('change')
                cart_id = request.POST.get('id')
                cart = get_object_or_404(Cart, id=cart_id, user=user)
                prod_obj = cart.product
                if change == str(1):
                    if prod_obj.stock > cart.cart_quantity:
                        cart.cart_quantity += 1
                        cart.cart_price=cart.product.Pro_price*cart.cart_quantity
                else:
                    if cart.cart_quantity > 1:
                        cart.cart_quantity -= 1 
                        cart.cart_price=cart.product.Pro_price*cart.cart_quantity
                    else:
                        cart.cart_quantity = 1
                        cart.cart_price=cart.product.Pro_price*cart.cart_quantity


                cart.save()

                # total = cart.cart_price * cart.quantity
                user_cart = Cart.objects.filter(user=user)
                sub_total = sum(user_cart.values_list('cart_price', flat=True))

                response_data = {'updateQuantity': cart.cart_quantity, 'total': cart.cart_price, 'subTotal': sub_total}
                return JsonResponse({'success':True,'datas':response_data})
            else:
                return JsonResponse({'success':False,'message': 'User not found'}, status=400)
        else:
            return JsonResponse({'success':False,'message': 'User not logged in'}, status=400)
    else:
        return redirect('Userlogin')
    


# function for checkout
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def checkout(request):
    if 'user' in request.session:
        user_email = request.session['user']
        user = CustomUser.objects.get(email=user_email)
        addresses = Address.objects.filter(user=user, is_listed=True).all()   
        obj = Cart.objects.filter(user=user).order_by('id')
        sub_total = sum(obj.values_list('cart_price', flat=True))
        coupons = Coupons.objects.all().order_by('id')
        
        total = sub_total - coupons
        


        context = {
            'addresses': addresses, 
            'sub_total': sub_total,
            'obj':obj,
            'coupons':coupons,
        }

        return render(request, 'platform/checkout.html', context)
    


# function for add address
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_address(request):
    if request.method == "POST":
        user = CustomUser.objects.filter(email = request.user).first()
        country = request.POST.get('country')
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        c_address = request.POST.get('c_address')
        city = request.POST.get('city')
        landMark = request.POST.get('landmark')
        state = request.POST.get('state')
        postal = request.POST.get('postal_zip')
        c_phone = request.POST.get('c_phone')

        if not f_name.isalpha() or len(f_name) < 3:
            return redirect('checkout')
        
        if not l_name.isalpha() or len(l_name) < 3:
            return redirect('checkout')
        
        c_address_stripped = c_address.strip()
        if not c_address_stripped or len(c_address_stripped) < 6:
            return redirect('checkout')
        
        city_stripped = city.strip()
        if not city_stripped or len(city) < 3:
            return redirect('checkout')
        
        landMark_stripped = landMark.strip()
        if not landMark_stripped or len(landMark) < 3:
            return redirect('checkout')
        
        if not country.isalpha() or len(country) < 3:
            return redirect('checkout')
        
        state_stripped = state.strip()
        if not state_stripped or len(state) < 3:
            return redirect('checkout')
        
        if not postal.isdigit() or len(postal) != 6:
            return redirect('checkout')
        
        if not c_phone.isdigit() or len(c_phone) != 10:
            return redirect('checkout')

        
        address_1 = Address.objects.create(
            user = user,
            country = country,
            first_name = f_name,
            last_name = l_name,
            street_address = c_address,
            city = city,
            landmark = landMark,
            state = state,
            pin_code = postal,
            phone = c_phone,

        )
        
        return redirect('checkout')
    
    else:
        return render(request, 'platform/checkout.html')
    


# fucntion for place order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    if request.user:
        user_email = request.user
        user = CustomUser.objects.get(email=user_email)
        address_id = request.POST.get('selected_address')
        new_address = Address.objects.get(id=address_id)
        payment_method = request.POST.get('payment')
        

        cart_items = Cart.objects.filter(user=user)
        print(cart_items)
        for item in cart_items:
            if item.cart_quantity > item.product.stock:
                return JsonResponse(
                   {"success":False, "message": "Some items out of stock"}
                )
            
            
        total_amount_coupon = request.POST.get("total_amount")
        print(total_amount_coupon)
            
        if cart_items.exists():
            total_quantity = sum(item.cart_quantity for item in cart_items)
            order = Order.objects.create(
            user=user,
            order_address=new_address,
            pyment_mode=payment_method,
            quantity=total_quantity,
            total_amount = total_amount_coupon
            )

            order.expected_date = order.order_date + timedelta(days=7)

            total_quantity = 0
            total_amount = 0

            # Create OrdersItem objects and calculate the total amount and quantity
            for item in cart_items:
                order_item = Order_item.objects.create(
                    order=order,
                    ord_product=item.product,
                    ord_quantity=item.cart_quantity,
                    price=item.product.discounted_price(),
                    status="Order confirmed",
                )
                order_item.save()
                print(order_item)

                # Calculate the total amount and quantity
                total_amount += item.cart_quantity * item.product.discounted_price()
                total_quantity += item.cart_quantity

                # Reduce the quantity of the product in the order
                prod_quantity = item.product
                prod_quantity.stock -= item.cart_quantity
                prod_quantity.save()

                # Update the total_amount and quantity in the order object
                order.total_amount = total_amount
                order.quantity = total_quantity
                order.save()

                # Order_id moving to session for further use
                request.session['order_id'] = str(order.order_id)

                # Clearing the cart items after placing the order
                cart_items.delete()

                return JsonResponse({"success": "Order placed successfully"})
            else:
                return JsonResponse({"success": False, "message": "your cart is empty"})
            
        return JsonResponse({"error": "User not authenticated"})
    



# function for apply coupons
def apply_coupons(request):
    if request.method == 'POST':
        if request.user:
            email = request.user
            user = CustomUser.objects.get(email=email)

            coupon_code = request.POST.get('couponCode')
            coupon_check = Coupons.objects.filter(code=coupon_code, is_active = True).first()
            if coupon_check:
                if CouponUsage.objects.filter(user=user, coupon=coupon_check).exists():
                    return JsonResponse({'error': "Coupon already applied."})
                else:
                    if coupon_check.used_count < coupon_check.usage_limit:
                        cart_total = sum(
                            Cart.objects.filter(user=user).values_list(
                            "cart_price", flat=True
                        )
                        )

                        if cart_total >= coupon_check.min_purchase:
                            if coupon_check.expiry_date < datetime.now().date():
                                return JsonResponse({"error": f"Coupon Expired"})
                            
                            total = cart_total - coupon_check.discount_value

                            response_data = {
                                "success":"added",
                                "total":total,
                                "coupon_code":coupon_code,
                                "discount_amount":coupon_check.discount_value,
                            }

                            coupon_check.used_count += 1
                            coupon_check.save()

                            CouponUsage.objects.create(user=user, coupon=coupon_check)

                            return JsonResponse(response_data)
                        
                        else:
                            return JsonResponse({"error": f"Minimum purchase amount of {round(coupon_check.min_purchase)} required"})
                        
                    else:
                        return JsonResponse({"error": "Sorry! This code has reached its usage limit."})
                    
            else:
                return JsonResponse({"error":"Invalid Coupon"})
            
        return JsonResponse({"error":"Inavalid request"})



# function for Remove coupon
def remove_coupon(request):
    if request.user:
        email = request.user
        user = CustomUser.objects.get(email=email)

        coupon_code = request.POST.get("couponCode")
        coupon_check = Coupons.objects.filter(code=coupon_code, is_active=True).first()
        if coupon_check:
            usage_check = CouponUsage.objects.filter(user=user, coupon=coupon_check).first()
            if usage_check:
                coupon_check.used_count -= 1
                coupon_check.save()
                usage_check.delete()

        # Update the cart total
        total = sum(Cart.objects.filter(user=user).values_list("cart_price", flat=True))

        response_data = {"success": "removed", "total": total}
        return JsonResponse(response_data)


