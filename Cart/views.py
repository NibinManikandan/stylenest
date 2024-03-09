from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse
from .models import Cart
from userAuth.models import *
from Admin_home.models import *
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime
from Userprofile.models import *
from django.views.decorators.cache import cache_control



# rendering cart page with cart details
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cart_page(request):
    email = request.session.get('user')

    if email:
        user = get_object_or_404(CustomUser, email = email)
        cart_items = Cart.objects.filter(user=user).order_by('id')
        subPrice = sum(cart_items.values_list('cart_price', flat=True))
        print(subPrice,'this is subprice')
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
            print('-------------------')
            user_email = request.session['user']
            user = CustomUser.objects.filter(email=user_email).first()
            if user:
                change = request.POST.get('change')
                cart_id = request.POST.get('id')
                print(change)
                print(cart_id)
                cart = get_object_or_404(Cart, id=cart_id, user=user)
                print(cart)
                prod_obj = cart.product
                print(prod_obj.stock)
                if change == str(1):
                    print('inside')
                    if prod_obj.stock > cart.quantity:
                        cart.quantity += 1
                        cart.cart_price=cart.product.Pro_price*cart.quantity
                else:
                    if cart.quantity > 1:
                        cart.quantity -= 1
                        cart.cart_price=cart.product.Pro_price*cart.quantity
                    else:
                        cart.quantity = 1
                        cart.cart_price=cart.product.Pro_price*cart.quantity



                cart.save()

                # total = cart.cart_price * cart.quantity
                user_cart = Cart.objects.filter(user=user)
                sub_total = sum(user_cart.values_list('cart_price', flat=True))
                print(sub_total,'this one')

                response_data = {'updateQuantity': cart.quantity, 'total': cart.cart_price, 'subTotal': sub_total}
                print(response_data)
                return JsonResponse({'success':True,'datas':response_data})
            else:
                return JsonResponse({'success':False,'message': 'User not found'}, status=400)
        else:
            return JsonResponse({'success':False,'message': 'User not logged in'}, status=400)
    else:
        return redirect('Userlogin')