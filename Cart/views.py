from datetime import timedelta
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from coupon.models import CouponUsage, Coupons
from wallet.models import Wallet
from .models import Cart
from userAuth.models import *
from Admin_home.models import *
from django.utils import timezone
from datetime import timedelta, datetime
from Userprofile.models import *
from order_manage.models import *
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache



# function for add items into cart 
def add_to_cart(request):
    if request.method == 'POST':
        if 'user' in request.session:
            email = request.session['user']
            user = get_object_or_404(CustomUser, email=email)
            product_id = request.POST.get('id')
            product = get_object_or_404(Product, id=product_id)

            offer_price = product.discounted_price()

            if offer_price < product.Pro_price and offer_price != 0:
                price = offer_price
            else:
                price = product.Pro_price
            
            # Check if the product is in stock
            if product.stock > 0:
                # Check if the product is already in the user's cart
                if Cart.objects.filter(user=user, product=product).exists():
                    return JsonResponse({'success': False, 'status': "Product already in cart"})
                else:
                    Cart.objects.create(
                        user=user,
                        product=product,
                        categorye = product.category,
                        created_at=timezone.now(),
                        cart_price=price
                    )
                    cart_count_ajax = Cart.objects.filter(user=user).count()
                    return JsonResponse({'status': "Product added successfully", 'success': True, 'cart_count_ajax': cart_count_ajax})
            else:
                return JsonResponse({'success': False, 'status': "Product is out of stock"})
        else:
            return JsonResponse({'success': False, 'status': "Please login to continue."})
    else:
        return render(request, 'platform/home.html')



# rendering cart page with cart details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_page(request):
    email = request.session.get('user')
    if email:
        user = get_object_or_404(CustomUser, email=email)
        cart_items = Cart.objects.filter(user=user).order_by('id')
        cart_items = cart_items.filter(product__is_listed=True)
        subPrice = sum(cart_items.values_list('cart_price', flat=True))
        return render(request, 'platform/cart.html', {'cart_items': cart_items, 'subPrice': subPrice})
    else:
        return redirect('Userlogin')



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
@never_cache
def checkout(request):
    if 'user' in request.session:
        user_email = request.session['user']
        user = CustomUser.objects.get(email=user_email)
        addresses = Address.objects.filter(user=user, is_listed=True).all()   
        obj = Cart.objects.filter(user=user).order_by('id')
        obj = obj.filter(product__is_listed=True)
        sub_total = sum(obj.values_list('cart_price', flat=True))
        cart_items_queryset = Cart.objects.filter(user=user).all()
        cart_items = [item for item in cart_items_queryset]
        current_date = timezone.now().date()
        active_coupons = Coupons.objects.filter(expiry_date__gte=current_date, is_active=True)

        valid_coupons = []
        for coupon in active_coupons:
            if coupon.used_count < coupon.usage_limit:
                valid_coupons.append({
                    'name': coupon.name,
                    'code': coupon.code,
                    'discount_value': coupon.discount_value,
                    'min_purchase': coupon.min_purchase,
                    'expiry_date': coupon.expiry_date,
                    'usage_limit': coupon.usage_limit,
                    'used_count': coupon.used_count,
                    'is_active': coupon.is_active,
                    'created_at': coupon.created_at,
                    'updated_at': coupon.updated_at
                })
        delivery_charge = 0

        if sub_total < 1000 and sub_total > 0:
            delivery_charge = 50
            sub_total = sub_total + delivery_charge
        else:
            sub_total
        
        context = {
            'addresses': addresses, 
            'sub_total': sub_total,
            'obj':obj,
            'valid_coupons':valid_coupons,
            'delivery_charge':delivery_charge,
            'cart_items':cart_items
        }

        return render(request, 'platform/checkout.html', context)
    


# function for add address
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ship_to_another(request):
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

        f_name_stripped = f_name.strip()
        if not f_name_stripped.isalpha() or len(f_name) < 3:
            return redirect('checkout')
        
        l_name_stripped = l_name.strip()
        if not l_name_stripped.isalpha() or len(l_name) < 3:
            return redirect('checkout')
        
        c_address_stripped = c_address.strip()
        if not c_address_stripped or len(c_address) < 6:
            return redirect('checkout')
        
        city_stripped = city.strip()
        if not city_stripped or len(city) < 3:
            return redirect('checkout')
        
        landMark_stripped = landMark.strip()
        if not landMark_stripped or len(landMark) < 3:
            return redirect('checkout')
        
        state_stripped = state.strip()
        if not state_stripped or len(state) < 3:
            return redirect('checkout')
        
        pin_stripped = postal.strip()
        if not pin_stripped.isdigit() or len(postal) != 6:
            return redirect('checkout')
        
        phone_stripped = c_phone.strip()
        if not phone_stripped.isdigit() or len(c_phone) != 10:
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
    
# Function for placing an order
# Function for placing an order
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    if request.user:
        user_email = request.user
        user = CustomUser.objects.get(email=user_email)
        address_id = request.POST.get('selected_address')
        new_address = Address.objects.get(id=address_id)
        payment_method = request.POST.get('payment')
        coupon_code = request.POST.get('couponCode')
        coupon = Coupons.objects.filter(code = coupon_code).first()
        total = 0 

        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            if item.cart_quantity > item.product.stock:
                return JsonResponse({"success":False, "message": "Some items are out of stock"})
              
            else:
                total += ((item.cart_quantity) * (item.product.Pro_price))
 
        if coupon:
            if coupon.min_purchase <= total:
                total -= coupon.discount_value
        
        if total > 1000:
            if cart_items.exists():
                total_quantity = sum(item.cart_quantity for item in cart_items)
                order = Order(
                user=user,
                order_address=new_address,
                pyment_mode=payment_method,
                quantity=total_quantity,
                total_amount = total
                )
                order.save()

                order.expected_date = order.order_date + timedelta(days=7)

                total_quantity = 0
                total = 0

                # Create OrdersItem objects and calculate the total amount and quantity
                for item in cart_items:
                    ord_prod_cate = Category.objects.get(C_name=item.product.category.C_name)
                    order_item = Order_item (
                        order=order,
                        ord_product=item.product,
                        ord_quantity=item.cart_quantity,
                        price=item.product.Pro_price,
                        category_name=ord_prod_cate,
                        status="Order confirmed",
                        payment_status="Pending"
                    )
                    order_item.save()

                    # Calculate the total amount and quantity
                    total += item.cart_quantity * item.product.Pro_price
                    total_quantity += item.cart_quantity

                    # Reduce the quantity of the product in the order
                    prod_quantity = item.product
                    prod_quantity.stock -= item.cart_quantity
                    prod_quantity.save()

                # Update the total_amount and quantity in the order object
                order.quantity = total_quantity
                order.save()

                # Order_id moving to session for further use
                request.session['order_id'] = str(order.order_id)
                request.session['flag']= 0


                # Clearing the cart items after placing the order
                cart_items.delete()

                return JsonResponse({"success": "Order placed successfully"})
            else:
                return JsonResponse({"success": False, "message": "your cart is empty"})
        else:
            return JsonResponse({"success":False, "message":"Orders exceeding 1000 rupees cannot be placed using cash on delivery."})
            
    return JsonResponse({"error": "User not authenticated"}, status = 400)



# function for place order using razorpay
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def order_razorpay(request):
    if request.user:
        email = request.user
        user = CustomUser.objects.filter(email=email).first()
        address_id = request.POST.get('selected_address')
        new_address = Address.objects.get(id=address_id)
        payment_method = request.POST.get('payment')
        coupon_code = request.POST.get('couponCode')
        flag = request.POST.get('flag')
        coupon = Coupons.objects.filter(code = coupon_code).first()
        delivery_charge = 0

        cart_items = Cart.objects.filter(user=user).all()
        total=0
        for item in cart_items:
            if item.cart_quantity > item.product.stock:
                return JsonResponse({"success": False, "message":"Some items are Out of Stock"})
            total += ((item.cart_quantity) * (item.cart_price))
        
        if coupon:
            if coupon.min_purchase <= total:
                total -= coupon.discount_value
        
        if total < 1000 and total > 0:
            delivery_charge = 50
            total +=  delivery_charge

        if cart_items.exists():
            total_quantity = sum(item.cart_quantity for item in cart_items)
            order = Order(
                user=user,
                order_address=new_address,
                pyment_mode=payment_method,
                quantity=total_quantity,
                total_amount=total
                )
            order.save()

            order.expected_date=order.order_date + timedelta(days=7)
            total_quantity=0
            total=0
        
            for item in cart_items:
                ord_prod_cate = Category.objects.get(C_name=item.product.category.C_name)
                order_item = Order_item (
                    order=order,
                    ord_product=item.product,
                    ord_quantity=item.cart_quantity,
                    price=item.product.Pro_price,
                    category_name=ord_prod_cate,
                    status="Order pending",
                    payment_status="Pending"
                )
                order_item.save()

                total += item.cart_quantity * item.product.Pro_price
                total_quantity += item.cart_quantity

                # Reduce the quantity of the product in the order
                prod_quantity = item.product
                prod_quantity.stock -= item.cart_quantity
                prod_quantity.save()

                # Update the total_amount and quantity in the order object
            order.quantity = total_quantity
            order.save()

            request.session['order_id'] = str(order.order_id)
            request.session['flag']= 0


            cart_items.delete()
            data = {'success':True,'amount':int(total*100), "currency":"INR",'order_id':order.order_id}

            return JsonResponse(data)
        else:
            return JsonResponse({'success': False, 'message':'Your catr is empty'})

        
def payment_confirm(request):
    if Order.total_amount < 20000:
        order_id = request.POST.get('order_id')
        product=Order.objects.filter(order_id=order_id).first()
        order_items=Order_item.objects.filter(order=product).all()
        for items in order_items:
            items.status='Order confirmed'
            items.payment_status='Paid'
            items.save()
        return JsonResponse({'success':True,"message":"Product ordered Successfully"})
    else:
        return redirect('checkout')


def repayment(request):
    order_id = request.POST.get('order_id')
    items=Order_item.objects.filter(id=order_id).first()
    if items.ord_product.stock != 0:
        items.status='Order confirmed'
        items.payment_status='Paid'
        items.save()
        request.session['order_id'] = order_id
        request.session['flag'] = 1
        return JsonResponse({'success':True,"message":"Payment is Successfull"})
    else:
        return JsonResponse({'success':False,"message":"We're sorry, but this product is currently unavailable."})



# function for place order wallet
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order_wallet(request):
    if request.user.is_authenticated:
        user = request.user
        address_id = request.POST.get('selected_address')
        new_address = Address.objects.get(id=address_id)
        payment = request.POST.get('payment')
        couponCode = request.POST.get('couponCode')
        coupon = Coupons.objects.filter(code=couponCode).first()
        request.session['used_coupon']=couponCode
        delivery_charge = 50
        
        cart_items = Cart.objects.filter(user=user)
        for item in cart_items:
            if item.cart_quantity > item.product.stock:
                return JsonResponse({"success": False, "message": "Some items are Out of Stock"})
                
        if cart_items.exists():
            wallet = Wallet.objects.filter(user=user).order_by('-id')
            if wallet:
                balance = wallet.first().balance
            else:
                balance = 0

            total_cart_price = sum(cart_items.values_list("cart_price", flat=True))
            if total_cart_price < 1000:
                total_cart_price = total_cart_price + delivery_charge
            else:
                total_cart_price=total_cart_price
            total_coupon_amount = total_cart_price # Initialize total_coupon_amount
            
            if coupon:
                total_coupon_amount -= coupon.discount_value

            if balance >= total_coupon_amount:
                order = Order.objects.create(
                    user=user,
                    order_address=new_address,
                    pyment_mode=payment,
                    total_amount=total_coupon_amount,
                    quantity=0  # This needs to be defined before calculating it
                )
                order.expected_date = order.order_date + timezone.timedelta(days=7)

                total_quantity = 0  # Initialize total_quantity
                total_amount = 0  # Initialize total_amount

                for item in cart_items:
                    ord_prod_cate = Category.objects.get(C_name=item.product.category.C_name)
                    order_item = Order_item (
                        order=order,
                        ord_product=item.product,
                        ord_quantity=item.cart_quantity,
                        price=item.product.Pro_price,
                        category_name=ord_prod_cate,
                        status="Order confirmed",
                        payment_status="Pending"
                    )
                    order_item.save()

                    total_amount += item.cart_quantity * item.product.Pro_price
                    total_quantity += item.cart_quantity

                    prod_quantity = item.product
                    prod_quantity.stock -= item.cart_quantity
                    prod_quantity.save()

                order.quantity = total_quantity
                order.total_amount = total_coupon_amount
                order.save()

                new_balance = balance - total_coupon_amount
                Wallet.objects.create(
                    user=user,
                    amount=total_coupon_amount,
                    balance=new_balance,
                    transaction_type="Debit",
                    transaction_details="Debited Money Through Purchase",
                )
                request.session['order_id'] = str(order.order_id)
                request.session['flag']= 0
                cart_items.delete()
                
                return JsonResponse({"success": "Order placed successfully"})
            else:
                return JsonResponse({"success": False, "message": "Insufficient balance in wallet"}, status=400)
            
    return JsonResponse({"error": "User not authenticated"}, status=400)



# function to apply coupon 
def apply_coupons(request):
    if request.method == 'POST':
        if request.user:
            email = request.user
            user = CustomUser.objects.get(email=email)

            coupon_code = request.POST.get('couponCode')
            coupon_check = Coupons.objects.filter(code=coupon_code, is_active = True).first()
            if coupon_check:
                if CouponUsage.objects.filter(user=user, coupon=coupon_check).exists():
                    return JsonResponse({'error': "Coupon already applied."}, status = 400)  
                else:
                    if coupon_check.used_count < coupon_check.usage_limit:
                        cart_total = sum(
                            Cart.objects.filter(user=user).values_list("cart_price", flat=True)
                        )

                        if cart_total >= coupon_check.min_purchase:
                            if coupon_check.expiry_date < datetime.now().date():
                                return JsonResponse({"error": f"Coupon Expired"}, status = 400)
                            
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
                            return JsonResponse({"error": f"Minimum purchase amount of {round(coupon_check.min_purchase)} required"}, status = 400)
                        
                    else:
                        return JsonResponse({"error": "Sorry! This code has reached its usage limit."}, status = 400)
                    
            else:
                return JsonResponse({"error":"Invalid Coupon"}, status = 400)
            
        return JsonResponse({"error":"Inavalid request"}, status = 400)
    



# function to remove coupon 
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
    



# function to show available coupon
def coupon_filtering(request):
    current_date = timezone.now().date()
    active_coupons = Coupons.objects.filter(expiry_date__gte=current_date, is_active=True)

    valid_coupons = []
    for coupon in active_coupons:
        if coupon.used_count < coupon.usage_limit:
            valid_coupons.append({
                'name': coupon.name,
                'code': coupon.code,
                'discount_value': coupon.discount_value,
                'min_purchase': coupon.min_purchase,
                'expiry_date': coupon.expiry_date,
                'usage_limit': coupon.usage_limit,
                'used_count': coupon.used_count,
                'is_active': coupon.is_active,
                'created_at': coupon.created_at,
                'updated_at': coupon.updated_at
            })

    return render(request, 'platform/checkout.html',{'valid_coupons': valid_coupons})