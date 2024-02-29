from django.shortcuts import render
from Admin_home.models import *

# Create your views here.



def Home(request):
    return render(request, 'platform/home.html')


def Shop(request):
    product = Product.objects.filter(is_listed = True)
    return render(request, 'platform/shop.html', {'products':product})


def Product_Details(request, id):
    product = Product.objects.get(id=id)
    cate = Category.objects.filter(is_listed = True)
    image_list = Product_Image.objects.filter(product=product)
    print(product)
    return render(request, 'platform/product_detail.html',{'products':product,'images':image_list})