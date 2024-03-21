from itertools import product
from django.shortcuts import render, redirect
from Admin_home.models import *
from userAuth.models import CustomUser
from wallet.models import Wallet
from wishlist.models import Wishlist
from django.http import JsonResponse

# Create your views here.


# function for view wishlist
def wishlist(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        wishlist = Wishlist.objects.filter(user=user).order_by('-id')

        return render(request, 'platform/wishlist.html', {"wishlist":wishlist})
    
    return redirect('Userlogin')
        


# function for add to wishlist
def add_to_wishlist(request):
    if request.method == 'POST':
        if 'user' in request.session:
            email = request.session['user']
            user = CustomUser.objects.get(email=email)
            prod_id = int(request.POST.get('product_id'))
            products = Product.objects.get(id=prod_id)

            if (Wallet.objects.filter(user=user, product=products).first()):
                return JsonResponse({'success':False,'status' : "Product already in Wishlist"})
            else:
                Wishlist.objects.create(user=user, product=products)
                return JsonResponse({"status": "Product added successfully", "success": True})
        else:
            return redirect('Userlogin')
    else:
        return render(request, 'platform/home.html')
    



# function for remove item from wish list
def remove_wish(request, id):
    item = Wishlist.objects.get(id=id)
    item.delete()
    return redirect('wishlist')