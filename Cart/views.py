from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Cart
from userAuth.models import *
from Admin_home.models import *
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta, datetime
from Userprofile.models import *



# cart page
def cart_page(request):
    user = request.user
    cart_item = Cart.objects.filter(customuser=user)
    if cart_item.exists():
        User = request.user
        user = CustomUser.objects.filter(email = User.email).first()
        address = Address.objects.filter(customuser=user)
        total = sum(cart_item.values_list('cart_price', flat=True))
        context = {
            'cart_item' : cart_item,
            'total' : total
        }

    return render(request, 'platform/cart.html', context)



# Add items into cart 
def add_to_cart(request):
    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        id = request.POST.get('id')
        product = Product.objects.get(id = id)


        if product.stock >= quantity:
            if Cart.objects.filter(customuser=request.user, product = product).exists():
                return JsonResponse({'success':False})
            

            # create or upfate cart items
            cart, created = Cart.objects.get_or_create(
                customuser = request.user, product = product,
            )

            price = product.discounted_price()
            cart.quantity = quantity
            cart.cart_price = price * Decimal(quantity)
            cart.save()


            response_data = {
                'success':True,
                'message':'Item added to cart Successfully.'
            }

            return JsonResponse(response_data)
        
        else:
            return JsonResponse({'success': False, 'message': 'Product out of stock'})

    return JsonResponse({'success': False})



# removing cart item
def remove_item_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        try:
            cart_item = Cart.objects.gart(id = item_id)
            cart_item.delete()

            return JsonResponse({"message":"item removed successfully"})
        except Cart.DoesNotExist:
            return JsonResponse({"message": "item not found"}, status=400)
        
    else:
        return JsonResponse({"message": "Invalid request method"}, status=405)
    



# update cart
def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            User = CustomUser.objects.filter(email = user.email).first()
            change = int(request.POST.get('change'))
            cart_id = int(request.POST.get('productId'))
            cart = Cart.objects.get(id = cart_id)


            product_obj = Product.objects.get(id = cart.product.id)

            if change == 1:
                if product_obj.stock > cart.quantity:
                    cart.quantity += 1
                    cart.save()

            else:
                if cart.quantity > 1:
                    cart.quantity -= 1
                    cart.save()

                else:
                    cart.quantity = 1
                    cart.save()


            prodTotal = product_obj.discounted_price() * cart.quantity
            cart.cart_price = prodTotal
            cart.save()
            cart_items = Cart.objects.filter(customuser = user)
            total = sum(cart_items.values_list('cart_price', flat = True))


            responsData = {
                'updatedQuantity':cart.quantity,
                'prodTotal':prodTotal,
                'totalCartPrice':total
            }
            return JsonResponse(responsData)

    return HttpResponse(status=200)





# def checkout(request):
#     if request.user.is_authenticated:
#         user = request.user
#         cart_item = Cart.objects.filter(customuser = user)
#         if cart_item.exists():
#             User = request.user
#             user = CustomUser.objects.filter(email = User.email).first()
#             address = Address.objects.filter(user = user)
#             cart_items = Cart.objects.filter(customuser = user)
#             total = sum(cart_items.values_list('cart_price', flat=True))
