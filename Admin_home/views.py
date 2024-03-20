from django.shortcuts import render, redirect
from Admin_home.models import Category, Product, Product_Image
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from userAuth.models import CustomUser
from django.contrib import messages


# Create your views here.

# admin login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u:u.is_superuser, login_url='admin_login')

def Dashboard(request):
    return render(request, "admin_panel/dashboard.html")



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
        print(stock)
        print('--------------------------')
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



# admin_logout
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url='admin_login')

def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')