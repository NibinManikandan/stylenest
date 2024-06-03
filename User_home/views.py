from django.shortcuts import render, redirect
from Admin_home.models import *
from decimal import Decimal
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import check_password
from userAuth.models import *
from Userprofile.models import *
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


# home page 
def Home(request):
    banners = Banner.objects.filter(is_listed=True).all()
    return render(request, 'platform/home.html', {'banners':banners})

# product page
def Shop(request):
    products = Product.objects.filter(is_listed=True).all()
    page_number = request.GET.get('page', 1)
    
    paginator = Paginator(products, 12)
    
    try:
        products = paginator.page(page_number)

    except PageNotAnInteger:
        products = paginator.page(1)

    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, 'platform/shop.html', {'products':products})



# product details page
def Product_Details(request, id):
    product = Product.objects.get(id=id)
    cate = Category.objects.filter(is_listed = True)
    image_list = Product_Image.objects.filter(product=product)

    offer_price = product.discounted_price()

    context={
        'product':product,
        'images':image_list,
        'cate':cate,
        'offer_price':offer_price,
        }
    return render(request, 'platform/product_detail.html', context)


# Search function
def search_products(request):
    search = request.GET['search']
    products = Product.objects.filter(Pro_name__icontains = search)
    categories = Category.objects.filter(C_name__icontains = search)
    context = {
        'products' : products,
        'allCategories' : categories
    }

    return render(request, 'platform/shop.html', context)




def filtter(request):
    cat = request.GET.get('categoryy', '0')
    sort = request.GET.get('sort')

    products = Product.objects.filter(is_listed=True)

    if cat != '0':
        products = products.filter(category__id=cat)

    if sort == 'low_to_high':
        products = products.order_by('Pro_price')
    elif sort == 'high_to_low':
        products = products.order_by('-Pro_price')
    else:
        products = products.order_by('-id')

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'cat': cat,
        'sort': sort
    }

    return render(request, 'platform/shop.html', context)



# function for about us
def about_us(request):
    return render(request, 'platform/about_us.html')


# function for contact us
def contact(request):
    return render(request, 'platform/contact.html')
