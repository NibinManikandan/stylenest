import email
from genericpath import exists
from django.contrib import messages
from django.shortcuts import render,redirect, redirect,get_object_or_404
from userAuth.models import *
from Userprofile.models import *
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout
from django.http import JsonResponse
import re
# Create your views here.



# function to user profile in profile
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def my_details(request):
    if request.user.is_authenticated:
        data = CustomUser.objects.filter(email = request.user).first()
        addressess = Address.objects.filter(user=request.user)

    context = {
        'data':data,
        'addressess':addressess
    }
    return render(request, 'platform/my_profile.html', context)



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
    return render(request, 'platform/my_profile.html')



# function to change password
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            old_pass = request.POST.get('old_pass')
            new_pass = request.POST.get('new_pass')
            cnf_new_pass = request.POST.get('cnf_new_pass')

            password_pattern = "^(?=.*[a-z])(?=.*[A-Z]).{6,}$"

            if check_password(old_pass, user.password):
                if new_pass == cnf_new_pass:
                    if re.match(password_pattern, new_pass):
                        user.set_password(new_pass)
                        user.save()
                        logout(request)
                        
                        print('password changed')

                        return JsonResponse({'success': True, 'message': 'Password changed successfully.'})
                    else:
                        return JsonResponse({'success': False, 'message': "New password must contain at least one uppercase letter, one lowercase letter, and be at least 6 characters long."}, status=400)
                else:
                    return JsonResponse({'success': False, 'message': 'Password and Confirm Password do not match!'}, status=400)
            else:
                return JsonResponse({'success': False, 'message': 'Current Password is incorrect!'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=400)
    


# function to add address
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_address(request):
    if request.method == "POST":
        user = CustomUser.objects.get(email=request.user)
        country = request.POST.get('country')
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        c_address = request.POST.get('c_address')
        city = request.POST.get('city')
        landMark = request.POST.get('landmark')
        state = request.POST.get('state')
        postal = request.POST.get('postal_zip')
        c_phone = request.POST.get('c_phone')
        
        f_name_stripped = f_name.strip()
        if not f_name_stripped.isalpha() or len(f_name) < 3:
            return redirect('add_address')
        
        l_name_stripped = l_name.strip()
        if not l_name_stripped.isalpha() or len(l_name) < 3:
            return redirect('add_address')
        
        c_address_stripped = c_address.strip()
        if not c_address_stripped or len(c_address) < 6:
            return redirect('add_address')
        
        city_stripped = city.strip()
        if not city_stripped or len(city) < 3:
            return redirect('add_address')
        
        landMark_stripped = landMark.strip()
        if not landMark_stripped or len(landMark) < 3:
            return redirect('add_address')
        
        state_stripped = state.strip()
        if not state_stripped or len(state) < 3:
            return redirect('add_address')
        
        pin_stripped = postal.strip()
        if not pin_stripped.isdigit() or len(postal) != 6:
            return redirect('add_address')
        
        phone_stripped = c_phone.strip()
        if not phone_stripped.isdigit() or len(c_phone) != 10:
            return redirect('add_address')
        
        new_address = Address.objects.create(
            user=user,
            country=country,
            first_name=f_name,
            last_name=l_name,
            street_address=c_address,
            city=city,
            landmark=landMark,
            state=state,
            pin_code=postal,
            phone=c_phone,
        )
        new_address.save()
        
        return redirect('add_address')

    else:
        return render(request, 'platform/my_profile.html')
    

# function to edit address
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_address(request, id):
    if request.user.is_authenticated:
        addresses = get_object_or_404(Address, id=id)
    if request.method == "POST":
        country = request.POST.get('country')
        f_name = request.POST.get('fname')
        l_name = request.POST.get('lname')
        c_address = request.POST.get('c_address')
        city = request.POST.get('city')
        landMark = request.POST.get('landmark')
        state = request.POST.get('state')
        postal = request.POST.get('postal_zip')
        c_phone = request.POST.get('c_phone')

        f_name_stripped = f_name.strip()
        if not f_name_stripped.isalpha() or len(f_name) < 3:
            return redirect('edit_address', id=id)
        
        l_name_stripped = l_name.strip()
        if not l_name_stripped.isalpha() or len(l_name) < 3:
            return redirect('edit_address', id=id)
        
        c_address_stripped = c_address.strip()
        if not c_address_stripped or len(c_address) < 6:
            return redirect('edit_address', id=id)
        
        city_stripped = city.strip()
        if not city_stripped or len(city) < 3:
            return redirect('edit_address', id=id)
        
        landMark_stripped = landMark.strip()
        if not landMark_stripped or len(landMark) < 3:
            return redirect('edit_address', id=id)
        
        state_stripped = state.strip()
        if not state_stripped or len(state) < 3:
            return redirect('edit_address', id=id)
        
        pin_stripped = postal.strip()
        if not pin_stripped.isdigit() or len(postal) != 6:
            return redirect('edit_address', id=id)
        
        phone_stripped = c_phone.strip()
        if not phone_stripped.isdigit() or len(c_phone) != 10:
            return redirect('edit_address', id=id)
        
        addresses.country = country
        addresses.first_name = f_name
        addresses.last_name = l_name
        addresses.street_address = c_address
        addresses.city = city
        addresses.landmark = landMark
        addresses.state = state
        addresses.pin_code = postal
        addresses.phone = c_phone
        addresses.save()

        return redirect('my_details')
        
    else:
        return render(request, 'platform/my_profile.html')



# function to delete address
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def del_address(request, id):
    if request.user.is_authenticated:
        user = request.user
        addresses = get_object_or_404(Address, id=id)
        if addresses.user != user:
            return redirect('my_details') 

        addresses.delete()
        return redirect('my_details')
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_details(request):
    if request.method == "POST":
        user = request.user
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        
        if len(first_name) < 4:
            return JsonResponse({'error': 'Minimum 4 characters required for First Name'}, status=400)

        if len(last_name) < 4:
            return JsonResponse({'error': 'Minimum 4 characters required for Last Name'}, status=400)

        if not phone.isdigit() or len(phone) != 10:
            return JsonResponse({'error': 'Enter a valid Phone number (10 digits)'}, status=400)

        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.save()

        return JsonResponse({'success': 'Profile details updated successfully'})

    return render(request, 'platform/my_profile.html')