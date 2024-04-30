from itertools import product
from django.shortcuts import render, redirect,get_object_or_404
from Admin_home.models import *
from userAuth.models import CustomUser
from wallet.models import Wallet
from wishlist.models import Wishlist
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# function for view wishlist
def wishlist(request):
    if 'user' in request.session:
        email = request.session['user']
        user = CustomUser.objects.get(email=email)
        wishlist = Wishlist.objects.filter(user=user).order_by('-id')

        page_number = request.GET.get('page', 1)
    
        paginator = Paginator(wishlist, 5)
        
        try:
            wishlist = paginator.page(page_number)

        except PageNotAnInteger:
            wishlist = paginator.page(1)

        except EmptyPage:
            wishlist = paginator.page(paginator.num_pages)


        return render(request, 'platform/wishlist.html', {"wishlist":wishlist})
    
    return redirect('Userlogin')
        


# function for add to wishlist
def add_to_wishlist(request):
    if request.method == 'POST':
        if 'user' in request.session:
            email = request.session['user']
            user = CustomUser.objects.get(email=email)
            prod_id = request.POST.get('id')
            products = get_object_or_404(Product, id=prod_id)
            
            if Wishlist.objects.filter(user=user, product=products).exists():
                return JsonResponse({'success':False,'status' : "Product already in Wishlist"})
            else:
                Wishlist.objects.create(
                    user=user, 
                    product=products,
                )
                return JsonResponse({"status": "Product added successfully", "success": True})
        else:
            return redirect('Userlogin')
    else:
        return render(request, 'platform/home.html')
    



# function for remove item from wish list
def remove_wish(request, id):
    wishlist_item = get_object_or_404(Wishlist, id=id)
    if wishlist_item.user != request.user:
        return redirect('home') 

    wishlist_item.delete()
    return redirect('wishlist')