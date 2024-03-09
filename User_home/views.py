from django.shortcuts import render
from Admin_home.models import *
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.


# home page 
def Home(request):
    return render(request, 'platform/home.html')

# product page
def Shop(request):
    product = Product.objects.filter(is_listed = True)
    return render(request, 'platform/shop.html', {'products':product})

# product details page
def Product_Details(request, id):
    product = Product.objects.get(id=id)
    cate = Category.objects.filter(is_listed = True)
    image_list = Product_Image.objects.filter(product=product)
    print(product)
    return render(request, 'platform/product_detail.html',{'products':product,'images':image_list})


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
