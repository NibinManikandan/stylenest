from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages




# Create your views here.


def Admin_Log(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        admin = authenticate(

            username=username,
            password=password
        )

        if admin is not None and admin.is_superuser:
            login(request, admin)
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('admin_login')

    return render(request, 'Admin_Auth/adm_login.html')









