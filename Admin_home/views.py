from itertools import product
from multiprocessing import context
from django.utils import timezone
from tkinter.tix import Tree
from django.db.models import Sum, Count
from unicodedata import category
from django.shortcuts import render, redirect
from Admin_home.models import Category, Product, Product_Image
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from order_manage.models import Order_item, Order
from userAuth.models import CustomUser
from django.contrib import messages
from django.http import JsonResponse
from wallet.models import Wallet


# Create your views here.

# admin login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def Dashboard(request):
    sort = request.GET.get('sort')
    sales_rate = 0
    revenue_data = 0
    users_data = 0
    if sort == 'today':
        sales_rate = Order.objects.filter(order_date__date=timezone.now().date()).count()
        revenue_queryset = Order.objects.filter(order_date__date=timezone.now().date())
        revenue_data = revenue_queryset.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        users_data = CustomUser.objects.filter(date_of_join=timezone.now().date()).count()
        
    elif sort == 'month':
        sales_rate = Order.objects.filter(order_date__month=timezone.now().month, order_date__year=timezone.now().year).count()
        revenue_queryset = Order.objects.filter(order_date__month=timezone.now().month, order_date__year=timezone.now().year)
        revenue_data = revenue_queryset.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        users_data = CustomUser.objects.filter(date_of_join__month=timezone.now().month, date_of_join__year=timezone.now().year).count()

    elif sort == 'year':
        sales_rate = Order.objects.filter(order_date__year=timezone.now().year).count()
        revenue_queryset = Order.objects.filter(order_date__year=timezone.now().year)
        revenue_data = revenue_queryset.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        users_data = CustomUser.objects.filter(date_of_join__year=timezone.now().year).count()

    else:
        sales_rate = Order.objects.filter(order_date__date=timezone.now().date()).count()
        revenue_queryset = Order.objects.filter(order_date__date=timezone.now().date())
        revenue_data = revenue_queryset.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
        users_data = CustomUser.objects.filter(date_of_join=timezone.now().date()).count()

    # top selling products
    top_sell_prod = Order_item.objects.values('ord_product__Pro_name') \
        .annotate(total_sales=Sum('ord_quantity')) \
        .order_by('-total_sales')[:5]
    
    product_names = [item['ord_product__Pro_name'] for item in top_sell_prod]
    sales_data = [item['total_sales'] for item in top_sell_prod]

    # top selling categories
    top_sell_category = Order_item.objects.values('category_name__C_name') \
        .annotate(total_sales=Sum('ord_quantity')) \
        .order_by('-total_sales')[:5]
    
    category_name = [item['category_name__C_name'] for item in top_sell_category]
    sale_data = [item['total_sales'] for item in top_sell_category]

    context = {
        'sales_rate': sales_rate,
        'revenue_data': revenue_data,
        'users_data': users_data,
        'product_names': product_names,
        'sales_data': sales_data,
        'category_name':category_name,
        'sale_data':sale_data
    }

    return render(request, 'admin_panel/dashboard.html', context)




# listing users in admin
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def User_list(request):
    Users = CustomUser.objects.all().exclude(is_superuser=True).order_by('id')
    return render(request, "admin_panel/user_list.html", {'Users': Users})



# user status block
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def user_status(request, id):
    user = CustomUser.objects.filter(id=id).first()
    if user.is_active==True:
        user.is_active=False
        user.save()

    else:
        user.is_active=True
        user.save()

    return redirect('users')



# function for showing all catogerys
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_catogory(request):
    category = Category.objects.all().order_by('id')
    return render(request, 'admin_panel/adm_category.html', {'categories': category})



#category status block
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def category_status(request, id):
    category = Category.objects.filter(id=id).first()
    if category.is_listed == True:
        category.is_listed = False
        category.save()

    else:
        category.is_listed = True
        category.save()
        
    return redirect('adm_category')



# edit category block
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def edit_category(request, id):
    category = Category.objects.get(id = id)

    if request.method == 'POST':
        update_name = request.POST.get('category_name')

        if update_name != category.C_name:
            if Category.objects.filter(C_name = update_name).exists():
                messages.error(request, 'Category with the same name already exist')

            else:
                category.C_name = update_name
                category.save()

                return redirect('adm_category')
            
    return render(request, 'admin_panel/edit_category.html', {'category':category})



# add category block
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url= 'admin_login')
def add_category(request):
    if request.method == 'POST':
        new_cate_name = request.POST.get('new_updated_category')

        try:
            exist_product = Category.objects.get(C_name__iexact=new_cate_name)
            messages.error(request, "A Category with the same name already exists.")
            return redirect("add_category")
        except ObjectDoesNotExist:
            pass
        
        Cate = Category(C_name = new_cate_name)
        Cate.save()
        return redirect('adm_category')
    return render(request, 'admin_panel/add_category.html')



# prouct list block
@cache_control(no_cache=True, must_revalidate=True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url= 'admin_login')
def products_list(request):
    product = Product.objects.all().order_by('id')
    return render(request, "admin_panel/product.html", {'product': product})



# product_status block
@cache_control(no_cache=True, must_revalidate=True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url= 'admin_login')
def product_status(request, id):
    P_status = Product.objects.filter(id=id).first()
    if P_status.is_listed == True:
        P_status.is_listed = False
        P_status.save()

    else:
        P_status.is_listed = True
        P_status.save()

    return redirect('adm_products')



# add products block
@cache_control(no_cache=True, must_revalidate=True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url= 'admin_login')
def add_products(request):
    category_list = Category.objects.all()
    context ={
        "cat": category_list,
    }
    if request.method == 'POST':
        Pro_name = request.POST.get('name')
        Pro_description = request.POST.get('description')
        category_id = request.POST.get('category')
        Pro_price = request.POST.get('price')
        stock = request.POST.get('stock')
        # checkthe product already exist with the same name
        try:
            existing_product = Product.objects.get(Pro_name__iexact=Pro_name)
            messages.error(request, 'Product Already exists with the same name.')
            return redirect('add_product')
        except ObjectDoesNotExist:
            pass

        category = Category.objects.get(id=category_id)

        product = Product(
            Pro_name = Pro_name,
            Pro_description = Pro_description,
            category = category,
            Pro_price = Pro_price,
            stock = stock
        )
        
        product.save()

        Pro_images = request.FILES.getlist('images')
        for img in Pro_images:
            Product_Image(product=product, Pro_image=img).save()

        messages.success(request, "Product added Succesfully.")
        return redirect('adm_products')

    return render(request, 'admin_panel/add_product.html', context)



# Edit products
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def Edit_product(request, id):
    Category_list = Category.objects.all()
    prod = Product.objects.get(id=id) 
    pro_img = Product_Image.objects.all()
    context = {'Cat': Category_list, 'Prod': prod,}
    
    if request.method =='POST':
        prod.Pro_name = request.POST.get('name')
        prod.Pro_Discription = request.POST.get('description')
        images  = request.FILES.getlist('images')   
        prod.Pro_price = request.POST.get('price')
        prod.category_id = request.POST.get('category')
        prod.stock = request.POST.get('stock')
        prod.save()

        if images:
            now = Product_Image.objects.filter(product=prod)
            for item in now:
                item.delete()

            for img in images:
                Product_Image(product=prod, Pro_image=img).save()

        return redirect('adm_products')
    
    return render(request, 'admin_panel/edit_product.html', context)



# function for list order items
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def adm_orders(request):
    order_items = Order_item.objects.all().order_by('-id')
    return render(request, "admin_panel/orders.html", {"items": order_items})



# function for change the order status
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def order_status_change(request, id):
    order = Order_item.objects.get(id=id)

    if request.method == 'POST':
        status = request.POST.get('status_change')

        if status == "Cancelled" or status == "Returned":
            if order.order.pyment_mode != 'COD':
                order.status = status
                order.ord_product.stock += order.ord_quantity

                wallet = Wallet.objects.filter(order.order.user).order_by('-id')
                if wallet:
                    balance = wallet.first().balance
                else:
                    balance = 0

                new_balance = balance + order.total_price()

                Wallet.objects.create(
                    user = order.order.user,
                    amount = order.total_price,
                    balance = new_balance,
                    transaction_type = 'Credit',
                    transaction_details = f"Recieved money through Order {status} By Seller"
                )
                order.status = status
                order.ord_product.stock += order.ord_quantity
                order.save()
                order.ord_product.save()
                return redirect("adm_orders")
            
            else:
                order.status = status

                order.save()
                return redirect("adm_orders")
        
        else:
            order.status = status
            order.save()
            return redirect("adm_orders")
        
    return render(request, 'admin_panel/order_info.html', {'obj':order})



# function for check offers
@cache_control(no_cache =True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def offers(request):
    return render(request, 'admin_panel/offers.html')



#function for show available product offers
@cache_control(no_cache =True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def productOffer(request):
    product = Product.objects.filter(Pro_offer__gt = 0)
    return render(request, 'admin_panel/prod_offer.html', {'product':product})



# function for add product offer
@cache_control(no_cache = True, must_revalidate =  True, no_store = True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def addProductOffer(request):
    products = Product.objects.all().order_by('id')

    if request.method == 'POST':
        prod = request.POST.get('product')
        discounted_price = request.POST.get('discount')

        offerProduct = Product.objects.get(id=prod)
        offerProduct.Pro_offer = discounted_price
        offerProduct.save()

        return redirect('productOffer')
    
    return render(request, 'admin_panel/addPordOffer.html',{'products':products})



# function for edit product offer
@cache_control(no_cache = True, must_revaldate = True, no_store = True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_prod_offer(request, id):
    products = Product.objects.all().order_by('id')
    item = Product.objects.get(id=id)

    if request.method == 'POST':
        product_discount = request.POST.get('discount')

        item.Pro_offer = product_discount
        item.save()
        return redirect('productOffer')
    
    return render(request, 'admin_panel/edit_prod_offer.html', {'item':item, 'products':products})



# function for cancell product offer
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def cancel_prod_offer(request, id):
    item = Product.objects.get(id=id)
    item.Pro_offer = 0
    item.save()
    return redirect('productOffer')



# function for add all category offers
@cache_control(no_cache=True, must_revalidate = True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def cateOffer(request):
    category = Category.objects.filter(Cate_offer__gt=0)
    return render(request, 'admin_panel/cate_offer.html',{'category':category})



# function for add cetegory offers
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def add_cate_offers(request):
    categories=Category.objects.all().order_by('id')

    if request.method == 'POST':
        cate = request.POST.get('category')
        cate_offer_val = request.POST.get('category_offer')

        Category_offer = Category.objects.get(id=cate)
        Category_offer.Cate_offer = cate_offer_val
        Category_offer.save()

        return redirect('cateOffer')
    
    return render(request, 'admin_panel/addCateOffer.html', {'categories':categories})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def edit_cate_offer(request, id):
    categories = Category.objects.all().order_by('id')
    item = Category.objects.get(id=id)

    if request.method == 'POST':
        cate_discount = request.POST.get('discount')

        item.Cate_offer = cate_discount
        item.save()
        return redirect(cateOffer)
    
    return render(request, 'admin_panel/edit_cate_offer.html',{'item':item, 'categories':categories})



#function for cancel category offer
@cache_control(no_cache=True, must_revalidate=True, no_sore=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')
def cancel_category_offers(request, id):
    item = Category.objects.get(id=id)
    item.Cate_offer = 0
    item.save()
    return redirect('cateOffer')



# admin_logout
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')