from django.contrib import messages
from django.shortcuts import render,redirect
from userAuth.models import *
from Userprofile.models import *
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.http import JsonResponse, HttpResponse
# Create your views here.



# function to user profile in profile
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def my_details(request):
    if request.user.is_authenticated:
        data = CustomUser.objects.filter(email = request.user).first()

    return render(request, 'platform/my_profile.html', {'data':data})



# order details
def my_orders(request):
    return render(request, 'platform/order_details.html')



# function for edit user peofile
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_details(request):
    if request.user.is_authenticated:
        user = CustomUser.objects.filter(email = request.user).first()
        if request.method == "POST":
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            phone_num = request.POST.get('phone')

            user.first_name = fname
            user.last_name = lname
            user.phone = phone_num
            user.save()

            return redirect('my_details')

    # Render the edit details form template
    return render(request, 'my_profile.html')



# function to change password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            old_pass = request.POST.get('old_pass')
            new_pass = request.POST.get('new_pass')
            cnf_new_pass = request.POST.get('cnf_new_pass')

            if check_password(old_pass, user.password):
                if new_pass == cnf_new_pass:
                    user.set_password(new_pass)
                    user.save()
                    logout(request)

                    return JsonResponse({'valid':True, 'message': 'Password changed successfully'}, status=200)
                else:
                    return JsonResponse({'valid':False, 'message': 'Password and Confirm Password do not match!'}, status=200)
            else:
                return JsonResponse({'valid':False, 'message': 'Current Password is incorrect!'}, status=200)
        else:
            return JsonResponse({'valid':False, 'message':'Invalid request method'}, status=200)

    return JsonResponse({'valid':False, 'message': 'Failed to change password'}, status=200)



# function to edit address
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def manage_address(request):
    if request.method == "POST":
        user = CustomUser.objects.filter(email = request.user).first()
        country = request.POST.get('country')
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        c_address = request.POST.get('c_address')
        city = request.POST.get('city')
        landMark = request.POST.get('landmark')
        state = request.POST.get('state')
        postal = request.POST.get('postal_zip')
        c_phone = request.POST.get('c_phone')

        if not f_name.isalpha() or len(f_name) < 3:
            return redirect('manage_address')
        
        if not l_name.isalpha() or len(l_name) < 3:
            return redirect('manage_address')
        
        c_address_stripped = c_address.strip()
        if not c_address_stripped or len(c_address) < 6:
            return redirect('manage_address')
        
        city_stripped = city.strip()
        if not city_stripped or len(city) < 3:
            return redirect('manage_address')
        
        landMark_stripped = landMark.strip()
        if not landMark_stripped or len(landMark) < 3:
            return redirect('manage_address')
        
        state_stripped = state.strip()
        if not state_stripped or len(state) < 3:
            return redirect('manage_address')
        
        if not postal.isdigit() or len(postal) != 6:
            return redirect('manage_address')
        
        if not c_phone.isdigit() or len(c_phone) != 10:
            return redirect('manage_address')
        
        addressess = Address.objects.create(
            user = user,
            country = country,
            first_name = f_name,
            last_name = l_name,
            street_address = c_address,
            city = city,
            landmark = landMark,
            state = state,
            pin_code = postal,
            phone = c_phone,

        )
        
        return redirect('manage_address')
    
    else:
        return render(request, 'platform/my_profile.html')