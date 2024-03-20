from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Coupons
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib import messages

# Create your views here.

# function for listing coupons
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def coupons(request):
    coupons = Coupons.objects.all().order_by('id')
    context = {'coupons':coupons}
    return render(request, 'admin_panel/coupon.html', context)



# function for adding coupons
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def add_coupons(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']
        discount = request.POST['discount_value']
        min_purchase = request.POST.get('min_purchase', 0)
        expiry_date = request.POST['expiry_date']
        usage_limit = request.POST['usage_limit']

        if Coupons.objects.filter(name=name).exists():
            messages.error(request, "Name already exist")
            return redirect('add_coupons')
        
        if Coupons.objects.filter(code=code):
            messages.error(request, "Code already exist")
            return redirect('add_coupons')
        
        Coupons.objects.create(
            name = name,
            code = code,
            discount_value=discount,
            min_purchase=min_purchase,
            expiry_date=expiry_date,
            usage_limit=usage_limit,
        )

        return redirect('coupons')
    
    return render(request, 'admin_panel/add_coupons.html')



# function for edit coupons
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def edit_coupons(request, id):
    coupon = Coupons.objects.filter(id=id).first()
    if request.method == "POST":
        name = request.POST["name"]
        code = request.POST["code"]
        discount = request.POST["discount_value"]
        min_purchase = request.POST.get("min_purchase", 0)
        expiry_date = request.POST["expiry_date"]
        usage_limit = request.POST["usage_limit"]

        # Check if the new name or code already exists (excluding the current coupon being edited)
        if Coupons.objects.filter(name=name).exclude(id=id).exists():
            messages.error(request, "Coupon with this name already exists.")
            return redirect("edit_coupons", id=id)

        if Coupons.objects.filter(code=code).exclude(id=id).exists():
            messages.error(request, "Coupon with this code already exists.")
            return redirect("edit_coupons", id=id)

        coupon.name = name
        coupon.code = code
        coupon.discount_value = discount
        coupon.min_purchase = min_purchase
        coupon.expiry_date = expiry_date
        coupon.usage_limit = usage_limit
        coupon.save()
        return redirect("coupons")

    return render(request, "admin_panel/edit_coupon.html", {"coupon": coupon})



# function for coupon Status
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@user_passes_test(lambda u: u.is_superuser, login_url="admin_login")
def coupon_status(request, id):
    coupon = Coupons.objects.filter(id=id).first()
    if coupon.is_active == True:
        coupon.is_active = False
        coupon.save()
    else:
        coupon.is_active = True
        coupon.save()
    return redirect("coupons")


